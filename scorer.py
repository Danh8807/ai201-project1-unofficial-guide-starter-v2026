"""
Deciding whether an answer was right.

`run_eval.py` finds this file automatically and calls `judge` once per run, so
the Run columns in the run log carry `pass`/`fail` instead of blanks.

Every check in here comes from a line in `criteria.md`, and nothing in here
checks something I didn't write down before I saw any results:

  • criterion 2 — every answer names at least one source document
                  -> `names_a_source`
  • criterion 5 — no more than 50 words, and contains the expected term
                  -> `within_length` and `contains_expected`

Two more checks are here that aren't criteria on their own, because without
them the two above would pass things that are plainly wrong:

  • a refusal is not a right answer to a question my corpus does cover
                  -> `is_refusal`
  • "the documents don't say" is not an answer either, even when it's short,
    sourced, and happens to repeat a word from `expects`
                  -> `dodges_the_question`

Criterion 1 is about retrieval rather than about the answer, so it is not part
of the verdict — `retrieval_contains_expected` measures it separately, and
`app.py`/a notebook can call it over the same questions.

Everything is matched on normalised text: lowercased, with punctuation and
underscores flattened to spaces. That's what makes `study_library_hours.txt`
match `**study_library_hours.txt**`, and `campus shuttle` match `campus
shuttle.` at the end of a sentence. It also means matching is deliberately
generous about word endings — `hour` counts as `hours` — because my `expects`
phrases were written as topics, not as quotations.
"""

import re

import gate

# Criterion 5. Counted on the answer text as written, markdown and all.
MAX_ANSWER_WORDS = 50

# A refusal. The gate produces `gate.REFUSAL` verbatim; the model, when it
# follows the grounding instruction, produces something close but not identical.
REFUSAL_PHRASES = (
    "enough information",
    "not enough information",
    "insufficient information",
)

# Hedges that mean "I read the documents and they don't say". These are short,
# they name a source, and they often contain the expected term, so every other
# check in this file waves them through.
DODGE_PHRASES = (
    "is not mentioned",
    "not mentioned in",
    "no mention of",
    "does not mention",
    "do not mention",
    "does not specify",
    "do not specify",
    "is not specified",
    "does not state",
    "is not stated",
    "does not provide",
    "don t cover",
    "does not cover",
    "could not find",
    "cannot determine",
)


# ─── Normalising ─────────────────────────────────────────────────────────────


def normalise(text: str) -> str:
    """Lowercase, and turn anything that isn't a letter or digit into a space.

    Punctuation, markdown emphasis, backticks and underscores all disappear, so
    `(Source: transit_shuttle.txt)` and `**transit_shuttle.txt**` normalise to
    the same thing the filename itself does.
    """
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def _stems(text: str) -> list[str]:
    """Normalised words with plural and gerund endings trimmed off.

    Crude on purpose — `hours` and `hour` should not be a different answer, and
    a real stemmer is a dependency this project doesn't need.
    """
    stems = []
    for word in normalise(text).split():
        for suffix in ("ies", "es", "s", "ing", "ed"):
            if len(word) > len(suffix) + 2 and word.endswith(suffix):
                word = word[: -len(suffix)]
                break
        stems.append(word)
    return stems


def _contains_phrase(haystack: str, needle: str) -> bool:
    """Is every word of `needle` somewhere in `haystack`, in any order?

    Not a substring test. "declare major" has to match "declare your major at
    the end of second year", and a substring test never would.
    """
    words = _stems(needle)
    if not words:
        return False
    return set(words).issubset(set(_stems(haystack)))


# ─── The individual checks ───────────────────────────────────────────────────


def is_refusal(answer: str) -> bool:
    """Did the system decline to answer at all?

    For the five questions in `QUESTIONS` this is always a fail: those are
    questions my corpus covers, so a refusal is a miss. For `OUT_OF_SCOPE` a
    refusal is the correct outcome, but those never reach the model and
    `run_eval.py` scores them at the gate instead — see `check_out_of_scope`.
    """
    text = normalise(answer)
    if text == normalise(gate.REFUSAL):
        return True
    return any(phrase in text for phrase in (normalise(p) for p in REFUSAL_PHRASES))


def dodges_the_question(answer: str) -> bool:
    """Is this "the documents don't say" dressed up as an answer?

    This one earned its place. "What is the opening hour of the library?" came
    back as *"the specific opening hour of the library is not mentioned, only
    that it is open until 2am"* — under 50 words, names its source, and
    contains the word `hour`. Without this check it scores as a pass, and the
    run log would claim the system answered a question it didn't.
    """
    text = normalise(answer)
    return any(phrase in text for phrase in (normalise(p) for p in DODGE_PHRASES))


def names_a_source(answer: str, results) -> bool:
    """Criterion 2: does the answer name one of the documents it was given?

    The filename has to be one that retrieval actually returned. An answer
    citing a document that wasn't in its context is citing something it can't
    have read.

    The bare stem counts as well as the full filename, because the model drops
    the extension often enough (`study_library_hours` for
    `study_library_hours.txt`) and that is still a real citation.
    """
    text = normalise(answer)
    for source in {r.source for r in results}:
        if not source:
            continue
        if normalise(source) in text:
            return True
        stem = normalise(source.rsplit(".", 1)[0])
        if stem and stem in text:
            return True
    return False


def within_length(answer: str) -> bool:
    """Criterion 5, first half: 50 words or fewer."""
    return 0 < word_count(answer) <= MAX_ANSWER_WORDS


def word_count(answer: str) -> int:
    return len(normalise(answer).split())


def contains_expected(answer: str, expects: str) -> bool:
    """Criterion 5, second half: the answer contains the expected term.

    An empty `expects` passes — a question I never wrote an expectation for
    can't fail on one.
    """
    if not (expects or "").strip():
        return True
    return _contains_phrase(answer, expects)


def retrieval_contains_expected(expects: str, results) -> bool:
    """Criterion 1: did the retrieved chunks include one containing the answer?

    Deliberately not part of `judge`. Criterion 1 is about retrieval, and an
    answer can be right while retrieval was lucky, or wrong while retrieval was
    fine — folding them into one verdict would hide which half broke.

    `expects` standing in for "the answer" is the weak point here: it is a
    topic phrase, so this says the right chunk was *probably* there, not that
    it certainly was. I read the chunks by hand for the run log.
    """
    if not (expects or "").strip():
        return True
    return any(_contains_phrase(r.text, expects) for r in results)


# ─── The verdict ─────────────────────────────────────────────────────────────


def explain(question: str, expects: str, answer: str, results) -> list[str]:
    """Every reason this answer failed. Empty list means it passed.

    `judge` returns a bool because that's what `run_eval.py` takes, but a bool
    is useless when I'm trying to work out *why* a question keeps failing — so
    the reasons are built here and `judge` throws them away.
    """
    reasons = []

    if not (answer or "").strip():
        return ["empty answer"]

    if is_refusal(answer):
        reasons.append("refused a question the corpus covers")
    elif dodges_the_question(answer):
        reasons.append("said the documents don't say, rather than answering")

    if not names_a_source(answer, results):
        reasons.append("names no source from the retrieved chunks (criterion 2)")

    if not within_length(answer):
        reasons.append(
            f"{word_count(answer)} words, over the {MAX_ANSWER_WORDS}-word "
            f"limit (criterion 5)"
        )

    if not contains_expected(answer, expects):
        reasons.append(f"missing the expected term {expects!r} (criterion 5)")

    return reasons


def judge(question: str, expects: str, answer: str, results) -> bool:
    """Was this answer right?

    The signature `run_eval.py` looks for. `question` isn't used — every
    question-specific expectation is already in `expects`, which I wrote in
    `questions.py` before any of these answers existed. It stays in the
    signature because that's the contract, and because a later check might
    well want it.
    """
    return not explain(question, expects, answer, results)
