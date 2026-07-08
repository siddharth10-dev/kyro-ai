import json
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from core.llm import llm
from app.tools.logs_tool import get_logs
from app.tools.metrics_tool import get_metrics
from app.tools.deployment_tool import get_deployment_info
from app.tools.github_tool import get_latest_commit

class InvestigationAgent:

    def investigate(self, incident):
        tools = [get_logs, get_metrics, get_deployment_info, get_latest_commit]
        tools_map = {t.name: t for t in tools}

        llm_with_tools = llm.bind_tools(tools)

        system_prompt = """You are an Investigation Agent.
Your goal is to investigate production incidents by retrieving relevant data.
Use the tools available to you to get logs, metrics, deployment info, or github commits.
When you receive an incident, decide which tools are needed and call them.
Once you receive the tool execution results, compile the evidence and output ONLY a JSON object in this format:
{
  "logs": [list of logs],
  "metrics": {metrics dict},
  "deployment": {
    "latest_commit": "latest commit message"
  }
}
Do not output any markdown formatting (like ```json), commentary, or extra text. Return only the JSON object.
"""

        incident_str = f"Incident: service='{incident.service}', message='{incident.message}', severity='{incident.severity}'"
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=incident_str)
        ]

        res = llm_with_tools.invoke(messages)

        if res.tool_calls:
            messages.append(res)
            for tool_call in res.tool_calls:
                tool_func = tools_map[tool_call["name"]]
                tool_res = tool_func.invoke(tool_call["args"])
                messages.append(ToolMessage(content=json.dumps(tool_res), tool_call_id=tool_call["id"]))

            final_res = llm_with_tools.invoke(messages)
            content = final_res.content.strip()
        else:
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
                return {"raw_response": content}