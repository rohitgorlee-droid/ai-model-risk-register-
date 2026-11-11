"""AI Governance: AI Model Risk Register (base version)."""
import json
from dataclasses import dataclass, asdict

@dataclass
class Risk:
    model: str
    description: str
    likelihood: int   # 1-5
    impact: int       # 1-5
    owner: str
    mitigation: str = ""

    @property
    def score(self):
        return self.likelihood * self.impact

    @property
    def level(self):
        return "HIGH" if self.score >= 15 else "MEDIUM" if self.score >= 8 else "LOW"

class Register:
    def __init__(self):
        self.risks = []
    def add(self, risk):
        self.risks.append(risk)
    def top(self, n=5):
        return sorted(self.risks, key=lambda r: r.score, reverse=True)[:n]
    def save(self, path):
        with open(path, "w") as f:
            json.dump([asdict(r) for r in self.risks], f, indent=2)
    @classmethod
    def load(cls, path):
        reg = cls()
        with open(path) as f:
            for d in json.load(f):
                reg.add(Risk(**d))
        return reg

if __name__ == "__main__":
    reg = Register()
    reg.add(Risk("loan-scoring-v2", "Bias against protected groups", 4, 5, "ml-team", "Quarterly fairness audit"))
    reg.add(Risk("chatbot-v1", "Prompt injection leaks data", 3, 4, "platform", "Output filtering"))
    reg.add(Risk("fraud-model", "Data drift degrades accuracy", 3, 2, "ds-team"))
    for r in reg.top():
        print(f"{r.level:6} {r.score:2}  {r.model}: {r.description}")
    reg.save("risk_register.json")
