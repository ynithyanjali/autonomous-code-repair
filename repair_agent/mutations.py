"""Generate small, explainable Python operator-repair candidates.

Scope is deliberately narrow: only one AST operator changes per candidate.
This is not an LLM or a general-purpose bug repair system.
"""

import ast
from dataclasses import dataclass


@dataclass(frozen=True)
class Mutation:
    line: int
    column: int
    original: str
    replacement: str
    code: str


OPERATORS = {
    ast.Add: [ast.Sub],
    ast.Sub: [ast.Add],
    ast.Mult: [ast.Add],
    ast.Eq: [ast.NotEq],
    ast.NotEq: [ast.Eq],
}


class _ChangeOneOperator(ast.NodeTransformer):
    def __init__(self, position, old_type, new_type):
        self.position = position
        self.old_type = old_type
        self.new_type = new_type
        self.changed = False

    def visit_BinOp(self, node):
        self.generic_visit(node)
        if (not self.changed and (node.lineno, node.col_offset) == self.position
                and isinstance(node.op, self.old_type)):
            node.op = self.new_type()
            self.changed = True
        return node

    def visit_Compare(self, node):
        self.generic_visit(node)
        if (not self.changed and len(node.ops) == 1
                and (node.lineno, node.col_offset) == self.position
                and isinstance(node.ops[0], self.old_type)):
            node.ops[0] = self.new_type()
            self.changed = True
        return node


def generate_mutations(source: str, max_candidates: int = 20) -> list[Mutation]:
    """Return candidate modules with one operator swapped in each."""
    tree = ast.parse(source)
    sites = []
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp):
            sites.append(((node.lineno, node.col_offset), type(node.op)))
        elif isinstance(node, ast.Compare) and len(node.ops) == 1:
            sites.append(((node.lineno, node.col_offset), type(node.ops[0])))

    results = []
    for position, original_type in sites:
        for replacement_type in OPERATORS.get(original_type, []):
            copied = ast.parse(source)
            changer = _ChangeOneOperator(position, original_type, replacement_type)
            changed_tree = changer.visit(copied)
            if not changer.changed:
                continue
            ast.fix_missing_locations(changed_tree)
            new_source = ast.unparse(changed_tree) + "\n"
            results.append(Mutation(
                line=position[0],
                column=position[1],
                original=original_type.__name__,
                replacement=replacement_type.__name__,
                code=new_source,
            ))
            if len(results) >= max_candidates:
                return results
    return results
