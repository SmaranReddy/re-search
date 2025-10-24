# graph_state.py
from typing import List, Dict, TypedDict

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        user_query: The initial user query.
        keywords: Keywords extracted by the planner.
        papers: A list of paper dictionaries (title, abstract) from ArXiv.
        summaries: A list of summaries for each paper.
    """
    user_query: str
    keywords: str
    papers: List[Dict[str, str]]
    summaries: List[str]