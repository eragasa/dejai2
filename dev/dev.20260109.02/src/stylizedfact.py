from __future__ import annotations

from datetime import date
from typing import List, Literal
from pydantic import BaseModel, Field, ConfigDict
from dataclasses import dataclass

def _norm(s: str) -> str:
  """normalize text"""
  return (s or "").strip().replace("\r\n", "\n")


# User-editable single-string template (keep it obvious + local)
STYLIZED_FACT_MD = """
##### {key} - {title}
- `statement`:{statement}
- `description`: {description}
- `claim`: {claim}
""".strip()


class StylizedFact(BaseModel):
  """
  A stylized fact is an observed regularity + an analyzed, falsifiable claim.

  Fields are intentionally minimal and schema-stable.
  """
  model_config = ConfigDict(extra="forbid")

  key: str = Field(
      ..., 
      description="Stable identifier, e.g. 'SF-1'")
  title: str = Field(
      ..., 
      description="Short human label")
  statement: str = Field(
      ...,
      description="Observable property")
  description: str = Field(
      ..., 
      description="How it manifests in practice")
  claim: str = Field(
     ..., 
     description="Falsifiable proposition derived from the fact")


def _norm(s: str) -> str:
    # Conservative normalization for embedding in Markdown
    return (s or "").strip().replace("\r\n", "\n")

@dataclass(frozen=True)
class StylizedFactsRenderer:
  """
  Pure renderer for StylizedFactsDoc -> Markdown atoms.

  - No mutation of the doc
  - No parsing of Markdown back into objects
  - Formatting is controlled by a single user-editable format string
  """
  pydantic_obj: StylizedFact
  template: str = STYLIZED_FACT_MD

  def to_md(self, f: "StylizedFact") -> str:
    return (
      self.atom_format.format(
        key=_norm(f.key),
        title=_norm(f.title),
        statement=_norm(f.statement),
        description=_norm(f.description),
        claim=_norm(f.claim),
      ).rstrip()
      + "\n"
    )
