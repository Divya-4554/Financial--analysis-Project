
import os
from dotenv import load_dotenv
load_dotenv()
from typing import Optional
import typing
import io


try:
    from PyPDF2 import PdfReader
except Exception:
    PdfReader = None

class FinancialDocumentTool:
    """Tool to read data from a PDF path and return cleaned text."""

    @staticmethod
    def read_data(path: str = "data/sample.pdf") -> str:
        if not os.path.exists(path):
            raise FileNotFoundError(f"PDF not found: {path}")


        if PdfReader:
            reader = PdfReader(path)
            pages = []
            for p in reader.pages:
                text = p.extract_text() or ""

                text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
                pages.append(text)
            return "\n\n".join(pages)
        else:

            with open(path, "rb") as f:
                return f"UNABLE_TO_EXTRACT_TEXT: installed parser missing. file size: {os.path.getsize(path)}"

class InvestmentTool:
    """Investment analysis helper (stub)."""

    @staticmethod
    def analyze_investment(financial_document_data: str) -> dict:

        import re
        nums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", financial_document_data)]
        summary = {
            "num_count": len(nums),
            "min": min(nums) if nums else None,
            "max": max(nums) if nums else None,
            "mean": (sum(nums) / len(nums)) if nums else None
        }

        return {"summary": summary, "note": "Use a proper financial model for production."}

class RiskTool:
    @staticmethod
    def create_risk_assessment(financial_document_data: str) -> dict:

        return {"risk_score": 0.5, "detail": "Placeholder risk assessment; implement model."}
