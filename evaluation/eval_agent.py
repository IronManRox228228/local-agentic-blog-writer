import json
from agents.base_llm import call_llm
from observability.logger import get_logger

logger = get_logger("Evaluator")


def evaluate_output(topic, generated_text, expected_tone):
    prompt = f"""
    You are an AI Judge.
    Original Topic: {topic}
    Expected Tone: {expected_tone}

    Generated Text:
    {generated_text[:1000]}...

    Rate this text on a scale of 1-5 for:
    1. Clarity
    2. Tone Match ({expected_tone})

    Format: "Clarity: X, Tone: Y"
    """

    result = call_llm([{"role": "user", "content": prompt}], agent_role="editor")  # Reusing editor config
    logger.info(f"Evaluation Result for '{topic}': {result}")
    return result


if __name__ == "__main__":
    # Example manual run
    print(evaluate_output("Test", "This is a very exciting test!", "hype"))