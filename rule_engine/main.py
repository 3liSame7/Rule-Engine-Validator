from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from schemas import RuleInput, FieldData
from logic import parse_rule, extract_fields, validate_data

app = FastAPI()


# ✅ Custom handler for 422 errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Invalid input. Please make sure your request follows the correct format.\n\n"
                      "- `fields` must be a JSON object (dict).\n"
                      "- `rules` must be a **list** of rule objects like:\n"
                      '  [{"field": "invoice_total", "operator": ">", "value": 1000}].'
        },
    )


# ✅ Rule parsing endpoint
@app.post("/parse-rule")
def parse(rule: RuleInput):
    if not rule.rule_text.strip():
        raise HTTPException(status_code=400, detail="Empty rule text.")
    try:
        return parse_rule(rule.rule_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM API Error: {str(e)}")


# ✅ Document field extraction endpoint
@app.post("/extract")
def extract(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded.")
    try:
        return extract_fields(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")


# ✅ Rule validation endpoint
@app.post("/validate")
def validate(data: FieldData):
    try:
        return validate_data(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")


# ✅ Health check endpoint
@app.get("/health")
def health():
    return {"status": "OK"}
