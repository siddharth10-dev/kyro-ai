import json
import logging
from core.llm import llm
from langchain_core.messages import SystemMessage, HumanMessage

logger = logging.getLogger(__name__)

class CommunicationAgent:
    def generate_reports(self, incident_data: dict) -> dict:
        service = incident_data.get("service", "unknown-service")
        message = incident_data.get("message", "")
        root_cause = incident_data.get("root_cause", {})
        recommendation = incident_data.get("recommendation", {})
        timeline = incident_data.get("timeline", [])
        
        system_prompt = """You are a professional SRE Communication Agent.
Your job is to generate three communication artifacts based on the provided incident investigation data:
1. An Incident Report (post-mortem) in a standard developer format (formatted as markdown). It must start with a generated incident ID like INC-XXX (e.g. INC-102), followed by: Root Cause, Impact, Resolution, and Next Steps.
2. An Executive Summary: A high-level, business-friendly explanation of what happened, the business impact, and how it was resolved, written in clear and concise non-technical language.
3. A Slack Message: A brief, beautifully formatted message for a Slack support/engineering channel that alerts the team of the resolution. Use emojis (e.g., ✅, 🚨) and summarize ID, Service, Root Cause, and Actions Taken.

Output your response ONLY as a JSON object with this format:
{
  "incident_report": "markdown string of the dev post-mortem report",
  "executive_summary": "concise business summary string",
  "slack_message": "slack formatted message string"
}
Do not include any explanation, markdown formatting (like ```json), or extra text outside the JSON. Return only the JSON object.
"""

        user_content = f"""
Incident Metadata:
- Service: {service}
- Message: {message}

Root Cause Analysis:
{json.dumps(root_cause, indent=2)}

Recommendation / Resolution:
{json.dumps(recommendation, indent=2)}

Timeline of events:
{json.dumps(timeline, indent=2)}
"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_content)
        ]

        logger.info("Generating communication reports using LLM...")
        res = llm.invoke(messages)
        content = res.content.strip()

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
                # Fallback format if parsing fails
                return {
                    "incident_report": f"# INC-100: Incident Report for {service}\\n\\n**Root Cause**: {root_cause.get('root_cause', 'Unknown')}\\n\\n**Impact**: {recommendation.get('impact', 'Unknown')}",
                    "executive_summary": f"The {service} service experienced an issue: '{message}'. The root cause was: {root_cause.get('root_cause', 'Unknown')}. It was successfully resolved.",
                    "slack_message": f"✅ *INC-100 Resolved* | *Service*: {service}\\n*Root Cause*: {root_cause.get('root_cause', 'Unknown')}\\n*Resolution*: Recommended actions have been approved.",
                    "raw_response": content
                }
