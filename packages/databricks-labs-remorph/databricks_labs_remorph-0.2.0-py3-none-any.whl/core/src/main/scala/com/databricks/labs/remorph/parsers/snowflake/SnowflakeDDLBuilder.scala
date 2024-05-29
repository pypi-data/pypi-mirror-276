package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.{IncompleteParser, ParserCommon, intermediate => ir}
import SnowflakeParser.{StringContext => StrContext, _}
import com.databricks.labs.remorph.parsers.intermediate.AddColumn

import scala.collection.JavaConverters._
class SnowflakeDDLBuilder
    extends SnowflakeParserBaseVisitor[ir.Catalog]
    with ParserCommon
    with IncompleteParser[ir.Catalog] {
  override protected def wrapUnresolvedInput(unparsedInput: String): ir.Catalog = ir.UnresolvedCatalog(unparsedInput)

  private def extractString(ctx: StrContext): String = {
    ctx.getText.stripPrefix("'").stripSuffix("'")
  }

  override def visitCreate_function(ctx: Create_functionContext): ir.Catalog = {
    val runtimeInfo = ctx match {
      case c if c.JAVA() != null => buildJavaUDF(c)
      case c if c.PYTHON() != null => buildPythonUDF(c)
      case c if c.JAVASCRIPT() != null => ir.JavascriptUDFInfo
      case c if c.SCALA() != null => buildScalaUDF(c)
      case c if c.SQL() != null || c.LANGUAGE() == null => ir.SQLUDFInfo(c.MEMOIZABLE() != null)
    }
    val name = ctx.object_name().getText
    val returnType = DataTypeBuilder.buildDataType(ctx.data_type())
    val parameters = ctx.arg_decl().asScala.map(buildParameter)
    val acceptsNullParameters = ctx.CALLED() != null
    val body = buildFunctionBody(ctx.function_definition())
    val comment = Option(ctx.comment_clause()).map(c => extractString(c.string()))
    ir.CreateInlineUDF(name, returnType, parameters, runtimeInfo, acceptsNullParameters, comment, body)
  }

  private def buildParameter(ctx: Arg_declContext): ir.FunctionParameter = {
    ir.FunctionParameter(
      name = ctx.arg_name().getText,
      dataType = DataTypeBuilder.buildDataType(ctx.arg_data_type().id_().data_type()),
      defaultValue = Option(ctx.arg_default_value_clause()).map(_.expr().accept(new SnowflakeExpressionBuilder)))
  }

  private def buildFunctionBody(ctx: Function_definitionContext): String = (ctx match {
    case c if c.DBL_DOLLAR() != null => c.DBL_DOLLAR().getText.stripPrefix("$$").stripSuffix("$$")
    case c if c.string() != null => extractString(c.string())
  }).trim

  private def buildJavaUDF(ctx: Create_functionContext): ir.UDFRuntimeInfo = buildJVMUDF(ctx)(ir.JavaUDFInfo.apply)
  private def buildScalaUDF(ctx: Create_functionContext): ir.UDFRuntimeInfo = buildJVMUDF(ctx)(ir.ScalaUDFInfo.apply)

  private def buildJVMUDF(ctx: Create_functionContext)(
      ctr: (Option[String], Seq[String], String) => ir.UDFRuntimeInfo): ir.UDFRuntimeInfo = {
    val imports =
      ctx
        .string_list()
        .asScala
        .find(occursBefore(ctx.IMPORTS(), _))
        .map(_.string().asScala.map(extractString))
        .getOrElse(Seq())
    ctr(extractRuntimeVersion(ctx), imports, extractHandler(ctx))
  }
  private def extractRuntimeVersion(ctx: Create_functionContext): Option[String] = ctx.string().asScala.collectFirst {
    case c if occursBefore(ctx.RUNTIME_VERSION(), c) => extractString(c)
  }

  private def extractHandler(ctx: Create_functionContext): String =
    Option(ctx.HANDLER()).flatMap(h => ctx.string().asScala.find(occursBefore(h, _))).map(extractString).get

  private def buildPythonUDF(ctx: Create_functionContext): ir.PythonUDFInfo = {
    val packages =
      ctx
        .string_list()
        .asScala
        .find(occursBefore(ctx.PACKAGES(0), _))
        .map(_.string().asScala.map(extractString))
        .getOrElse(Seq())
    ir.PythonUDFInfo(extractRuntimeVersion(ctx), packages, extractHandler(ctx))
  }

  override def visitCreate_table(ctx: Create_tableContext): ir.Catalog = {
    val tableName = ctx.object_name().getText
    val columns = buildColumnDeclarations(
      ctx
        .create_table_clause()
        .column_decl_item_list_paren()
        .column_decl_item_list()
        .column_decl_item()
        .asScala)

    ir.CreateTableCommand(tableName, columns)
  }

  private def buildColumnDeclarations(ctx: Seq[Column_decl_itemContext]): Seq[ir.ColumnDeclaration] = {
    // According to the grammar, either ctx.full_col_decl or ctx.out_of_line_constraint is non-null.
    val columns = ctx.collect {
      case c if c.full_col_decl() != null => buildColumnDeclaration(c.full_col_decl())
    }
    // An out-of-line constraint may apply to one or many columns
    // When an out-of-line contraint applies to multiple columns,
    // we record a column-name -> constraint mapping for each.
    val outOfLineConstraints: Seq[(String, ir.Constraint)] = ctx.collect {
      case c if c.out_of_line_constraint() != null => buildOutOfLineConstraints(c.out_of_line_constraint())
    }.flatten

    // Finally, for every column, we "inject" the relevant out-of-line constraints
    columns.map { col =>
      val additionalConstraints = outOfLineConstraints.collect {
        case (columnName, constraint) if columnName == col.name => constraint
      }
      col.copy(constraints = col.constraints ++ additionalConstraints)
    }
  }

  private def buildColumnDeclaration(ctx: Full_col_declContext): ir.ColumnDeclaration = {
    val name = ctx.col_decl().column_name().getText
    val dataType = DataTypeBuilder.buildDataType(ctx.col_decl().data_type())
    val constraints = ctx.inline_constraint().asScala.map(buildInlineConstraint)
    val nullability = if (ctx.null_not_null().isEmpty) {
      Seq()
    } else {
      Seq(ir.Nullability(!ctx.null_not_null().asScala.exists(_.NOT() != null)))
    }
    ir.ColumnDeclaration(name, dataType, virtualColumnDeclaration = None, nullability ++ constraints)
  }

  private[snowflake] def buildOutOfLineConstraints(ctx: Out_of_line_constraintContext): Seq[(String, ir.Constraint)] = {
    val columnNames = ctx.column_list_in_parentheses(0).column_list().column_name().asScala.map(_.getText)
    val repeatForEveryColumnName = List.fill[ir.UnnamedConstraint](columnNames.size)(_)
    val unnamedConstraints = ctx match {
      case c if c.UNIQUE() != null => repeatForEveryColumnName(ir.Unique)
      case c if c.primary_key() != null => repeatForEveryColumnName(ir.PrimaryKey)
      case c if c.foreign_key() != null =>
        val referencedObject = c.object_name().getText
        val references =
          c.column_list_in_parentheses(1).column_list().column_name().asScala.map(referencedObject + "." + _.getText)
        references.map(ir.ForeignKey.apply)
      case c => repeatForEveryColumnName(ir.UnresolvedConstraint(c.getText))
    }
    val constraintNameOpt = Option(ctx.id_()).map(_.getText)
    val constraints = constraintNameOpt.fold[Seq[ir.Constraint]](unnamedConstraints) { name =>
      unnamedConstraints.map(ir.NamedConstraint(name, _))
    }
    columnNames.zip(constraints)
  }

  private[snowflake] def buildInlineConstraint(ctx: Inline_constraintContext): ir.Constraint = ctx match {
    case c if c.UNIQUE() != null => ir.Unique
    case c if c.primary_key() != null => ir.PrimaryKey
    case c if c.foreign_key() != null =>
      val references = c.object_name().getText + Option(ctx.column_name()).map("." + _.getText).getOrElse("")
      ir.ForeignKey(references)
    case c => ir.UnresolvedConstraint(c.getText)
  }

  override def visitAlter_table(ctx: Alter_tableContext): ir.Catalog = {
    val tableName = ctx.object_name(0).getText
    ctx match {
      case c if c.table_column_action() != null =>
        ir.AlterTableCommand(tableName, buildColumnActions(c.table_column_action()))
      case c if c.constraint_action() != null =>
        ir.AlterTableCommand(tableName, buildConstraintActions(c.constraint_action()))
      case c => ir.UnresolvedCatalog(c.getText)
    }
  }

  private[snowflake] def buildColumnActions(ctx: Table_column_actionContext): Seq[ir.TableAlteration] = ctx match {
    case c if c.ADD() != null =>
      c.full_col_decl().asScala.map(buildColumnDeclaration).map(AddColumn.apply)
    case c if !c.alter_column_clause().isEmpty =>
      c.alter_column_clause().asScala.map(buildColumnAlterations)
    case c if c.DROP() != null =>
      Seq(ir.DropColumns(c.column_list().column_name().asScala.map(_.getText)))
    case c if c.RENAME() != null =>
      Seq(ir.RenameColumn(c.column_name(0).getText, c.column_name(1).getText))
    case c => Seq(ir.UnresolvedTableAlteration(c.getText))
  }

  private[snowflake] def buildColumnAlterations(ctx: Alter_column_clauseContext): ir.TableAlteration = {
    val columnName = ctx.column_name().getText
    ctx match {
      case c if c.data_type() != null =>
        ir.ChangeColumnDataType(columnName, DataTypeBuilder.buildDataType(c.data_type()))
      case c if c.DROP() != null && c.NULL_() != null =>
        ir.DropConstraint(Some(columnName), ir.Nullability(c.NOT() == null))
      case c if c.NULL_() != null =>
        ir.AddConstraint(columnName, ir.Nullability(c.NOT() == null))
      case c => ir.UnresolvedTableAlteration(c.getText)
    }
  }

  private[snowflake] def buildConstraintActions(ctx: Constraint_actionContext): Seq[ir.TableAlteration] = ctx match {
    case c if c.ADD() != null =>
      buildOutOfLineConstraints(c.out_of_line_constraint()).map(ir.AddConstraint.tupled)
    case c if c.DROP() != null =>
      buildDropConstraints(c)
    case c if c.RENAME() != null =>
      Seq(ir.RenameConstraint(c.id_(0).getText, c.id_(1).getText))
    case c => Seq(ir.UnresolvedTableAlteration(c.getText))
  }

  private[snowflake] def buildDropConstraints(ctx: Constraint_actionContext): Seq[ir.TableAlteration] = {
    val columnListOpt = Option(ctx.column_list_in_parentheses())
    val affectedColumns = columnListOpt.map(_.column_list().column_name().asScala.map(_.getText)).getOrElse(Seq())
    ctx match {
      case c if c.primary_key() != null => dropConstraints(affectedColumns, ir.PrimaryKey)
      case c if c.UNIQUE() != null => dropConstraints(affectedColumns, ir.Unique)
      case c if c.id_.size() > 0 => Seq(ir.DropConstraintByName(c.id_(0).getText))
      case c => Seq(ir.UnresolvedTableAlteration(ctx.getText))
    }
  }

  private def dropConstraints(affectedColumns: Seq[String], constraint: ir.Constraint): Seq[ir.TableAlteration] = {
    if (affectedColumns.isEmpty) {
      Seq(ir.DropConstraint(None, constraint))
    } else {
      affectedColumns.map(col => ir.DropConstraint(Some(col), constraint))
    }
  }
}
