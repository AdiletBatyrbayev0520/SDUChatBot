from typing import Dict


MODEL_PRICES_USD_PER_1K_TOKENS: Dict[str, Dict[str, float]] = {
    # gpt-4.1: $5 input, $15 output per 1M ⇒ $0.005 / $0.015 per 1K
    "gpt-4.1": {"input": 0.005, "cached_input": 0.001, "output": 0.015},
    # gpt-4.1-mini: $0.40 / $1.60 per 1M ⇒ $0.0004 / $0.0016 per 1K
    "gpt-4.1-mini": {"input": 0.0004, "cached_input": 0.0001, "output": 0.0016},
    # gpt-4o-mini: $0.15 / $0.60 per 1M ⇒ $0.00015 / $0.0006 per 1K
    # Batch API ~50% discount exists, but current calculator ignores batch_* fields
    "gpt-4o-mini": {"input": 0.00015, "cached_input": 0.0, "output": 0.0006},
    # gpt-4.5-preview: $75 / $150 per 1M ⇒ $0.075 / $0.15 per 1K
    "gpt-4.5-preview": {"input": 0.075, "cached_input": 0.0, "output": 0.15},
    # o1: $150 / $600 per 1M ⇒ $0.15 / $0.60 per 1K
    "o1": {"input": 0.15, "cached_input": 0.0, "output": 0.60},
    # o3-pro: $80 / $20 per 1M ⇒ $0.08 / $0.02 per 1K
    "o3-pro": {"input": 0.08, "cached_input": 0.0, "output": 0.02},
}


def get_model_cost_for_usage(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    prices = MODEL_PRICES_USD_PER_1K_TOKENS.get(model)
    if not prices:
        return 0.0
    input_cost = (prompt_tokens / 1000.0) * prices["input"]
    output_cost = (completion_tokens / 1000.0) * prices["output"]
    return round(input_cost + output_cost, 6)


def get_model_cost_per_pdf(model: str, total_input_tokens: int, total_output_tokens: int) -> float:
    prices = MODEL_PRICES_USD_PER_1K_TOKENS.get(model)
    if not prices:
        return 0.0
    input_cost = (total_input_tokens / 1000.0) * prices["input"]
    output_cost = (total_output_tokens / 1000.0) * prices["output"]
    return round(input_cost + output_cost, 6)


def get_model_prices(model: str) -> Dict[str, float] | None:
    return MODEL_PRICES_USD_PER_1K_TOKENS.get(model)


