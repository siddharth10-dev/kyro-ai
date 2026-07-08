from langgraph.graph import StateGraph, END

from graph.state import IncidentState


from app.agents.alert_agent import AlertAgent
from app.agents.investigen import InvestigationAgent
from app.agents.root_cause_agent import RootCauseAgent
from app.agents.runbook_agent import RunbookAgent
from app.agents.recommendation_agent import RecommendationAgent

alert_agent = AlertAgent()

investigation_agent = InvestigationAgent()

root_agent = RootCauseAgent()

runbook_agent = RunbookAgent()

recommendation_agent = RecommendationAgent()

def alert_node(state):
    print("🚨 ALERT NODE RUNNING")

    result = alert_agent.classify(
        state["incident"]
    )

    return {
        "classification": result
    }

def investigation_node(state):
    print("🔍 INVESTIGATION NODE RUNNING")

    result = investigation_agent.investigate(
        state["incident"]
    )


    return {
        "investigation": result
    }

def root_cause_node(state):
    print("🧠 ROOT CAUSE NODE RUNNING")

    result = root_agent.analyze(
        state["incident"],
        state["investigation"]
    )


    return {
        "root_cause": result
    }

def runbook_node(state):
    print("📚 RUNBOOK NODE RUNNING")

    result = runbook_agent.retrieve(
        state["root_cause"]
    )


    return {
        "runbook": result
    }


def recommendation_node(state):
    print("⚡ RECOMMENDATION NODE RUNNING")

    result = recommendation_agent.recommend(
        state["root_cause"],
        state["runbook"],
        state["investigation"]
    )


    return {
        "recommendation": result
    }



def create_incident_workflow():

    workflow = StateGraph(IncidentState)


    workflow.add_node("alert_node", alert_node)

    workflow.add_node("investigation_node", investigation_node)

    workflow.add_node("root_cause_node", root_cause_node)

    workflow.add_node("runbook_node", runbook_node)

    workflow.add_node("recommendation_node", recommendation_node)


    workflow.set_entry_point("alert_node")

    workflow.add_edge("alert_node", "investigation_node")

    workflow.add_edge("investigation_node", "root_cause_node")

    workflow.add_edge("root_cause_node", "runbook_node")

    workflow.add_edge("runbook_node", "recommendation_node")

    workflow.add_edge("recommendation_node", END)


    return workflow.compile()
    

sentinel_graph = create_incident_workflow()



