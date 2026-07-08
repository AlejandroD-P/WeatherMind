from dataclasses import dataclass


@dataclass
class Recommendation:
    risk_level: str
    status: str
    message: str