from typing import Literal, TypeAlias, TypedDict


class NumberLiteralNode(TypedDict):
    type: Literal["number_literal"]
    value: float


class StringLiteralNode(TypedDict):
    type: Literal["string_literal"]
    value: str


class VariableRefNode(TypedDict):
    type: Literal["variable_ref"]
    name: str


class BareVariableRefNode(TypedDict):
    type: Literal["bare_variable_ref"]
    name: str


class CurrentRefNode(TypedDict):
    type: Literal["current_ref"]


class ParentRefNode(TypedDict):
    type: Literal["parent_ref"]


class UnaryOpNode(TypedDict):
    type: Literal["unary_op"]
    operator: Literal["unary_minus"]
    operand: "AnyASTNode"


class BinaryOpNode(TypedDict):
    type: Literal["binary_op"]
    operator: Literal[
        "add",
        "subtract",
        "multiply",
        "divide",
        "eq",
        "ne",
        "lt",
        "gt",
        "lte",
        "gte",
        "or",
        "and",
    ]
    left: "AnyASTNode"
    right: "AnyASTNode"


class FunctionCallNode(TypedDict):
    type: Literal["function_call"]
    name: str
    arguments: list["AnyASTNode"]


AnyASTNode: TypeAlias = (
    NumberLiteralNode
    | StringLiteralNode
    | VariableRefNode
    | BareVariableRefNode
    | CurrentRefNode
    | ParentRefNode
    | UnaryOpNode
    | BinaryOpNode
    | FunctionCallNode
)

ExpressionAST: TypeAlias = AnyASTNode
