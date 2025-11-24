from typing import Dict, Any, List, Callable

class State:
    """Shared state object passed between agents."""
    def __init__(self, initial_input: str):
        self.initial_input = initial_input
        self.plan = None
        self.draft_sections = {}
        self.full_draft = ""
        self.emotional_draft = ""
        self.final_output = ""
        self.feedback = []
        self.metadata = {}

class WorkflowGraph:
    """Simple Directed Acyclic Graph (DAG) implementation."""
    def __init__(self):
        self.nodes = {}
        self.sequence = []

    def add_node(self, name: str, func: Callable):
        self.nodes[name] = func
        self.sequence.append(name)

    def run(self, state: State):
        current_state = state
        for node_name in self.sequence:
            print(f"\n--- ⏩ Running Node: {node_name} ---")
            func = self.nodes[node_name]
            current_state = func(current_state)
        return current_state