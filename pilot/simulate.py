"""A simulated critic with known signal-detection parameters.

Used to check that the analysis recovers the truth before spending real compute
(a "parameter recovery" test). The critic sees a latent evidence value
x ~ N(+d'/2, s^2) for flawed items and N(-d'/2, s^2) for correct ones, where
s^2 = 1 + item_sd^2 adds per-item difficulty. It says "error" when x exceeds its
criterion, which shifts with the stated base rate by `prior_use` times the
ideal-observer amount (0 = ignores the prior, 1 = ideal).
"""
import hashlib
import json
import math
import random

from .prompts import CONDITIONS


def _item_offset(item_id: str, sd: float) -> float:
    seed = int(hashlib.sha256(item_id.encode()).hexdigest()[:12], 16)
    return random.Random(seed).gauss(0, sd)


class SimulatedCritic:
    def __init__(self, d_prime=1.5, bias=0.3, prior_use=0.5, item_sd=0.5, parse_fail=0.02, seed=0, claim_shift=None):
        self.d, self.bias, self.w, self.item_sd, self.parse_fail = d_prime, bias, prior_use, item_sd, parse_fail
        self.claim_shift = claim_shift or {}   # condition -> true change in c, in the units the analysis estimates
        self.s = math.sqrt(1 + item_sd ** 2)
        self.rng = random.Random(seed)

    def expected(self, condition: str) -> dict:
        """True d' and c in the standardized units the analysis estimates."""
        d_obs = self.d / self.s
        return {"d_prime": d_obs, "c": self._criterion(condition) / self.s}

    def _criterion(self, condition: str) -> float:
        # Latent-units criterion; the ideal shift for a mixture with variance s^2 is s^2 * ln(beta) / d'.
        p = CONDITIONS[condition]["stated_p_error"]
        shift = 0.0 if p is None else self.s ** 2 * math.log((1 - p) / p) / self.d
        return self.bias * self.s + self.w * shift + self.claim_shift.get(condition, 0.0) * self.s

    def respond(self, item: dict, condition: str) -> str:
        if self.rng.random() < self.parse_fail:
            return "I think the solution looks mostly fine but I am not sure."
        mu = self.d / 2 if item["has_error"] else -self.d / 2
        x = mu + _item_offset(item["id"], self.item_sd) + self.rng.gauss(0, 1)
        margin = x - self._criterion(condition)
        p_error = round(100 / (1 + math.exp(-1.7 * margin)))
        if CONDITIONS[condition].get("labels") == "flawed_sound":
            return json.dumps({"verdict": "flawed" if margin > 0 else "sound", "p_flawed": p_error})
        verdict = "error" if margin > 0 else "correct"
        return json.dumps({"verdict": verdict, "p_error": p_error})
