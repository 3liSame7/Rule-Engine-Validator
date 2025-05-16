from pydantic import BaseModel
from typing import List, Optional, Any

class RuleInput(BaseModel):
    rule_text: str

class FieldData(BaseModel):
    fields: dict
    rules: Optional[List[dict]] = []

class ValidationResult(BaseModel):
    rule: str
    status: str
    actual: Optional[Any] = None
    expected: Optional[str] = None

class ValidationSummary(BaseModel):
    total: int
    passed: int
    failed: int

class ValidationResponse(BaseModel):
    results: List[ValidationResult]
    summary: ValidationSummary
