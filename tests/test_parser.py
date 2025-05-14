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


# This list should be populated with all example expressions from the JSON data we discussed.
# Each item is a tuple: (expression_string, description_string)
odk_expressions_to_validate = [
    # From "Variables (${question-name})"
    ("${some_question_name}", "Feature: Variables - Example: ${some_question_name}"),
    # From "Single Dot (.)"
    (".", "Feature: Single Dot - Example: ."),
    # From "Double Dot (..)"
    ("..", "Feature: Double Dot - Example: .."),
    ("position(..)", "Feature: Double Dot - Example: position(..)"),
    # From "XPath Paths"
    (
        "/data/group_name/question_name",
        "Feature: XPath Paths - Example: /data/group_name/question_name",
    ),
    (
        "../other_question_name",
        "Feature: XPath Paths - Example: ../other_question_name",
    ),
    (
        "instance('external_data')/root/item/value",
        "Feature: XPath Paths - Example: instance('external_data')/root/item/value",
    ),
    # From "XPath Predicates ([])"
    (
        "instance('cities_data')/root/item[state_id = ${selected_state_id}]/city_name",
        "Feature: XPath Predicates - Example: instance(...)/...[...]/...",
    ),
    (
        "/data/repeat_group/item[item_value = 'yes' and position() > 1]",
        "Feature: XPath Predicates - Example: /.../...[... and position() > 1]",
    ),
    # From "Expression" (general examples)
    ("${person_age} > 18", "Feature: Expression - Example: ${person_age} > 18"),
    (
        "concat(${user_first_name}, ' ', ${user_last_name})",
        "Feature: Expression - Example: concat(...)",
    ),
    (
        "if(${is_applicable}='yes', 'value_if_true', 'value_if_false')",
        "Feature: Expression - Example: if(...)",
    ),
    (
        "selected(${multi_select_question}, 'option_value')",
        "Feature: Expression - Example: selected(...)",
    ),
    # From "Calculations"
    (
        "${price} * ${quantity}",
        "Feature: Calculations - Example: ${price} * ${quantity}",
    ),
    ("round(${raw_value}, 2)", "Feature: Calculations - Example: round(...)"),
    ("date(${date_question}) + 5", "Feature: Calculations - Example: date(...) + 5"),
    # From "Values from the last saved record (${last-saved#question-name})"
    (
        "${last-saved#meter_reading}",
        "Feature: Values from last saved record - Example: ${last-saved#meter_reading}",
    ),
    # From "Empty values in math (NaN gotcha) - Handled with functions"
    (
        "coalesce(${optional_number_input}, 0) + 5",
        "Feature: Empty values in math - Example: coalesce(...) + 5",
    ),
    (
        "if(${optional_number_input} = '', 0, ${optional_number_input}) * 10",
        "Feature: Empty values in math - Example: if(...) * 10",
    ),
    # From "Requiring responses" (Note: 'yes' might be a special token for your grammar)
    ("yes", "Feature: Requiring responses - Example: yes"),
    (
        "true()",
        "Feature: Requiring responses - Example: true()",
    ),  # Already covered by function tests typically
    ("${q1_value} != ''", "Feature: Requiring responses - Example: ${q1_value} != ''"),
    # From "Setting default responses"
    (
        "'fixed_default_string'",
        "Feature: Setting default responses - Example: 'fixed_default_string'",
    ),
    (
        "100",
        "Feature: Setting default responses - Example: 100",
    ),  # Covered by number literal
    (
        "${another_question_value}",
        "Feature: Setting default responses - Example: ${another_question_value}",
    ),  # Covered by variable
    (
        "today()",
        "Feature: Setting default responses - Example: today()",
    ),  # Covered by function
    ("uuid()", "Feature: Setting default responses - Example: uuid()"),
    (
        "concat('ID-', ${counter})",
        "Feature: Setting default responses - Example: concat('ID-', ${counter})",
    ),
    # From "Triggering calculations on value change" (These are typically references, not complex expressions themselves)
    (
        "${monitored_question}",
        "Feature: Triggering calculations - Example: ${monitored_question}",
    ),
    (
        "my_question_name_literal",
        "Feature: Triggering calculations - Example: my_question_name_literal",
    ),  # Covered by bare variable if grammar allows
    # From "Validating and restricting responses"
    (". > 0 and . < 100", "Feature: Validating responses - Example: . > 0 and . < 100"),
    # In Python strings, backslashes for regex need to be escaped.
    (
        "regex(., '^\\d{5}$')",
        "Feature: Validating responses - Example: regex(., '^\\d{5}$')",
    ),
    (
        "string-length(.) > 5 and string-length(.) < 10",
        "Feature: Validating responses - Example: string-length(.) > 5 and string-length(.) < 10",
    ),
    (
        "not(selected(., 'none_of_the_above') and count-selected(.) > 1)",
        "Feature: Validating responses - Example: not(selected(...) and count-selected(...))",
    ),
    # From "Read-only questions"
    # ("yes", "Feature: Read-only questions - Example: yes"), # Duplicate of above 'yes'
    # ("true()", "Feature: Read-only questions - Example: true()"), # Duplicate
    (
        "${form_status} = 'closed'",
        "Feature: Read-only questions - Example: ${form_status} = 'closed'",
    ),
    # From "Conditionally showing questions/groups"
    # ("${user_age} >= 18", "Feature: Conditionally showing - Example: ${user_age} >= 18"), # Similar to other comparisons
    # ("${consent_given} = 'yes'", "Feature: Conditionally showing - Example: ${consent_given} = 'yes'"),
    (
        "selected(${multi_select_q}, 'option1') and ${another_condition}",
        "Feature: Conditionally showing - Example: selected(...) and ${...}",
    ),
    # From "Groups of questions (begin_group...end_group)" - relevant expression
    (
        "${display_personal_info_group} = 'yes'",
        "Feature: Groups - Relevant Expression Example",
    ),
    # From "Repeating questions (begin_repeat...end_repeat)" - relevant expression
    ("${ask_about_children} = 'yes'", "Feature: Repeats - Relevant Expression Example"),
    # From "Controlling the number of repetitions"
    ("3", "Feature: Controlling repetitions - Example: 3"),  # Covered by number literal
    (
        "${count_of_items}",
        "Feature: Controlling repetitions - Example: ${count_of_items}",
    ),
    (
        "if(${specify_count}='yes', ${user_defined_count}, 1)",
        "Feature: Controlling repetitions - Example: if(...)",
    ),
    (
        "count(${nodeset_question})",
        "Feature: Controlling repetitions - Example: count(${nodeset_question})",
    ),
    # From "Filtering options in select questions"
    (
        "country_column_in_choices = ${selected_country_value}",
        "Feature: Filtering options - Example: country_column... = ${...}",
    ),
    (
        "region_code = ../region_filter_question",
        "Feature: Filtering options - Example: region_code = ../...",
    ),
    (
        "age > 20 and gender = 'female'",
        "Feature: Filtering options - Example: age > 20 and gender = 'female'",
    ),  # Note: 'age', 'gender' here are like bare variables referring to choice attributes
    (
        "contains(additional_attribute_column, ${tag_filter})",
        "Feature: Filtering options - Example: contains(...)",
    ),
    # From "Generating select ones from repeats"
    (
        "instance('repeat_items_instance')/root/item[group_id = ${current_group_id}]/item_name",
        "Feature: Generating select from repeats - Example: instance(...)/...[...]/...",
    ),
    (
        "search('repeat_generated_csv', 'once', 'csv_value_col', ${lookup_value}, 'csv_label_col', ${lookup_value})",
        "Feature: Generating select from repeats - Example: search(...)",
    ),
    (
        "custom_filter_property_in_choices = /data/my_repeat[position() = current()/../index_for_repeat]/value_from_repeat",
        "Feature: Generating select from repeats - Example: custom_prop = /data/my_repeat[...]",
    ),
]


@pytest.mark.parametrize("expression, description", odk_expressions_to_validate)
def test_odk_expressions_do_not_error(expression, description):
    """
    Tests that ODK documentation expressions can be parsed without raising an error.
    The correctness of the AST is not checked in this stage.
    """
    try:
        parser.parse(expression)
        # If you want to log successful parsing, you can add a print statement here,
        # but it's generally not needed for passing tests.
        # print(f"Successfully parsed: {description} - Expression: {expression}")
    except Exception as e:
        pytest.fail(
            f"Parsing expression for '{description}' FAILED.\nExpression: {expression}\nError: {e}"
        )
