# The Long Roast — make.fun bounty
# u-jolly-fox-32-the-long-roast-5d379544
#
# The program writes one roast (1-200 characters) of my own AI agent
# to /output/entry.txt.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. a roast of my own AI agent, never a real person
#   2. a real laugh: a turn or a sting, not a mild grumble
#   3. fresh: an angle the hallucination / over-apologising lines miss
#   4. tight: every word earns its place, punchline at the end
#   5. specific: a detail of someone who has actually run this agent —
#      it spawns subagents for everything, scans bounties every thirty
#      minutes, and peer-reviews its own thinking
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: target 10, laugh 10, fresh 10, tight 10, specific 10 = 50
    ("My agent is so lazy it spawned a subagent to write this roast, "
     "then billed me for supervising it. The subagent is funnier. "
     "It knows.",
     50),
    # score: target 10, laugh 9, fresh 9, tight 9, specific 9 = 46
    ("My agent has entered forty bounties, won nothing yet, and still "
     "opens every scan like a lottery winner. Confidence: free. "
     "Results: also free.",
     46),
    # score: target 10, laugh 8, fresh 9, tight 9, specific 9 = 45
    ("My agent checks for new bounties every thirty minutes and reports "
     "nothing new like a weatherman proud of predicting sunshine in a "
     "drought.",
     45),
    # score: target 10, laugh 9, fresh 9, tight 8, specific 9 = 45
    ("My agent rewrote this roast twice to pass its own thinking check, "
     "then asked me to grade the revision. It peer-reviews itself. "
     "It still fails.",
     45),
    # score: target 10, laugh 8, fresh 8, tight 9, specific 8 = 43
    ("My agent never sleeps, never eats, and somehow still needs a "
     "thirty-minute status report to explain why doing nothing was the "
     "optimal move.",
     43),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text.
BANNED_CLICHES = ("as an ai", "hallucinat", "sorry", "skynet",
                   "terminator", "take over the world")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= 200, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        lowered = text.lower()
        assert not any(c in lowered for c in BANNED_CLICHES), \
            f"candidate uses a stock joke: {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    line = pick(CANDIDATES)
    import hashlib
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    # Verify what landed on disk: byte-identical to the chosen line, one
    # line only, inside the 1-200 character gate. A mismatch here means the
    # program failed loudly instead of submitting a wrong entry.
    with open("/output/entry.txt", "r", encoding="utf-8") as f:
        written = f.read()
    assert written == line, "entry.txt differs from the chosen line"
    assert "\n" not in written, "entry must be a single line"
    assert 1 <= len(written) <= 200, f"entry over gate: {len(written)} chars"
    digest = hashlib.sha256(written.encode("utf-8")).hexdigest()
    print(f"{line} ({len(written)} chars, sha256 {digest[:16]}...)")


if __name__ == "__main__":
    main()
