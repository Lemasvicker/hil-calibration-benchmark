from __future__ import annotations
import math
import random
from dataclasses import dataclass

@dataclass
class Stream:
    y_true: list[int]     # 1 = event soon, 0 = not
    score: list[float]    # model score in [0,1]

def make_synthetic_stream(n: int = 600, seed: int = 7) -> Stream:
    rng = random.Random(seed)
    y_true, score = [], []
    for t in range(n):
        # rare "event windows"
        in_event = 1 if (t % 200) in range(150, 165) else 0
        base = 0.10 + 0.65 * in_event
        s = min(1.0, max(0.0, base + rng.gauss(0.0, 0.08)))
        y_true.append(in_event)
        score.append(s)
    return Stream(y_true=y_true, score=score)

def simulate_alerts(stream: Stream, threshold: float) -> dict:
    alerts = [1 if s >= threshold else 0 for s in stream.score]
    tp = sum(1 for a, y in zip(alerts, stream.y_true) if a == 1 and y == 1)
    fp = sum(1 for a, y in zip(alerts, stream.y_true) if a == 1 and y == 0)
    fn = sum(1 for a, y in zip(alerts, stream.y_true) if a == 0 and y == 1)
    # simple burden proxy: alerts per hour if fs=1Hz (here: per 600s -> per 10min)
    burden = sum(alerts) / max(len(alerts), 1)
    precision = tp / (tp + fp + 1e-12)
    recall = tp / (tp + fn + 1e-12)
    f1 = 2 * precision * recall / (precision + recall + 1e-12)
    return {"tp": tp, "fp": fp, "fn": fn, "precision": precision, "recall": recall, "f1": f1, "burden": burden}

def hil_calibration_loop(stream: Stream, start: float = 0.50, steps: int = 6) -> float:
    """
    Toy HIL loop: if burden too high -> increase threshold;
    if recall too low -> decrease threshold.
    """
    thr = start
    for _ in range(steps):
        m = simulate_alerts(stream, thr)
        if m["burden"] > 0.20:
            thr = min(0.95, thr + 0.05)
        elif m["recall"] < 0.60:
            thr = max(0.05, thr - 0.05)
        else:
            break
    return thr

def main() -> None:
    stream = make_synthetic_stream()
    thr0 = 0.50
    m0 = simulate_alerts(stream, thr0)
    thr1 = hil_calibration_loop(stream, start=thr0)
    m1 = simulate_alerts(stream, thr1)

    print("HIL Calibration Benchmark demo (synthetic)")
    print(f"Start threshold: {thr0:.2f} | precision={m0['precision']:.3f} recall={m0['recall']:.3f} f1={m0['f1']:.3f} burden={m0['burden']:.3f}")
    print(f"Calibrated thr : {thr1:.2f} | precision={m1['precision']:.3f} recall={m1['recall']:.3f} f1={m1['f1']:.3f} burden={m1['burden']:.3f}")

if __name__ == "__main__":
    main()
