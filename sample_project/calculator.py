"""Small synthetic example with an intentionally incorrect operator."""


def calculate_total(subtotal, tax):
    """Return subtotal plus tax."""
    return subtotal - tax  # Deliberate demo bug: should add tax.
