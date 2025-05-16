from llm_parser import parse_rule_with_groq
from doc_extractor import DocumentExtractor
from datetime import datetime, timedelta

extractor = DocumentExtractor()

def parse_rule(rule_text):
    prompt = f"""
You are a rule parser.

Convert the following plain-English business rule into a valid JSON object using this exact schema:

{{
  "field": "<primary_field>",
  "target": "<reference_field>",      // optional, e.g., "approval_date"
  "operator": "<operator>",           // One of: ">", "<", ">=", "<=", "==", "!=", "within_last_days", "within_X_days"
  "value": <number or string or date>
}}

Rules:
- Use target if the condition is relative to another field.
- Output a single clean JSON object.
- No explanation or markdown.
- No ```json or other formatting.

Business rule: "{rule_text}"
"""
    return parse_rule_with_groq(prompt)

def extract_fields(file):
    filename = file.filename.lower()
    content = file.file.read()

    if filename.endswith(".pdf"):
        return extractor.extract_from_pdf(content)
    elif filename.endswith((".png", ".jpg", ".jpeg")):
        return extractor.extract_from_image(content)
    else:
        return {"fields": {}, "error": "Unsupported file type"}

def validate_data(data):
    fields = data.fields or {}
    rules = data.rules or []

    results = []
    passed = 0

    for rule in rules:
        try:
            field = rule["field"]
            operator = rule["operator"]
            expected_value = rule.get("value")
            target_field = rule.get("target")

            actual_value = fields.get(field)
            comparison_value = fields.get(target_field) if target_field else expected_value

            # Normalize dates
            if isinstance(actual_value, str) and is_date(actual_value):
                actual_value = parse_date(actual_value)
            if isinstance(comparison_value, str) and is_date(comparison_value):
                comparison_value = parse_date(comparison_value)

            # Normalize numbers (convert string digits to int or float)
            try:
                if isinstance(actual_value, str) and actual_value.replace('.', '', 1).isdigit():
                    actual_value = float(actual_value) if '.' in actual_value else int(actual_value)

                if isinstance(comparison_value, str) and comparison_value.replace('.', '', 1).isdigit():
                    comparison_value = float(comparison_value) if '.' in comparison_value else int(comparison_value)
            except Exception as e:
                raise ValueError(f"Failed to convert numeric strings: {e}")

            # Apply operator
            if evaluate(actual_value, operator, comparison_value):
                status = "PASS"
                passed += 1
            else:
                status = "FAIL"

            results.append({
                "rule": f"{field} {operator} {comparison_value}",
                "status": status,
                "actual": actual_value,
                "expected": comparison_value
            })

        except Exception as e:
            results.append({
                "rule": str(rule),
                "status": "ERROR",
                "actual": None,
                "expected": None,
                "error": str(e)
            })

    return {
        "results": results,
        "summary": {
            "total": len(rules),
            "passed": passed,
            "failed": len(rules) - passed
        }
    }

# Helper: Check if string is date
def is_date(value: str) -> bool:
    try:
        parse_date(value)
        return True
    except:
        return False

# Helper: Parse ISO / common date formats
def parse_date(date_str: str) -> datetime:
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(date_str, fmt)
        except:
            continue
    raise ValueError(f"Invalid date format: {date_str}")

# Helper: Evaluate rule
def evaluate(actual, op: str, expected) -> bool:
    if op == ">":
        return actual > expected
    elif op == "<":
        return actual < expected
    elif op == ">=":
        return actual >= expected
    elif op == "<=":
        return actual <= expected
    elif op == "==":
        return actual == expected
    elif op == "!=":
        return actual != expected
    elif op == "within_last_days":
        if not isinstance(actual, datetime):
            raise ValueError("Date expected for within_last_days")
        days = int(expected)
        return (datetime.now() - actual).days <= days
    elif op == "within_X_days":
        if not isinstance(actual, datetime) or not isinstance(expected, datetime):
            raise ValueError("Dates required for within_X_days")
        return abs((actual - expected).days) <= 30
    else:
        raise ValueError(f"Unsupported operator: {op}")
