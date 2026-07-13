import json
import datetime
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from core.llm import llm
from app.tools.logs_tool import get_logs
from app.tools.metrics_tool import get_metrics
from app.tools.deployment_tool import get_deployment_info
from app.tools.github_tool import get_latest_commit

class InvestigationAgent:

    def investigate(self, incident, timeline: list) -> dict:
        tools = [get_logs, get_metrics, get_deployment_info, get_latest_commit]
        tools_map = {t.name: t for t in tools}

        llm_with_tools = llm.bind_tools(tools)

        system_prompt = """You are an Investigation Agent.
Your goal is to investigate production incidents by retrieving relevant data (logs, metrics, git commits, and deployment info).

You operate in a loop. At each step, analyze the current messages and determine:
1. If you need more information, call the appropriate tool(s).
2. If you already have enough evidence or no more tools will help, do NOT call any tools. Instead, construct a final JSON summary.

When compiling your final summary, return ONLY a JSON object in this format:
{
  "logs": [list of logs],
  "metrics": {metrics dict},
  "deployment": {
    "latest_commit": "latest commit message"
  }
}

Do not include any explanation, markdown blocks (like ```json), or extra text outside the JSON. Return only the JSON object.
"""

        incident_str = f"Incident: service='{incident.service}', message='{incident.message}', severity='{incident.severity}'"
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=incident_str)
        ]

        max_iterations = 5
        content = ""
        
        for iteration in range(max_iterations):
            res = llm_with_tools.invoke(messages)
            messages.append(res)

            if res.tool_calls:
                for tool_call in res.tool_calls:
                    tool_name = tool_call["name"]
                    tool_args = tool_call["args"]
                    
                    # Update timeline
                    time_str = datetime.datetime.now().strftime("%H:%M")
                    if tool_name == "get_logs":
                        timeline.append(f"{time_str} Logs collected")
                    elif tool_name == "get_metrics":
                        timeline.append(f"{time_str} Metrics collected")
                    elif tool_name in ("get_deployment_info", "get_latest_commit"):
                        timeline.append(f"{time_str} Deployment checked")
                    
                    # Execute tool
                    if tool_name in tools_map:
                        tool_func = tools_map[tool_name]
                        try:
                            tool_res = tool_func.invoke(tool_args)
                        except Exception as e:
                            tool_res = f"Error: {str(e)}"
                    else:
                        tool_res = f"Tool {tool_name} not found"

                    messages.append(ToolMessage(content=json.dumps(tool_res), tool_call_id=tool_call["id"]))
            else:
                # LLM chose not to call any tools; it has finished its analysis.
                content = res.content.strip()
                break
        
        if not content and len(messages) > 0:
            content = messages[-1].content.strip()

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