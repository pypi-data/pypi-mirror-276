package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate._
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser.{Comparison_operatorContext, LiteralContext, Ranking_windowed_functionContext}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec
import org.mockito.Mockito._
import org.scalatestplus.mockito.MockitoSugar

class SnowflakeExpressionBuilderSpec
    extends AnyWordSpec
    with SnowflakeParserTestCommon
    with Matchers
    with MockitoSugar {

  override protected def astBuilder: SnowflakeExpressionBuilder = new SnowflakeExpressionBuilder

  "SnowflakeExpressionBuilder" should {
    "translate literals" in {
      example("null", _.literal(), Literal(nullType = Some(NullType())))
      example("true", _.literal(), Literal(boolean = Some(true)))
      example("false", _.literal(), Literal(boolean = Some(false)))
      example("1", _.literal(), Literal(integer = Some(1)))
      example("-1", _.literal(), Literal(integer = Some(-1)))
      example("1.1", _.literal(), Literal(float = Some(1.1f)))
      example("1.1e2", _.literal(), Literal(integer = Some(110)))
      example("1.1e-2", _.literal(), Literal(float = Some(0.011f)))
      example("0.123456789", _.literal(), Literal(double = Some(0.123456789)))
      example("0.123456789e-1234", _.literal(), Literal(decimal = Some(Decimal("0.123456789e-1234", None, None))))
      example("'foo'", _.literal(), Literal(string = Some("foo")))
    }

    "translate column names" in {
      example("x", _.column_name(), Column("x"))
    }

    "translate aggregation functions" in {
      example("COUNT(x)", _.aggregate_function(), Count(Column("x")))
    }

    "translate a query with a window function" in {

      example(
        query = "ROW_NUMBER() OVER (ORDER BY a DESC)",
        rule = _.ranking_windowed_function(),
        expectedAst = Window(
          window_function = RowNumber,
          partition_spec = Seq(),
          sort_order = Seq(SortOrder(Column("a"), DescendingSortDirection, SortNullsLast)),
          frame_spec = WindowFrame(
            frame_type = RowsFrame,
            lower = FrameBoundary(current_row = false, unbounded = true, value = Noop),
            upper = FrameBoundary(current_row = true, unbounded = false, value = Noop))))

      example(
        query = "ROW_NUMBER() OVER (PARTITION BY a)",
        rule = _.ranking_windowed_function(),
        expectedAst = Window(
          window_function = RowNumber,
          partition_spec = Seq(Column("a")),
          sort_order = Seq(),
          frame_spec = WindowFrame(
            frame_type = RowsFrame,
            lower = FrameBoundary(current_row = false, unbounded = true, value = Noop),
            upper = FrameBoundary(current_row = true, unbounded = false, value = Noop))))
      example(
        query = "NTILE(42) OVER (PARTITION BY a ORDER BY b, c DESC, d)",
        rule = _.ranking_windowed_function(),
        expectedAst = Window(
          window_function = NTile(Literal(integer = Some(42))),
          partition_spec = Seq(Column("a")),
          sort_order = Seq(
            SortOrder(Column("b"), AscendingSortDirection, SortNullsLast),
            SortOrder(Column("c"), DescendingSortDirection, SortNullsLast),
            SortOrder(Column("d"), AscendingSortDirection, SortNullsLast)),
          frame_spec = WindowFrame(
            frame_type = RowsFrame,
            lower = FrameBoundary(current_row = false, unbounded = true, value = Noop),
            upper = FrameBoundary(current_row = true, unbounded = false, value = Noop))))
    }

    // see https://github.com/databrickslabs/remorph/issues/258
    "missing bits in window function grammar" ignore {

      // line 1:35 mismatched input 'NULLS' expecting {')', ','}
      example(
        query = "ROW_NUMBER() OVER (ORDER BY a DESC NULLS FIRST)",
        rule = _.ranking_windowed_function(),
        expectedAst = Window(
          window_function = RowNumber,
          partition_spec = Seq(),
          sort_order = Seq(SortOrder(Column("a"), DescendingSortDirection, SortNullsLast)),
          frame_spec = WindowFrame(
            frame_type = RowsFrame,
            lower = FrameBoundary(current_row = false, unbounded = true, value = Noop),
            upper = FrameBoundary(current_row = true, unbounded = false, value = Noop))))

      // line 1:33 no viable alternative at input 'a ROWS'
      example(
        query = "ROW_NUMBER() OVER(PARTITION BY a ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)",
        rule = _.ranking_windowed_function(),
        expectedAst = null)
    }

    "translate star-expressions" in {
      example("*", _.column_elem_star(), Star(None))
      example("t.*", _.column_elem_star(), Star(Some("t")))
    }
  }

  "SnowflakeExpressionBuilder.buildSortOrder" should {

    "translate ORDER BY a" in {
      val tree = parseString("ORDER BY a", _.order_by_expr())
      (new SnowflakeExpressionBuilder).buildSortOrder(tree) shouldBe Seq(
        SortOrder(Column("a"), AscendingSortDirection, SortNullsLast))
    }

    "translate ORDER BY a ASC" in {
      val tree = parseString("ORDER BY a ASC", _.order_by_expr())
      (new SnowflakeExpressionBuilder).buildSortOrder(tree) shouldBe Seq(
        SortOrder(Column("a"), AscendingSortDirection, SortNullsLast))
    }

    "translate ORDER BY a DESC" in {
      val tree = parseString("ORDER BY a DESC", _.order_by_expr())
      (new SnowflakeExpressionBuilder).buildSortOrder(tree) shouldBe Seq(
        SortOrder(Column("a"), DescendingSortDirection, SortNullsLast))
    }

    "translate ORDER BY a, b DESC" in {
      val tree = parseString("ORDER BY a, b DESC", _.order_by_expr())
      (new SnowflakeExpressionBuilder).buildSortOrder(tree) shouldBe Seq(
        SortOrder(Column("a"), AscendingSortDirection, SortNullsLast),
        SortOrder(Column("b"), DescendingSortDirection, SortNullsLast))
    }

    "translate ORDER BY a DESC, b" in {
      val tree = parseString("ORDER BY a DESC, b", _.order_by_expr())
      (new SnowflakeExpressionBuilder).buildSortOrder(tree) shouldBe Seq(
        SortOrder(Column("a"), DescendingSortDirection, SortNullsLast),
        SortOrder(Column("b"), AscendingSortDirection, SortNullsLast))
    }

    "translate ORDER BY with many expressions" in {
      val tree = parseString("ORDER BY a DESC, b, c ASC, d DESC, e", _.order_by_expr())
      (new SnowflakeExpressionBuilder).buildSortOrder(tree) shouldBe Seq(
        SortOrder(Column("a"), DescendingSortDirection, SortNullsLast),
        SortOrder(Column("b"), AscendingSortDirection, SortNullsLast),
        SortOrder(Column("c"), AscendingSortDirection, SortNullsLast),
        SortOrder(Column("d"), DescendingSortDirection, SortNullsLast),
        SortOrder(Column("e"), AscendingSortDirection, SortNullsLast))
    }

    "translate EXISTS expressions" in {
      example("EXISTS (SELECT * FROM t)", _.predicate, Exists(Project(namedTable("t"), Seq(Star(None)))))
    }

    // see https://github.com/databrickslabs/remorph/issues/273
    "translate NOT EXISTS expressions" ignore {
      example("NOT EXISTS (SELECT * FROM t)", _.expr(), Not(Exists(Project(namedTable("t"), Seq(Star(None))))))
    }

  }

  "translate CASE expressions" in {
    example(
      "CASE WHEN col1 = 1 THEN 'one' WHEN col2 = 2 THEN 'two' END",
      _.case_expression(),
      Case(
        expression = None,
        branches = scala.collection.immutable.Seq(
          WhenBranch(Equals(Column("col1"), Literal(integer = Some(1))), Literal(string = Some("one"))),
          WhenBranch(Equals(Column("col2"), Literal(integer = Some(2))), Literal(string = Some("two")))),
        otherwise = None))

    example(
      "CASE 'foo' WHEN col1 = 1 THEN 'one' WHEN col2 = 2 THEN 'two' END",
      _.case_expression(),
      Case(
        expression = Some(Literal(string = Some("foo"))),
        branches = scala.collection.immutable.Seq(
          WhenBranch(Equals(Column("col1"), Literal(integer = Some(1))), Literal(string = Some("one"))),
          WhenBranch(Equals(Column("col2"), Literal(integer = Some(2))), Literal(string = Some("two")))),
        otherwise = None))

    example(
      "CASE WHEN col1 = 1 THEN 'one' WHEN col2 = 2 THEN 'two' ELSE 'other' END",
      _.case_expression(),
      Case(
        expression = None,
        branches = scala.collection.immutable.Seq(
          WhenBranch(Equals(Column("col1"), Literal(integer = Some(1))), Literal(string = Some("one"))),
          WhenBranch(Equals(Column("col2"), Literal(integer = Some(2))), Literal(string = Some("two")))),
        otherwise = Some(Literal(string = Some("other")))))

    example(
      "CASE 'foo' WHEN col1 = 1 THEN 'one' WHEN col2 = 2 THEN 'two' ELSE 'other' END",
      _.case_expression(),
      Case(
        expression = Some(Literal(string = Some("foo"))),
        branches = scala.collection.immutable.Seq(
          WhenBranch(Equals(Column("col1"), Literal(integer = Some(1))), Literal(string = Some("one"))),
          WhenBranch(Equals(Column("col2"), Literal(integer = Some(2))), Literal(string = Some("two")))),
        otherwise = Some(Literal(string = Some("other")))))

  }

  "Unparsed input" should {
    "be reported as UnresolvedExpression" in {
      example("{'name':'Homer Simpson'}", _.json_literal(), UnresolvedExpression("{'name':'Homer Simpson'}"))
    }
  }

  "SnowflakeExpressionBuilder.visit_Literal" should {
    "handle unresolved input" in {
      val literal = mock[LiteralContext]
      astBuilder.visitLiteral(literal) shouldBe Literal(nullType = Some(NullType()))
      verify(literal).sign()
      verify(literal).STRING()
      verify(literal).DECIMAL()
      verify(literal).FLOAT()
      verify(literal).REAL()
      verify(literal).true_false()
      verify(literal).NULL_()
      verifyNoMoreInteractions(literal)
    }
  }

  "SnowflakeExpressionBuilder.buildComparisonExpression" should {
    "handle unresolved input" in {
      val operator = mock[Comparison_operatorContext]
      val dummyTextForOperator = "dummy"
      when(operator.getText).thenReturn(dummyTextForOperator)
      astBuilder.buildComparisonExpression(operator, null, null) shouldBe UnresolvedExpression(dummyTextForOperator)
      verify(operator).EQ()
      verify(operator).NE()
      verify(operator).LTGT()
      verify(operator).GT()
      verify(operator).LT()
      verify(operator).GE()
      verify(operator).LE()
      verify(operator).getText
      verifyNoMoreInteractions(operator)
    }
  }

  "SnowflakeExpressionBuilder.buildWindowFunction" should {
    "handle unresolved input" in {
      val windowedFunction = mock[Ranking_windowed_functionContext]
      val dummyTextForWindowedFunction = "dummy"
      when(windowedFunction.getText).thenReturn(dummyTextForWindowedFunction)
      astBuilder.buildWindowFunction(windowedFunction) shouldBe UnresolvedExpression(dummyTextForWindowedFunction)
      verify(windowedFunction).ROW_NUMBER()
      verify(windowedFunction).NTILE()
      verify(windowedFunction).getText
      verifyNoMoreInteractions(windowedFunction)
    }
  }
}
