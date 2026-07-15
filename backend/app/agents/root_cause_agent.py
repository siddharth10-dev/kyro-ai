import json
from core.llm import llm, clean_content
from langchain_core.messages import SystemMessage, HumanMessage

class RootCauseAgent:

    def analyze(self, incident, investigation):
        system_prompt = """You are a Root Cause Analysis Agent.
Analyze the production incident using the provided incident details and investigation evidence (logs, metrics, deployments).
Determine what actually failed.
Output your analysis ONLY as a JSON object with this format:
{
  "root_cause": "brief explanation of what failed and why",
  "confidence": 0.0 to 1.0,
  "reasoning": [
    "reasoning step 1",
    "reasoning step 2"
  ]
}
Do not output any markdown formatting (like ```json), commentary, or extra text. Return only the JSON object.
"""

        incident_data = {
            "service": incident.service,
            "message": incident.message,
            "severity": incident.severity
        }

        evidence = {
            "logs": investigation.get("logs", []),
            "metrics": investigation.get("metrics", {}),
            "deployment": investigation.get("deployment", {})
        }

        user_content = f"Incident Details:\n{json.dumps(incident_data, indent=2)}\n\nEvidence:\n{json.dumps(evidence, indent=2)}"

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_content)
        ]

        res = llm.invoke(messages)
        content = clean_content(res.content)

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
                return {"raw_response": content}