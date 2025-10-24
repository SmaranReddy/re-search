from .agents.planner_agent import PlannerAgent
from .agents.retriever_agent import RetrieverAgent
from .agents.summarizer_agent import SummarizerAgent
from .graph_state import GraphState
from langgraph.graph import StateGraph, END

# --- 1. Instantiate Agents ---
planner = PlannerAgent()
retriever = RetrieverAgent()
summarizer = SummarizerAgent()

# --- 2. Define Graph Node Functions ---

def run_planner(state: GraphState):
    """Node to extract keywords from the user query."""
    print("--- 🧠 RUNNING PLANNER ---")
    user_query = state['user_query']
    keywords = planner.plan(user_query)
    return {"keywords": keywords}

def run_retriever(state: GraphState):
    """Node to retrieve papers from ArXiv."""
    print("--- 📚 RUNNING RETRIEVER ---")
    keywords = state['keywords']
    papers = retriever.search_papers(keywords)
    
    print(f"DEBUG: Found {len(papers)} papers.")
    if papers:
        print("--- DEBUG: ALL RETRIEVED PAPERS ---")
        for i, paper in enumerate(papers):
            print(f"  {i+1}: {paper['title']}")
        print("-----------------------------------")
    else:
        print("DEBUG: No papers found")
        
    return {"papers": papers}

def run_summarizer(state: GraphState):
    """Node to summarize each paper's abstract."""
    print("--- ✍️ RUNNING SUMMARIZER ---")
    papers = state['papers']
    summaries = []
    for i, paper in enumerate(papers):
        print(f"DEBUG: Summarizing paper {i+1} ('{paper['title']}')")
        summary = summarizer.summarize(paper['abstract'])
        summaries.append(summary)
    print("--- Summarization Complete ---")
    return {"summaries": summaries}

# --- 3. Build and Compile the Graph (at top level) ---
workflow = StateGraph(GraphState)

workflow.add_node("planner", run_planner)
workflow.add_node("retriever", run_retriever)
workflow.add_node("summarizer", run_summarizer)

workflow.set_entry_point("planner")
workflow.add_edge("planner", "retriever")
workflow.add_edge("retriever", "summarizer")
workflow.add_edge("summarizer", END)

# Compile the graph into a runnable app
app = workflow.compile()

# --- 4. Define an Importable Function for Streamlit ---
def run_graph(user_query: str) -> dict:
    """
    Runs the compiled LangGraph app with a user query
    and returns the final state.
    """
    inputs = {"user_query": user_query}
    # .invoke() runs the graph and returns the final state
    final_state = app.invoke(inputs)
    return final_state

# --- 5. Main execution block (for testing) ---
# This part only runs if you execute main.py directly
if __name__ == "__main__":
    query = input("Enter your research topic: ")
    
    final_state = run_graph(query)
    
    print("\n--- ✅ FINAL SUMMARIES ---")
    if final_state.get('summaries'):
        for i, summary in enumerate(final_state['summaries']):
            paper_title = final_state['papers'][i]['title']
            print(f"\n--- Summary for: '{paper_title}' ---")
            print(summary)
    else:
        print("No summaries could be generated.")