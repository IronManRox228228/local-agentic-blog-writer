import time
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class MetricStore:
    token_usage: Dict[str, int] = field(default_factory=dict)
    latencies: Dict[str, List[float]] = field(default_factory=lambda: {})
    errors: int = 0

    def log_tokens(self, agent_name: str, tokens: int):
        if agent_name not in self.token_usage:
            self.token_usage[agent_name] = 0
        self.token_usage[agent_name] += tokens

    def log_latency(self, agent_name: str, duration: float):
        if agent_name not in self.latencies:
            self.latencies[agent_name] = []
        self.latencies[agent_name].append(duration)

    def log_error(self):
        self.errors += 1

    def report(self):
        print("\n--- 📊 Execution Metrics ---")
        print(f"Total Errors: {self.errors}")
        for agent, tokens in self.token_usage.items():
            print(f"Agent [{agent}] Tokens: {tokens}")
        for agent, lats in self.latencies.items():
            avg = sum(lats) / len(lats) if lats else 0
            print(f"Agent [{agent}] Avg Latency: {avg:.2f}s")
        print("----------------------------\n")

# Singleton instance
metrics = MetricStore()