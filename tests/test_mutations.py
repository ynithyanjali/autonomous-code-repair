import ast
import unittest
from repair_agent.mutations import generate_mutations


class MutationTests(unittest.TestCase):
    def test_subtraction_candidate_to_addition(self):
        candidates = generate_mutations("def f(a, b):\n    return a - b\n")
        self.assertTrue(any("return a + b" in c.code for c in candidates))

    def test_all_generated_code_parses(self):
        candidates = generate_mutations("def f(a, b):\n    return a != b\n")
        self.assertTrue(candidates)
        for candidate in candidates:
            ast.parse(candidate.code)

    def test_no_mutations_for_constant(self):
        self.assertEqual(generate_mutations("x = 5\n"), [])


if __name__ == "__main__":
    unittest.main()
