class RecommendationAgent:


    def recommend(
            self,
            root_cause,
            runbook
        ):


        confidence = (
            root_cause["confidence"]
        )


        if confidence > 0.85:

            risk = "LOW"

        elif confidence > 0.60:

            risk = "MEDIUM"

        else:

            risk = "HIGH"



        return {


            "summary":

            f"""
            Issue detected:
            {root_cause['root_cause']}
            """,



            "action_plan":

            runbook[
                "recommended_steps"
            ],



            "risk":

            risk,


            "requires_approval":

            True
        }