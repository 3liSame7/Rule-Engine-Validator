from langchain_core.prompts import PromptTemplate
import pytesseract
from PIL import Image
import io
import fitz  # PyMuPDF
import os
import json
import re
import openai  # Groq-compatible OpenAI client

class DocumentExtractor:
    def __init__(self):
        self.client = openai.OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.model = "llama3-8b-8192"

        self.prompt_template = PromptTemplate(
            input_variables=["text"],
            template="""
You are a document data extractor. Extract the following fields from the input text:

- invoice_total
- invoice_date
- payment_date
- approval_date
- contract_date

Respond ONLY with valid JSON (no markdown, no comments).

Text:
{text}
"""
        )

    def extract_from_pdf(self, file_bytes: bytes) -> dict:
        pdf = fitz.open(stream=file_bytes, filetype="pdf")
        text = "".join([page.get_text() for page in pdf])
        if not text.strip():
            raise ValueError("PDF text extraction failed or returned empty.")
        return self._extract_fields_via_llm(text)

    def extract_from_image(self, file_bytes: bytes) -> dict:
        image = Image.open(io.BytesIO(file_bytes))
        text = pytesseract.image_to_string(image)
        if not text.strip():
            raise ValueError("OCR failed or returned empty text.")
        return self._extract_fields_via_llm(text)

    def _extract_fields_via_llm(self, raw_text: str) -> dict:
        prompt = self.prompt_template.format(text=raw_text)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=512
            )
            output = response.choices[0].message.content.strip()

            if output.startswith("```json"):
                output = output[7:].strip()
            elif output.startswith("```"):
                output = output[3:].strip()
            if output.endswith("```"):
                output = output[:-3].strip()

            match = re.search(r'{[\s\S]+}', output)
            if not match:
                raise ValueError("No valid JSON found in LLM output.")

            parsed = json.loads(match.group(0))
            return {"fields": parsed}

        except Exception as e:
            return {"fields": {}, "error": f"LLM parsing failed: {str(e)}"}