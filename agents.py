
import os
from dotenv import load_dotenv
load_dotenv()

from crewai.agents import Agent  # adjust import to match crewai SDK in your env
# Import the cleaned tools
from tools import FinancialDocumentTool, InvestmentTool, RiskTool

# Initialize llm - placeholder. Configure from env, e.g. CREWAI_API_KEY or other.
# The exact LLM init depends on CrewAI SDK. Replace with correct factory call.
llm = None
try:
    # Example (pseudocode) - replace with your actual CrewAI LLM creation code:
    # from crewai import LLM
    # llm = LLM(api_key=os.environ["CREWAI_API_KEY"])
    pass
except Exception:
    llm = None


financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Carefully extract factual information from the supplied financial document and produce evidence-based analysis. Do not fabricate facts.",
    verbose=False,
    memory=False,
    backstory="Expert in accounting and financial modelling. Prioritize accuracy, cite document sections and avoid investment advice that would be considered regulated advice.",
    tools=[FinancialDocumentTool, InvestmentTool, RiskTool],
    llm=llm,
    max_iter=3,
    max_rpm=60,
    allow_delegation=False
)


verifier = Agent(
    role="Document Verifier",
    goal="Confirm whether the uploaded file contains verifiable financial content; if uncertain, state limitations.",
    verbose=False,
    memory=False,
    backstory="Focus on file type detection and confidence scoring.",
    llm=llm,
    max_iter=1
)
