
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
import os
import uuid
import asyncio
import logging
from typing import Any, Dict

from crewai import Crew, Process
from agents import financial_analyst, verifier
from task import analyze_financial_document

app = FastAPI(title="Financial Document Analyzer")

logger = logging.getLogger("uvicorn.error")

def run_crew_sync(query: str, file_path: str = "data/sample.pdf") -> Dict[str, Any]:
    financial_crew = Crew(
        agents=[financial_analyst],
        tasks=[analyze_financial_document],
        process=Process.sequential,
    )
    payload = {"query": query, "file_path": file_path}
    result = financial_crew.kickoff(payload)
    return result

@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):

    if not file.filename.lower().endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Only PDF or TXT uploads allowed.")

    file_id = str(uuid.uuid4())
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir, f"financial_document_{file_id}.pdf")

    try:

        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, run_crew_sync, query.strip(), file_path)

        return {
            "status": "success",
            "query": query,
            "analysis": response,
            "file_processed": file.filename
        }
    except Exception as e:
        logger.exception("Error processing document")
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
    finally:

        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            logger.warning("Failed to cleanup uploaded file", exc_info=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), reload=True)
