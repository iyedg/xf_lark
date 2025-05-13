import pytest

from xf_lark import XFParser

parser = XFParser()


def test_number_literal():
    expression = "123"
    expected_ast = {"type": "number_literal", "value": 123.0}
    assert parser.parse(expression) == expected_ast


def test_string_literal_single_quotes():
    expression = "'hello'"
    expected_ast = {"type": "string_literal", "value": "hello"}
    assert parser.parse(expression) == expected_ast


def test_string_literal_double_quotes():
    expression = '"world"'
    expected_ast = {"type": "string_literal", "value": "world"}
    assert parser.parse(expression) == expected_ast


def test_variable_reference():
    expression = "${myVar}"
    expected_ast = {"type": "variable_ref", "name": "myVar"}
    assert parser.parse(expression) == expected_ast


def test_bare_variable_reference():
    expression = "bareVar"
    expected_ast = {"type": "bare_variable_ref", "name": "bareVar"}
    assert parser.parse(expression) == expected_ast


def test_current_reference():
    expression = "."
    expected_ast = {"type": "current_ref"}
    assert parser.parse(expression) == expected_ast


def test_parent_reference():
    expression = ".."
    expected_ast = {"type": "parent_ref"}
    assert parser.parse(expression) == expected_ast


def test_simple_addition():
    expression = "1 + 2"
    expected_ast = {
        "type": "binary_op",
        "operator": "add",
        "left": {"type": "number_literal", "value": 1.0},
        "right": {"type": "number_literal", "value": 2.0},
    }
    assert parser.parse(expression) == expected_ast


def test_addition_with_variable():
    expression = "${count} + 10"
    expected_ast = {
        "type": "binary_op",
        "operator": "add",
        "left": {"type": "variable_ref", "name": "count"},
        "right": {"type": "number_literal", "value": 10.0},
    }
    assert parser.parse(expression) == expected_ast


def test_subtraction():
    expression = "10 - 3"
    expected_ast = {
        "type": "binary_op",
        "operator": "subtract",
        "left": {"type": "number_literal", "value": 10.0},
        "right": {"type": "number_literal", "value": 3.0},
    }
    assert parser.parse(expression) == expected_ast


def test_multiplication():
    expression = "3 * 4"
    expected_ast = {
        "type": "binary_op",
        "operator": "multiply",
        "left": {"type": "number_literal", "value": 3.0},
        "right": {"type": "number_literal", "value": 4.0},
    }
    assert parser.parse(expression) == expected_ast


def test_division():
    expression = "10 div 2"
    expected_ast = {
        "type": "binary_op",
        "operator": "divide",
        "left": {"type": "number_literal", "value": 10.0},
        "right": {"type": "number_literal", "value": 2.0},
    }
    assert parser.parse(expression) == expected_ast


def test_operator_precedence():
    expression = "1 + 2 * 3"  # Expected: 1 + (2 * 3)
    expected_ast = {
        "type": "binary_op",
        "operator": "add",
        "left": {"type": "number_literal", "value": 1.0},
        "right": {
            "type": "binary_op",
            "operator": "multiply",
            "left": {"type": "number_literal", "value": 2.0},
            "right": {"type": "number_literal", "value": 3.0},
        },
    }
    assert parser.parse(expression) == expected_ast


def test_parentheses_override_precedence():
    expression = "(1 + 2) * 3"
    expected_ast = {
        "type": "binary_op",
        "operator": "multiply",
        "left": {
            "type": "binary_op",
            "operator": "add",
            "left": {"type": "number_literal", "value": 1.0},
            "right": {"type": "number_literal", "value": 2.0},
        },
        "right": {"type": "number_literal", "value": 3.0},
    }
    assert parser.parse(expression) == expected_ast


def test_unary_minus():
    expression = "-5"
    expected_ast = {
        "type": "unary_op",
        "operator": "unary_minus",
        "operand": {"type": "number_literal", "value": 5.0},
    }
    assert parser.parse(expression) == expected_ast


def test_unary_minus_with_expression():
    expression = "-(1 + 2)"
    expected_ast = {
        "type": "unary_op",
        "operator": "unary_minus",
        "operand": {
            "type": "binary_op",
            "operator": "add",
            "left": {"type": "number_literal", "value": 1.0},
            "right": {"type": "number_literal", "value": 2.0},
        },
    }
    assert parser.parse(expression) == expected_ast


def test_simple_function_call_no_args():
    expression = "today()"
    expected_ast = {"type": "function_call", "name": "today", "arguments": []}
    assert parser.parse(expression) == expected_ast


def test_function_call_with_one_arg():
    expression = "round(1.23)"
    expected_ast = {
        "type": "function_call",
        "name": "round",
        "arguments": [{"type": "number_literal", "value": 1.23}],
    }
    assert parser.parse(expression) == expected_ast


def test_function_call_with_multiple_args():
    expression = "concat('hello', ${user}, 12)"
    expected_ast = {
        "type": "function_call",
        "name": "concat",
        "arguments": [
            {"type": "string_literal", "value": "hello"},
            {"type": "variable_ref", "name": "user"},
            {"type": "number_literal", "value": 12.0},
        ],
    }
    assert parser.parse(expression) == expected_ast


def test_nested_function_call():
    expression = "string-length(concat('a', 'b'))"
    expected_ast = {
        "type": "function_call",
        "name": "string-length",
        "arguments": [
            {
                "type": "function_call",
                "name": "concat",
                "arguments": [
                    {"type": "string_literal", "value": "a"},
                    {"type": "string_literal", "value": "b"},
                ],
            }
        ],
    }
    assert parser.parse(expression) == expected_ast


# --- Comparison Operators ---
@pytest.mark.parametrize(
    "op_str, op_name",
    [
        ("=", "eq"),
        ("!=", "ne"),
        ("<", "lt"),
        (">", "gt"),
        ("<=", "lte"),
        (">=", "gte"),
    ],
)
def test_comparison_operators(op_str, op_name):
    expression = f"1 {op_str} 2"
    expected_ast = {
        "type": "binary_op",
        "operator": op_name,
        "left": {"type": "number_literal", "value": 1.0},
        "right": {"type": "number_literal", "value": 2.0},
    }
    assert parser.parse(expression) == expected_ast


# --- Logical Operators ---
def test_logical_and():
    expression = "1 > 0 and ${var} < 10"
    expected_ast = {
        "type": "binary_op",
        "operator": "and",
        "left": {
            "type": "binary_op",
            "operator": "gt",
            "left": {"type": "number_literal", "value": 1.0},
            "right": {"type": "number_literal", "value": 0.0},
        },
        "right": {
            "type": "binary_op",
            "operator": "lt",
            "left": {"type": "variable_ref", "name": "var"},
            "right": {"type": "number_literal", "value": 10.0},
        },
    }
    assert parser.parse(expression) == expected_ast


def test_logical_or():
    expression = "selected(.) or false()"
    expected_ast = {
        "type": "binary_op",
        "operator": "or",
        "left": {
            "type": "function_call",
            "name": "selected",
            "arguments": [{"type": "current_ref"}],
        },
        "right": {"type": "function_call", "name": "false", "arguments": []},
    }
    assert parser.parse(expression) == expected_ast


def test_complex_logical_expression():
    expression = "(1=1 or 2=2) and (3=3 or 4=4)"  # (true or true) and (true or true)
    expected_ast = {
        "type": "binary_op",
        "operator": "and",
        "left": {
            "type": "binary_op",
            "operator": "or",
            "left": {
                "type": "binary_op",
                "operator": "eq",
                "left": {"type": "number_literal", "value": 1.0},
                "right": {"type": "number_literal", "value": 1.0},
            },
            "right": {
                "type": "binary_op",
                "operator": "eq",
                "left": {"type": "number_literal", "value": 2.0},
                "right": {"type": "number_literal", "value": 2.0},
            },
        },
        "right": {
            "type": "binary_op",
            "operator": "or",
            "left": {
                "type": "binary_op",
                "operator": "eq",
                "left": {"type": "number_literal", "value": 3.0},
                "right": {"type": "number_literal", "value": 3.0},
            },
            "right": {
                "type": "binary_op",
                "operator": "eq",
                "left": {"type": "number_literal", "value": 4.0},
                "right": {"type": "number_literal", "value": 4.0},
            },
        },
    }
    assert parser.parse(expression) == expected_ast


def test_syntax_error():
    with pytest.raises(Exception):
        parser.parse("1 +")


def test_empty_expression():
    with pytest.raises(Exception):
        parser.parse("")
