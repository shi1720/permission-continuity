"""Exact permission-window accounting; integer days, half-open intervals.

This is an audit of declared inputs, not a predictor of legal decisions or outages.
No third-party dependencies. A path's capacity, scope and technical readiness
must be validated by its caller before it is supplied to these functions.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product

@dataclass(frozen=True, order=True)
class Window:
    start: int
    end: int

    def __post_init__(self):
        if type(self.start) is not int or type(self.end) is not int:
            raise TypeError("Window endpoints must be integer days")
        if self.end <= self.start:
            raise ValueError("A window must have positive duration")

def union(windows):
    result = []
    for w in sorted(windows):
        if result and w.start <= result[-1].end:
            old = result.pop()
            result.append(Window(old.start, max(old.end, w.end)))
        else:
            result.append(w)
    return result

def intersection(layers):
    """Every layer is required, alternatives within a layer are substitutable."""
    if not layers:
        raise ValueError("At least one required layer is necessary")
    result = union(layers[0])
    for layer in layers[1:]:
        found = []
        for a, b in product(result, union(layer)):
            lo, hi = max(a.start, b.start), min(a.end, b.end)
            if lo < hi:
                found.append(Window(lo, hi))
        result = union(found)
    return result

def safe_starts(windows, duration, horizon):
    """Integer start days t such that [t,t+duration) is wholly covered.

    Output windows contain integer start days, including t=end-duration.
    horizon bounds candidate starts, not the end of the disruption.
    """
    if type(duration) is not int:
        raise TypeError("Duration must be an integer number of days")
    if duration < 1:
        raise ValueError("Duration must be a positive integer")
    result = []
    for w in union(windows):
        lo = max(w.start, horizon.start)
        hi = min(w.end-duration+1, horizon.end)
        if lo < hi:
            result.append(Window(lo, hi))
    return union(result)

def count(windows):
    return sum(w.end-w.start for w in union(windows))

def audit(paths, duration, horizon, switching=False):
    """Union after erosion disallows switching; erosion after union permits it.

    switching=True assumes instantaneous compatible handoff, sufficient capacity,
    and all necessary authorizations for switching. It is an optimistic bound.
    """
    effective = [intersection(layers) for layers in paths]
    if switching:
        safe = safe_starts([w for p in effective for w in p], duration, horizon)
    else:
        safe = union([w for p in effective for w in safe_starts(p, duration, horizon)])
    return {"safe_days":count(safe), "candidate_days":horizon.end-horizon.start,
            "safe_windows":[[w.start,w.end] for w in safe],
            "effective_paths":[[[w.start,w.end] for w in p] for p in effective]}
