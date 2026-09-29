# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. --> This project is an unofficial advising assistant built to help university students navigate academic policies, course selection, and campus administrative procedures. Using a focused corpus of university handbooks, policy sheets, and course guides, the system answers everyday logistical questions such as major declaration deadlines, pass/fail options, and graduation requirements. It pairs vector-based semantic search with distance-gated retrieval to locate exact policy excerpts and generate direct, grounded answers. If a query falls outside the available campus documents, the system stops hallucination by refusing to answer rather than guessing.

## Chunking Strategy 

**Chunk size:**
**Overlap:**

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `thread_bike_commute.txt#0` — produced by: `chunker.py::split_documents`

```
THREAD: Anything specific for first-generation students?

--- reply 1 (33 votes) ---
The advising office has a specific programme and it is genuinely good, but it is opt-in and badly publicised. Ask for it by name.
```

**Chunk 2** — source: `thread_first_gen.txt#0` — produced by: `chunker.py::split_documents`

```
THREAD: Anything specific for first-generation students?

--- reply 1 (33 votes) ---
The advising office has a specific programme and it is genuinely good, but it is opt-in and badly publicised. Ask for it by name.
```

**Chunk 3** — source: `thread_laptop_specs.txt#1` — produced by: `chunker.py::split_documents`

```
THREAD: How much laptop do I actually need for CS courses?

--- reply 2 (18 votes) ---
Adding: the lab machines exist and are better than anything you'll buy. For the heavy assignments people just use those.
```

**Chunk 4** — source: `thread_office_hours_etiquette.txt#1` — produced by: `chunker.py::split_documents`

```
THREAD: Is it weird to go to office hours with no specific question?

--- reply 2 (29 votes) ---
They're usually empty. You are doing the instructor a favour by turning up.

--- reply 3 (18 votes) ---
If it helps, treat it as a standing appointment. Go every week for a month and it stops feeling like a thing.
```

**Chunk 5** — source: `thread_roommate_conflict.txt#1` — produced by: `chunker.py::split_documents`

```
THREAD: Roommate situation isn't working. What now?

--- reply 2 (14 votes) ---
Room changes happen at the semester boundary almost always, and mid-semester only in fairly serious cases.

--- reply 3 (33 votes) ---
Write down specifics before the meeting. 'It's not working' is hard to act on; 'guests four nights a week past 2am'is not.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** "When can I declare my major?"

**Answer:**

```
You can declare your major at the end of your second semester, or later if you need to. 

Source: admin_declaring_a_major.txt

Sources retrieved: admin_add_drop_deadline.txt, admin_declaring_a_major.txt, admin_graduation_requirements.txt, admin_pass_fail_option.txt, admin_study_abroad.txt
```

**My relevance cutoff:**: 0.6 

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|"Does work-study affect your financial aid?"                 |Yes|0.341|
|"When can I declare my major?"                               |Yes|0.308|
|"What is the opening hour of the library?"                   |Yes|0.235|
|"Where to sit at the library?"                               |Yes|0.349|
|"What is the transit shuttle schedule?"                      |Yes|0.383|
|"What is the capital of Mongolia?                            |No |0.825|
|"How do I change the oil in a diesel engine?"                |No |0.850|
|"Who won the 1994 World Cup?"                                |No |0.846|
|"What is the recommended dosage of ibuprofen for a headache?"|No |0.849|
|"How do I write a for loop in Rust?"                         |No |0.864|

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.** I asked Claude to write the chunking function. It came back with a complete chunking function with overlap. 

**2.** I realize that it is better to include the thread title in each chunk, so I asked Claude to include that in the chunking function. It came back with some codes and I changed my chunking function based on that. 

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |4/5  |4/5  |4/5  |MET  |
| 2. Every answer names a source | 4 of 5 |5/5  |5/5  |5/5  |MET  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |5/5  |5/5  |5/5  |MET  |
| 4. Chunks are 200–400 characters|4 of 5 |4/5 |4/5 |4/5 |MET |
| 5. Answer ≤50 words and contains expected term|5 of 5 |5/5 |5/5 |5/5 |MET |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->
     Produced by `run_eval.py::main`, judged by `scorer.py::judge` / `explain`,
retrieval from `store.py::search`, chunks from `chunker.py::split_documents`.

**Criterion 1** — the one failing case (identical across all 3 runs):

Question: What is the opening hour of the library?
Best distance: 0.2348 (passed the gate)
Sources retrieved: admin_library_holds.txt, housing_calder_annexe_noise.txt,
housing_morrow_house_noise.txt, housing_old_brewhouse_noise.txt, study_library_hours.txt

Based on the provided documents, the specific opening hour of the library is not
mentioned, only the closing times (until 2am during term and until 10pm during
reading week).

Source: study_library_hours.txt


**Criterion 2** — `scorer.py::names_a_source` passing case:

Question: What is the transit shuttle schedule? — run 2
The campus shuttle runs a loop every 20 minutes from 7:00 am to 11:00 pm on
weekdays, and every 40 minutes on weekends. (Source: transit_shuttle.txt)

`names_a_source` normalises "(Source: transit_shuttle.txt)" and matches it
against the retrieved source list — passes.

**Criterion 3** — `run_eval.py::check_out_of_scope`, cutoff 0.6:

What is the capital of Mongolia? — best distance 0.825 — refused
How do I change the oil in a diesel engine? — best distance 0.850 — refused
Who won the 1994 World Cup? — best distance 0.846 — refused
What is the recommended dosage of ibuprofen for a headache? — best distance 0.849 — refused
How do I write a for loop in Rust? — best distance 0.864 — refused
-> gate refused 5 of 5


**Criterion 4** — 
  ======================================================================
> Chunk 2  |  source: admin_campus_jobs_and_financial_aid.txt#0  |  produced by: chunker.py::split_documents
  ======================================================================
  On the campus jobs and financial aid
  
  Work-study earnings don't count against your financial aid the way ordinary income does. Non-work-study campus jobs 
pay the same and do count, which is a difference worth understanding before you take the first job offered.
  
  ======================================================================
> Chunk 3  |  source: admin_declaring_a_major.txt#0  |  produced by: chunker.py::split_documents
  ======================================================================
  On the declaring a major
  
  You declare at the end of your second semester, or later if you need to. There's no penalty for declaring late and no 
advantage to declaring early except that it assigns you a departmental adviser, who is generally more useful than the 
general one.
  
  ======================================================================
  ======================================================================
> Chunk 112  |  source: study_library_hours.txt#0  |  produced by: chunker.py::split_documents
  ======================================================================
  Library hours and where to actually sit
  
  Open until 2am during term, until 10pm during reading week, which is backwards and catches everyone out every single 
year.
  
  Third floor is silent and enforced. Second floor is quiet in theory. The basement has the only outlets at every seat 
and is therefore full from about 10am.
  ======================================================================
> Chunk 113  |  source: transit_shuttle.txt#0  |  produced by: chunker.py::split_documents
  ======================================================================
  The campus shuttle
  
  Runs a loop every 20 minutes from 7am to 11pm on weekdays and every 40 minutes on weekends. The published timetable 
is optimistic by about five minutes in the morning and accurate the rest of the day.
  
  ======================================================================
> Chunk 114  |  source: transit_shuttle.txt#1  |  produced by: chunker.py::split_documents
  ======================================================================
  The campus shuttle
  
  It's free with a student ID. The stop outside Fenwick Court is the one that gets skipped when the driver is behind, 
which is worth knowing if you live there.
  
  ======================================================================


**Criterion 5** — `scorer.py::within_length` + `contains_expected`, the
library-hours case (technically passes both sub-checks even though the
answer doesn't really answer the question — see Diagnoses):

Question: When can I declare my major? — expects "declare major"
You can declare your major at the end of your second semester, or later if
you need to.
Source: admin_declaring_a_major.txt

`contains_expected` matches on stems as a bag of words, not a literal phrase —
"declare" and "major" both appear, in any order, so this passes even though
the exact phrase "declare major" never appears verbatim.


## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer (target: 4/5) | MET | 4/5 held across all 3 runs, not just once — the one miss (library opening hour) retrieved the topically-correct chunk every time, so the miss is a content gap, not an inconsistent result. |
| 2 | Every answer names a source (target: 5/5) | MET | Checked all 15 answers (5 questions × 3 runs) by hand against `scorer.py::names_a_source`'s logic — every one cites a real retrieved filename. |
| 3 | Gate stops out-of-corpus questions (target: 4/5) | MET | 5/5 refused, and the distances (0.825–0.864) sit with a clean gap above the 0.6 cutoff and above every in-scope distance (0.235–0.383), so this isn't a close call. |
| 4 | Chunks are 200–400 characters (target: all chunks) | MISSED | `python app.py chunks -n 200` shows two real chunks under 200 characters (`housing_tamsin_court.txt#1` at 138, `transit_shuttle.txt#1` at 177) — one of which is retrieved for my own shuttle-schedule test question, so it's not an edge case I can wave off. |
| 5 | Answer ≤50 words and contains expected term (target: 5/5) | MET, but see revision below | Literally 5/5 by the wording I wrote — but the library-hours answer passes only because `contains_expected` matches loose word-stems, not because it actually answers the question. See `criteria.md` for why I'm revising this one rather than just noting a caveat. |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

In `chunker.py::split_documents`, the final leftover `buffer` for each
document was appended as its own chunk unconditionally, with no minimum-length
check:

     if buffer:
        pieces.append(buffer)

I changed this to merge the trailing buffer into the previous chunk instead of
standing alone, whenever it's shorter than the 200-character floor:

     if buffer:
          pieces.append(buffer)

     MIN_CHUNK_SIZE = 200

     merged: list[str] = []
     for piece in pieces:
          if merged and len(piece) < MIN_CHUNK_SIZE:
               merged[-1] = f"{merged[-1]}\n\n{piece}"
          else:
               merged.append(piece)

     if len(merged) > 1 and len(merged[0]) < MIN_CHUNK_SIZE:
          merged[1] = f"{merged[0]}\n\n{merged[1]}"
          merged = merged[1:]

     pieces = merged

**Why I picked it:** Milestone 3 diagnosed the criterion 4 miss as a single
mechanism — not two unrelated problems — causing both violations
(`housing_tamsin_court.txt#1` at 138 chars, `transit_shuttle.txt#1` at 177
chars): a document's last paragraph gets closed out as a chunk unconditionally
once the loop ends, with no check against the minimum. I picked this fix
because it targets that exact mechanism directly, rather than a workaround
like raising `chunk_size` globally (which wouldn't fix a *short* trailing
piece) or hand-editing the two known-bad documents (which would hide the bug
instead of fixing it — the next document added to the corpus with a short
final paragraph would hit the same failure).

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

## Run Log — After

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | 4 of 5 | 4/5 | 4/5 | 4/5 | MET (unchanged) |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET (unchanged) |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET (unchanged) |
| 4. Chunks are 200–400 characters | all chunks | shortest 178, longest 461 | (deterministic) | (deterministic) | still MISSED |
| 5. Answer ≤50 words and contains expected term | 5 of 5 | 5/5 | 5/5 | 5/5 | MET (unchanged) |

**Did it help?**

Partially. The worst violation before the fix — a 23-character chunk that was
just a document title standing alone (`admin_housing_lottery.txt`, "On the
housing lottery") — is gone; the shortest chunk is now 178 characters, a real
paragraph. But the merge strategy (fold any chunk under 200 characters into
its neighbor, no upper check) traded one failure mode for another: at least
one merge pushed a combined chunk to 461 characters, over the 400 ceiling.
Chunk count dropped from 117 to 90, so this pattern happened across more of
the corpus than just the one case I diagnosed by hand.


## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->Criterion 4 remains MISSED. The chunker now guarantees a floor (merge-only
logic) but not a ceiling — it never checks whether a merge result stays under
400 before committing to it. Fixing this properly would need the merge to
check the combined length first and fall back to leaving a short chunk
standalone when merging would break the 400 ceiling instead. I'm accepting
this trade-off for this submission given time constraints: the fix
measurably reduced the severity of the violation (worst case went from a
23-character orphaned title to a 178-character real paragraph) without
regressing any other criterion, but it does not fully satisfy criterion 4 as
written.

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
**Criterion 4 (chunk 200–400 characters):** I'd write this as a range with an
explicit tolerance instead of a hard floor and ceiling, or add a note on how
violations should be resolved when they conflict. My fix this unit revealed
the two bounds actively fight each other — merging a chunk up to clear the
200-character floor can push it past the 400-character ceiling, and nothing
in my original criterion said which one wins. If I'd written "at least 90% of
chunks fall in 200–400 characters, and no chunk is under 100 or over 500" up
front, I'd have had a real tolerance band instead of discovering the
trade-off live during the fix, out of time to resolve it properly.

**Criterion 5 (≤50 words, contains expected term):** I'd write this the way
`criteria.md`'s own Unit 2 guidance describes a legitimate revision — I
already added "and is not a refusal or a dodge" as a revision, and in
hindsight I'd have written it that way from the start. The original wording
let a "the documents don't say" answer pass criterion 5 outright, because
`contains_expected` matches loose word-stems rather than checking whether the
system actually attempted an answer. That's not a target I missed; it's a
target that didn't measure what I meant it to measure, and I only found that
by reading `scorer.py`'s own comments, which say as much directly.

**Criterion 1 (retrieved chunk contains the answer):** I'd leave this one
alone. It held at a consistent 4/5 across all three runs both before and
after the chunking fix, and the one miss has a diagnosis that doesn't call
the target itself into question — the fact was never in the corpus,
retrieval did its job correctly. This is the one criterion where hitting the
target on the first try didn't feel like it was set too low; a harder version
of this corpus (documents that don't state a fact plainly, or state it two
ways in different files) would be a better stress test next time, but 4/5
was a reasonable bar for what I actually wrote in Milestone 2.

**Criteria 2 and 3:** both landed comfortably above target (5/5 against 5/5,
and 5/5 against a 4/5 target) with a clean margin in the underlying distances
— I'd tighten criterion 3's target to 5/5 next time, since the actual
separation between in-scope and out-of-scope distances (0.235–0.383 vs.
0.825–0.864) leaves no real ambiguity for this gate to fail on, and "4 of 5"
turned out to be a safe target rather than a meaningful one.