

import sys
from orchestrator.graph import WorkflowGraph, State
from agents.planner_agent import planner_node
from agents.writer_agent import writer_node
from agents.emovere_agent import emovere_node
from agents.editor_agent import editor_node
from agents.publisher_agent import publisher_node
from observability.logger import get_logger
from observability.metrics import metrics

logger = get_logger("Main")


def main():
    logger.info("Initializing Agentic Blog Writer System...")

    if len(sys.argv) < 2:
        topic = input("Enter a blog topic: ")
    else:
        topic = sys.argv[1]

    # 1. Initialize State
    initial_state = State(initial_input=topic)

    # 2. Build Graph
    workflow = WorkflowGraph()
    workflow.add_node("Planner", planner_node)
    workflow.add_node("Writer", writer_node)
    workflow.add_node("Emovere", emovere_node)
    workflow.add_node("Editor", editor_node)
    workflow.add_node("Publisher", publisher_node)

    # 3. Run Orchestration
    try:
        logger.info(f"Starting pipeline for topic: {topic}")
        final_state = workflow.run(initial_state)

        print("\n\n=== FINAL BLOG POST ===")
        print(final_state.final_output)
        print("=======================\n")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        print("Ensure LMStudio is running with model 'lfm2-vl-450m' at localhost:1234")

    # 4. Dump Metrics
    metrics.report()


if __name__ == "__main__":
    main()