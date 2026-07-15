import os
import json
import logging
from core.llm import llm, clean_content
from app.utils.vector_store import RunbookVectorStore

logger = logging.getLogger(__name__)

class RunbookAgent:
    def __init__(self):
        self.vector_store = RunbookVectorStore()

    def retrieve(self, root_analysis: dict, investigation_data: dict = None) -> dict:
        cause = root_analysis.get("root_cause", "")
        evidence = json.dumps(investigation_data) if investigation_data else ""
        
        # Query the vector store for the single most relevant runbook
        query = f"Root Cause: {cause}\nEvidence: {evidence}"
        logger.info(f"Searching similar runbooks for query...")
        similar_docs = self.vector_store.search_similar(query, top_k=1)
        
        if similar_docs:
            matched_filename = similar_docs[0]["filename"]
            matched_content = similar_docs[0]["content"]
            logger.info(f"Retrieved runbook: {matched_filename} (Similarity: {similar_docs[0]['similarity']:.4f})")
        else:
            matched_filename = "Unknown"
            matched_content = "No runbooks matched this issue."
            logger.warning("No matching runbook found in vector store.")

        system_prompt = """You are a Runbook Retrieval-Augmented Generation (RAG) Agent.
Your goal is to inspect the Root Cause Analysis, system evidence, and the matched runbook retrieved from the vector database, and return the runbook title and recovery steps.

Here is the matched runbook retrieved from the vector database:
--- RUNBOOK FILE: {filename} ---
{content}

Based on the root cause, evidence, and this runbook, format and return the recovery steps.
Return ONLY a JSON object in this format:
{{
  "matched_runbook": "Runbook Title",
  "recommended_steps": [
    "step 1 from the selected runbook",
    "step 2 from the selected runbook",
    ...
  ]
}}

Do not include any explanation, markdown formatting (like ```json), or extra text outside the JSON. Return only the JSON object.
"""

        prompt = f"""
Root Cause: {cause}
System Evidence: {evidence}
"""

        response = llm.invoke([
            ("system", system_prompt.format(filename=matched_filename, content=matched_content)),
            ("human", prompt)
        ])

        content = clean_content(response.content)
        try:
            return json.loads(content)
        except Exception:
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            try:
                return json.loads(content)
            except Exception:
                return {
                    "matched_runbook": matched_filename.replace(".md", "").replace("_", " ").title(),
                    "recommended_steps": [
                        "Investigate system logs",
                        "Verify metric thresholds"
                    ],
                    "raw_response": content
                }

