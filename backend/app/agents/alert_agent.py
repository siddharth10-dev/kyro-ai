from core.llm import llm, clean_content


class AlertAgent:


    def classify(self, incident):


        prompt = f"""

        You are an AI incident classification agent.


        Analyze this production alert:


        Service:
        {incident.service}


        Message:
        {incident.message}


        Severity:
        {incident.severity}


        Return ONLY JSON:

        {{
        "service":"",
        "category":"",
        "priority":"",
        "summary":""
        }}

        """


        response = llm.invoke(prompt)

        import json
        try:
            return json.loads(clean_content(response.content))
        except Exception:
            return {"raw_response": response.content}