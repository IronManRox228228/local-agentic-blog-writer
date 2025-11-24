import requests
import yaml
import json
import time
from observability.metrics import metrics

with open("config/models.yaml", "r") as f:
    config = yaml.safe_load(f)


def call_llm(messages, agent_role="default", temperature=0.7):
    url = f"{config['endpoint']}/chat/completions"
    model_id = config.get(agent_role, "lfm2-vl-450m")

    payload = {
        "model": model_id,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 20000
    }

    start_time = time.time()
    try:
        response = requests.post(url, json=payload, timeout=config['timeout'])
        response.raise_for_status()
        data = response.json()

        content = data['choices'][0]['message']['content']
        usage = data.get('usage', {}).get('total_tokens', 0)

        # Metrics
        metrics.log_tokens(agent_role, usage)
        metrics.log_latency(agent_role, time.time() - start_time)

        return content
    except Exception as e:
        metrics.log_error()
        print(f"LLM Call Failed for {agent_role}: {e}")
        # Fallback for small models that might fail
        return f"[Error generating text: {e}]"