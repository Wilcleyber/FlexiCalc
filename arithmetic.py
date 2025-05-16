import re
import math
import ast

def evaluate_expression(expr: str) -> float:
    expr = expr.replace('×', '*').replace('÷', '/')

    if not any(c.isdigit() for c in expr):
        raise ValueError("Invalid expression")

    expr = convert_percentage_expressions(expr)

    try:
        tree = ast.parse(expr, mode='eval')

        allowed_types = (
            ast.Expression, ast.BinOp, ast.UnaryOp,
            ast.Constant, ast.Call, ast.Name, ast.Load,
            ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod,
            ast.USub, ast.UAdd
        )

        for node in ast.walk(tree):
            if not isinstance(node, allowed_types):
                raise ValueError("Invalid expression")

        return eval(compile(tree, filename="<ast>", mode="eval"), {"__builtins__": None}, {})
    except Exception as e:
        raise ValueError(f"Error in expression: {e}")

def convert_percentage_expressions(expr: str) -> str:
    pattern = r'(\d+(?:\.\d+)?)(\s*[\+\-])\s*(\d+(?:\.\d+)?)%'

    def replacer(match):
        base = match.group(1)
        operator = match.group(2)
        percentage = match.group(3)
        return f"{base}{operator}({base}*{percentage}/100)"

    return re.sub(pattern, replacer, expr)

def square(value: float) -> float:
    return value ** 2

def square_root(value: float) -> float:
    if value < 0:
        raise ValueError("Cannot extract root of negative number.")
    return math.sqrt(value)

def percentage(value: float) -> float:
    return value / 100


                        
