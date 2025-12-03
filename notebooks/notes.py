from dataclasses import dataclass
from typing import List

# ------------------------------------------------------------
# Variable and Formula
# ------------------------------------------------------------

@dataclass
class Variable:
    """Represents a single variable appearing in a formula."""
    symbol: str       # should be plain: F, m, a
    description: str  # description with units
    units: str

@dataclass
class Formula:
    """A LaTeX formula with its associated variables."""
    formula_latex: str          # WITHOUT $$...$$ — class handles wrapping
    variables: List[Variable]

    def variables_to_markdown_table(self) -> str:
        """Returns a Markdown table of variable symbols and descriptions."""
        rows = [
            "| Symbol | Description | Units(SI) |",
            "|--------|-------------|-----------|",
        ]
        for v in self.variables:
            rows.append(f"| {v.symbol} | {v.description} | {v.units}|")
        return "\n".join(rows)

    def to_markdown(self) -> str:
        """Returns a Markdown block: formula + variable table."""
        return (
            "$$\n"
            f"{self.formula_latex}\n"
            "$$\n\n"
            f"{self.variables_to_markdown_table()}"
        )
