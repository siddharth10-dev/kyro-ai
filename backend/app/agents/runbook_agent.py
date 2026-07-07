from app.tools.runbook_tool import search_runbook


class RunbookAgent:


    def retrieve(self, root_analysis):


        cause = root_analysis["root_cause"]


        runbook = search_runbook(cause)


        return {

            "matched_runbook":

            runbook["title"],


            "recommended_steps":

            runbook["steps"]

        }
