import datetime
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

def get_time_str():
    return datetime.datetime.now().strftime("%H:%M")

def alert_node(state):
    print("🚨 ALERT NODE RUNNING")
    timeline = list(state.get("timeline", []))
    time_str = get_time_str()
    timeline.append(f"{time_str} Alert received")
    
    result = alert_agent.classify(
        state["incident"]
    )
    
    timeline.append(f"{time_str} Alert classified")
    return {
        "classification": result,
        "timeline": timeline
    }

def investigation_node(state):
    print("🔍 INVESTIGATION NODE RUNNING")
    timeline = list(state.get("timeline", []))
    time_str = get_time_str()
    timeline.append(f"{time_str} Investigation started")
    
    result = investigation_agent.investigate(
        state["incident"],
        timeline
    )
    
    time_str = get_time_str()
    timeline.append(f"{time_str} Investigation complete")
    return {
        "investigation": result,
        "timeline": timeline
    }

def root_cause_node(state):
    print("🧠 ROOT CAUSE NODE RUNNING")
    timeline = list(state.get("timeline", []))
    time_str = get_time_str()
    timeline.append(f"{time_str} Root cause analysis started")
    
    result = root_agent.analyze(
        state["incident"],
        state["investigation"]
    )
    
    time_str = get_time_str()
    timeline.append(f"{time_str} Root cause generated")
    return {
        "root_cause": result,
        "timeline": timeline
    }

def runbook_node(state):
    print("📚 RUNBOOK NODE RUNNING")
    timeline = list(state.get("timeline", []))
    time_str = get_time_str()
    timeline.append(f"{time_str} Searching runbooks")
    
    result = runbook_agent.retrieve(
        state["root_cause"],
        state["investigation"]
    )
    
    time_str = get_time_str()
    timeline.append(f"{time_str} Runbook retrieved")
    return {
        "runbook": result,
        "timeline": timeline
    }

def recommendation_node(state):
    print("⚡ RECOMMENDATION NODE RUNNING")
    timeline = list(state.get("timeline", []))
    time_str = get_time_str()
    timeline.append(f"{time_str} Generating recommendations")
    
    result = recommendation_agent.recommend(
        state["root_cause"],
        state["runbook"],
        state["investigation"]
    )
    
    time_str = get_time_str()
    timeline.append(f"{time_str} Recommendation created")
    return {
        "recommendation": result,
        "timeline": timeline
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
    

kyro_graph = create_incident_workflow()



