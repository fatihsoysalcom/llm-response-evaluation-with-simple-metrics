import re

def simulate_llm_response(prompt: str) -> str:
    """
    Simulates an LLM generating a response based on a given prompt.
    In a real scenario, this would be an API call to an actual LLM.
    """
    prompt_lower = prompt.lower()
    if "capital of france" in prompt_lower:
        return "Paris is the capital and most populous city of France. Situated on the River Seine, it is a major European city and a global center for art, fashion, gastronomy and culture."
    elif "shortest path algorithm" in prompt_lower:
        return "Dijkstra's algorithm is an algorithm for finding the shortest paths between nodes in a graph, which may represent, for example, road networks. It was conceived by computer scientist Edsger W. Dijkstra in 1956 and published three years later."
    elif "explain quantum physics" in prompt_lower:
        # This response is intentionally a bit long to show metric flagging
        return "Quantum physics is a fundamental theory in physics that describes the properties of nature at the scale of atoms and subatomic particles. It's quite complex and involves concepts like wave-particle duality and quantum entanglement, challenging classical physics."
    elif "who invented the lightbulb" in prompt_lower:
        # This response is intentionally a bit generic/long to show metric flagging
        return "The invention of the lightbulb is often credited to Thomas Edison, who significantly improved upon earlier designs and made it practical for widespread use. However, many inventors contributed to its development over time."
    else:
        return "I'm sorry, I don't have enough information to answer that question comprehensively."

def evaluate_llm_response(
    prompt: str,
    llm_response: str,
    expected_keywords: list[str],
    min_length: int,
    max_length: int
) -> dict:
    """
    Evaluates an LLM response based on predefined objective metrics.
    This moves beyond subjective 'feels good' to quantifiable scores.
    """
    evaluation_results = {}

    # Metric 1: Keyword Presence (Relevance)
    # This checks how many of the critical keywords are present in the response.
    # Using regex with word boundaries to avoid partial matches (e.g., "car" in "cart").
    found_keywords = [
        keyword for keyword in expected_keywords
        if re.search(r'\b' + re.escape(keyword) + r'\b', llm_response, re.IGNORECASE)
    ]
    keyword_match_score = len(found_keywords) / len(expected_keywords) if expected_keywords else 1.0
    evaluation_results["keyword_match_score"] = round(keyword_match_score, 2)
    evaluation_results["found_keywords"] = found_keywords

    # Metric 2: Response Length (Conciseness/Completeness)
    # This checks if the response falls within a desired length range.
    response_word_count = len(llm_response.split())
    evaluation_results["response_word_count"] = response_word_count
    if min_length <= response_word_count <= max_length:
        length_score = 1.0
        length_status = "within range"
    elif response_word_count < min_length:
        length_score = 0.5 # Penalize for being too short
        length_status = "too short"
    else: # response_word_count > max_length
        length_score = 0.7 # Penalize for being too long
        length_status = "too long"
    evaluation_results["length_score"] = round(length_score, 2)
    evaluation_results["length_status"] = length_status

    # Metric 3: Overall Score (a simple weighted average for demonstration)
    # In a real system, this would be more sophisticated with different weights
    # and potentially more metrics (e.g., factuality, toxicity, coherence).
    overall_score = (keyword_match_score * 0.6) + (length_score * 0.4)
    evaluation_results["overall_score"] = round(overall_score, 2)

    return evaluation_results

if __name__ == "__main__":
    print("--- Production-Level LLM Evaluation: From Intuition to Metrics ---")
    print("This example demonstrates moving from subjective 'feels good' to objective, metric-driven LLM evaluation.\n")

    # Define a set of test cases with objective evaluation criteria
    test_cases = [
        {
            "prompt": "What is the capital of France?",
            "expected_keywords": ["Paris", "France", "capital", "city"],
            "min_length": 20,
            "max_length": 40,
            "subjective_expectation": "Should be accurate and concise about Paris."
        },
        {
            "prompt": "Explain Dijkstra's algorithm.",
            "expected_keywords": ["Dijkstra", "algorithm", "shortest paths", "graph"],
            "min_length": 30,
            "max_length": 60,
            "subjective_expectation": "Should clearly explain the algorithm's purpose."
        },
        {
            "prompt": "Tell me about quantum physics in one sentence.",
            "expected_keywords": ["quantum physics", "atoms", "particles", "theory"],
            "min_length": 10,
            "max_length": 20,
            "subjective_expectation": "Should be very brief but informative."
        },
        {
            "prompt": "Who invented the lightbulb?",
            "expected_keywords": ["lightbulb", "Edison", "invented"],
            "min_length": 15,
            "max_length": 25,
            "subjective_expectation": "Should mention key figures and invention."
        }
    ]

    for i, test_case in enumerate(test_cases):
        print(f"\n--- Test Case {i+1} ---")
        prompt = test_case["prompt"]
        expected_keywords = test_case["expected_keywords"]
        min_length = test_case["min_length"]
        max_length = test_case["max_length"]
        subjective_expectation = test_case["subjective_expectation"]

        print(f"Prompt: '{prompt}'")
        print(f"Subjective Expectation: '{subjective_expectation}'")
        print(f"Objective Criteria: Keywords={expected_keywords}, Length={min_length}-{max_length} words")

        # Simulate LLM response
        llm_response = simulate_llm_response(prompt)
        print(f"\nLLM Response:\n'{llm_response}'")

        # Evaluate the response using defined metrics
        # This is the core concept: replacing intuition with quantifiable metrics.
        evaluation_metrics = evaluate_llm_response(
            prompt, llm_response, expected_keywords, min_length, max_length
        )

        print("\n--- Objective Evaluation Metrics ---")
        print(f"  Keyword Match Score: {evaluation_metrics['keyword_match_score']} (Found: {evaluation_metrics['found_keywords']})")
        print(f"  Response Word Count: {evaluation_metrics['response_word_count']} ({evaluation_metrics['length_status']})")
        print(f"  Length Score: {evaluation_metrics['length_score']}")
        print(f"  Overall Score: {evaluation_metrics['overall_score']}")

        # A simple interpretation based on metrics
        if evaluation_metrics['overall_score'] >= 0.8:
            print("\nConclusion: The response objectively performed well against criteria. (Production-ready candidate)")
        elif evaluation_metrics['overall_score'] >= 0.6:
            print("\nConclusion: The response objectively performed acceptably, but has room for improvement. (Needs refinement)")
        else:
            print("\nConclusion: The response objectively performed poorly against criteria. (Requires significant work)")

        print("-" * 40)
