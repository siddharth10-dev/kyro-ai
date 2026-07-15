import json
from core.llm import llm, clean_content
from langchain_core.messages import SystemMessage, HumanMessage

class RecommendationAgent:

    def recommend(self, root_cause, runbook, evidence):
        system_prompt = """You are a Recommendation Agent.
Given the Root Cause Analysis, standard Runbook steps, and the gathered Evidence (logs, metrics, deployment details), generate a recovery plan.
Analyze the impact of the issue and prescribe actions to recover.
Output your recovery plan ONLY as a JSON object with this format:
{
  "impact": "detailed explanation of the impact",
  "actions": [
    "action 1",
    "action 2",
    "action 3"
  ],
  "risk": "low" | "medium" | "high"
}
Do not output any markdown formatting (like ```json), commentary, or extra text. Return only the JSON object.
"""

        user_content = f"Root Cause Analysis:\n{json.dumps(root_cause, indent=2)}\n\nMatched Runbook:\n{json.dumps(runbook, indent=2)}\n\nEvidence:\n{json.dumps(evidence, indent=2)}"

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