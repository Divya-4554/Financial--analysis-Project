# task.py
from crewai import Task
from agents import financial_analyst, verifier
from tools import FinancialDocumentTool, InvestmentTool, RiskTool

analyze_financial_document = Task(
    description="Extract facts from the document and produce a concise, evidence-based analysis. Use FinancialDocumentTool.read_data and return structured JSON.",
    expected_output="""{
        "document_text": "<extracted text fragment>",
        "key_metrics": {"revenue": "...", "net_income": "..."},
        "investment_insight": "<neutral, non-regulatory observations>",
        "confidence": 0.0
    }""",
    agent=financial_analyst,
    tools=[FinancialDocumentTool, InvestmentTool, RiskTool],
    async_execution=False
)
