# Venues stream: shortlist, risks and 2027 timeline

Checked on 2026-11-06. Facts are in `../venues.csv` (27 rows: the 12 original candidates plus 15 added venues). Every recorded fact comes from the venue's own pages, read with WebFetch. Searches limited to official domains were used to find those pages and the example papers. Where an official page could not be read, the CSV says so and marks the fact as unverified. The 171 pages and searches are logged in `venues_query_log.csv`.

The paper being placed: an empirical SDT study of LLM critics on ProcessBench. It covers stated base rates, the instruction to use them as a prior, payoffs, and one-line tone framings, scored with d′, c, the prior-use ratio ρ against the ideal observer, and logprob ROC curves. It compares the critics with the human SDT literature. It has four open models now, with frontier and thinking-mode models planned (C1–C8). The author comes from computer vision and wants a first publication that also helps a resume.

## Ranked shortlist

### 1. ACL 2027 through ACL Rolling Review (ARR): submit Jan 4, 2027 (main conference, with Findings as fallback)

- **Why it fits:** most published LLM-as-a-judge bias and reliability work is in *ACL main and Findings, for example *Can You Trick the Grader?* (Findings of EMNLP 2025) and conformal intervals for judges (EMNLP 2025). The ideal-observer ρ, the payoff arm and the logprob ROC set this paper apart within that literature. ACL 2027 considers papers it doesn't take for the main conference for Findings automatically. Findings is archival and well recognized on an NLP resume.
- **Timing:** about 8 weeks from now. That is enough to add one or two frontier models. Thinking mode (C8) can follow in revision if needed. ACL 2027 is in Kyoto, Aug 17–22, 2027 (main conference Aug 20–22). The commitment and notification dates are not announced yet.
- **Review time:** the published ARR cycles run about 10 weeks from submission to meta-review. In the Oct 2026 cycle that was Oct 12 to Dec 17. For a Jan 4 submission, expect reviews and meta-reviews around mid-March 2027. That is an estimate; the Jan 2027 cycle dates are not posted.
- **Risks:**
  - **Designated service contributor (new since Oct 2026).** Each submission must name a qualified person who will review 5 papers in that same cycle. Without one, the paper goes into a lottery and may be desk-rejected. Computer-vision work counts: "major ML" venues include CVPR, ICCV, ECCV and TPAMI, as well as NeurIPS, ICML, ICLR, AAAI, IJCAI, TMLR and COLM. A PhD holder qualifies with 2 such papers. A PhD student qualifies with 2 such papers and at least 3 papers in total. If the author doesn't qualify, a qualified co-author is needed, or a non-author contributor who vouches for the paper. Manual verification is slow, so apply early. All authors need complete OpenReview profiles.
  - **Novelty bar.** Reviewers will know the judge-bias literature. "Prompts move c, not d′" is already partly covered (C4; see 2608.16003 on the same ProcessBench data, 2609.18204 and 2610.22631). Lead with C1–C3 (ρ ≪ 1 against the ideal observer, no gain from the prior instruction, payoffs ignored), C5, C6 and C7. With only four small open models the work may read as narrow, so add at least one frontier model.
  - **Format.** 8 pages, plus a mandatory Limitations section; a paper without one is desk-rejected.

### 2. TMLR (rolling, free, no deadline)

- **Why it fits:** TMLR judges technical correctness and whether claims are backed by evidence, not perceived significance. That suits a clean claims-and-CIs study by a newcomer. It accepts LLM-judge papers, for example *Quantitative LLM Judges Using Post-Hoc Score Calibration* (Aug 2026). It is free and open access. A TMLR paper with a J2C, Featured or Outstanding certification can be presented at NeurIPS, ICLR or ICML through the Journal-to-Conference track. That presentation does not count as a proceedings paper.
- **Review time:** no statistics are published. Reviews are due 2 weeks after assignment if the main text is 12 pages or less, and 4 weeks if longer. Reviewers recommend 2 weeks after all reviews are in, so plan on a few months, not weeks.
- **Risks:**
  - Less visible on an NLP resume than ACL main, unless it earns a certification, which is selective.
  - Reviewers can still ask for more models.
  - Nothing may be under parallel review at an archival venue, so TMLR and ARR are either/or.
- **Role:** the first choice if no designated contributor is available for ARR, or the fallback after weak ARR reviews.

### 3. COLM 2027 (deadline not announced; COLM 2026 was abstract Mar 26, paper Mar 31)

- **Why it fits:** the COLM 2026 call lists evaluation, the science of LMs, and LMs and the human mind as topics. COLM 2025 accepted judge-bias and verifier papers, for example *Assessing Judging Bias in Large Reasoning Models*. It is a well-regarded venue in the LM community. A late-March deadline would leave time for the frontier and thinking-mode runs.
- **Review time:** in the 2026 cycle, decisions came about 14 weeks after submission (Mar 31 to Jul 8).
- **Risks:**
  - The date is unconfirmed.
  - A paper may not be under review at another conference at the same time. So COLM is incompatible with a CogSci 2027 paper under review in March, and an ARR submission must be withdrawn first.
  - Each submission is expected to supply a reviewer.

### 4. CogSci 2027 (Bilbao, Jul 28–31, 2027; deadline not announced, CogSci 2026 closed Feb 2, 2026)

- **Why it fits:** this is the audience for the human comparison (conservative criteria, base-rate and payoff use against the ideal observer). The format is 6 pages, double-blind, with about 9 weeks from submission to notification in 2026. The society says its proceedings are not archival for journal purposes, so the work can later grow into a journal article, typically with at least 30% new material. Good journal follow-ups are Open Mind (free, diamond OA, decision expected within 1–2 months) and *Cognitive Science*. One 2027 program chair is at NYU.
- **Risks:**
  - Worth less than ACL or TMLR for ML or industry roles.
  - Reviewers expect the human SDT literature to be handled properly, with every citation verified.
  - Concurrency:
    - CogSci allows concurrent review at another conference.
    - ARR and COLM forbid it, so don't send overlapping full papers to CogSci and to ARR or COLM at the same time.
    - TMLR allows overlap with venues that declare themselves non-archival. That should make CogSci and TMLR compatible, but confirm with TMLR.
    - A 150-word CogSci member abstract (poster) is a low-overlap way to attend while the full paper is elsewhere. Check this too.

### 5. AAAI-27 workshop "Effective and Efficient Evaluation for AI Scientists" (Nov 20, 2026, 06:00 UTC): the fast first step

- **Why it fits:** its topics name LLM-as-a-judge reliability and calibration, and how sensitive results are to the judge, prompt and rubric. It is non-archival, so it blocks nothing later. Review is double-blind, full papers run 6–8 pages in the AAAI kit, notification is Dec 2, and the workshop is Feb 22, 2027 in Montréal. The four-model pilot is enough for it. It gives early feedback and a line on the resume within a month.
- **Risks:**
  - Two weeks of writing.
  - Travel and registration if accepted; AAAI-27 requires in-person presentation for the main proceedings, and workshop attendance rules were not checked.
  - A workshop paper counts for little on its own.

### Considered but not in the top five

- **ICML 2027** (Rio de Janeiro, Jul 31–Aug 6). The call is not posted; the 2026 deadline was Jan 28. It is a stronger resume line, but the novelty bar is higher. Its deadline falls about three weeks after ARR's, so pick one of the two.
- **NeurIPS 2027 Evaluations & Datasets track** (Europe; dates not announced; the 2026 deadline was May 6). Good scope for evaluation methodology, but a high bar, and it needs frontier models. A reasonable option if ARR doesn't work out.
- **TACL.** Monthly deadlines, free, 10 pages, and 45 days to first decision in 2020. It is a high bar, and papers that ARR or *ACL venues reject must wait 9 months before going to TACL.
- **IJCAI-27.** Jan 11, 2027, 7+2 pages, with a USD 100 fee unless no author appears on another IJCAI-27 submission. Weaker fit.
- **Royal Society Open Science Registered Report.** Fits only if C8 is pre-registered *before* running it, which conflicts with running it for ARR in December. RSOS took a median 19 days to first decision in 2025.
- **Nature Machine Intelligence / Nature Human Behaviour.** Stretch targets. First editorial decision is fast (10 and 6 days), but acceptance takes about 8 months, and the optional OA APC is about USD 12,850.
- **Behavior Research Methods.** Fits only as a methods or toolkit paper.
- **Computational Brain & Behavior, PNAS Nexus, Patterns, JAIR, Computational Linguistics, CoNLL, *SEM, BlackboxNLP.** Weaker fit or poor timing; details are in the CSV.

## Timeline, Nov 2026 – 2027

Plan A assumes a qualified designated contributor for ARR.

| When | Step |
|---|---|
| Now – Nov 19, 2026 | Write the 6–8 page workshop paper from the pilot (C1–C7). Create or complete OpenReview profiles with ORCID and DBLP for every author. Settle who the ARR designated contributor is, and apply early for manual verification if needed. Start the frontier and thinking-mode runs. |
| Nov 20, 2026, 06:00 UTC | Submit to AAAI-27 EvalAIScientists (non-archival). |
| By Dec 3, 2026 | Optional but sensible in a fast-moving area: post arXiv v1. ACL 2027's call forbids posting a deanonymized preprint in the month before submission, so post before Dec 4, or wait until after Jan 4. Don't update arXiv in between. |
| Dec 2, 2026 | Workshop notification. |
| Jan 4, 2027 | ARR submission for ACL 2027: 8 pages plus Limitations, at least one frontier model, C8 if ready. The designated contributor then reviews 5 papers in this cycle. |
| Feb 22, 2027 | Workshop in Montréal, if accepted. |
| ~mid-Mar 2027 (estimate) | ARR reviews, author response, meta-review. Commit to ACL 2027 (commitment date not yet announced) or withdraw and revise. |
| If withdrawing (Mar–Apr) | Submit to TMLR (rolling), or COLM 2027 if its deadline is again late March, or the next ARR cycle for EMNLP 2027 (early Nov 2027, Mexico or Central America; dates not announced). TACL stays closed for 9 months. |
| ~May 2027 | ACL 2027 notification (date not announced). |
| Jul 28–31, 2027 | CogSci 2027: a member abstract or poster, but only if it is compatible with where the full paper is under review. |
| Aug 17–22, 2027 | ACL 2027, Kyoto. |
| Late 2027 | Cognitive-science journal version (Open Mind or *Cognitive Science*) with a substantially new human-comparison contribution. |

**Plan B (no designated contributor, or Jan 4 is too tight):**

1. Submit to the workshop on Nov 20.
2. Post arXiv v1 whenever ready; TMLR allows this.
3. Submit to TMLR in Jan–Feb 2027, keeping the main text to 12 pages or less for the 2-week review window.
4. Optionally, send a 6-page CogSci 2027 paper focused on the human comparison (deadline probably early February) after confirming with TMLR that the overlap is acceptable.
5. If TMLR accepts the paper with a certification, request a Journal-to-Conference slot at NeurIPS 2027 or ICLR 2028; deadlines not announced. ICLR 2027's request deadline is Dec 18, 2026, too early for this paper.

COLM 2027 can replace TMLR in this plan, but then skip CogSci, because COLM forbids concurrent review.

## Rules to keep in mind

- **Preprints and anonymity at ARR.** The ARR call and ARR's anonymity page (policy of Jan 15, 2024) say there is no anonymity period: preprints may be posted at any time, and authors can opt into a binding no-preprint commitment. The ACL 2027 first call (posted Oct 6, 2026) adds a one-month no-preprint window before submission. Follow the stricter rule.
- **Who may submit to ARR.** A designated service contributor is required. Caps are 20 submissions per author and 5 as first author per cycle. A paper under review at ARR cannot be under review anywhere else that is refereed and archival, including archival workshops. Withdraw before resubmitting elsewhere.
- **Choosing a workshop.** Pick non-archival workshops. TACL, TMLR, NeurIPS, ICML, ICLR, AAAI, IJCAI and COLM explicitly allow overlap with non-archival workshops, and ARR's ban names only archival ones. Archival *ACL workshop papers count as prior publication.
- **ICLR.** Every submission, including rejected ones, stays public with author names after review, which matters for a first paper. Each author may have at most one paper in which no author is an eligible reviewer.
- **Per-venue paperwork:**
  - COLM: disclose LLM use.
  - ICLR: AI-use statement.
  - NeurIPS: checklist.
  - JAIR: reproducibility checklist.
  - BRM: Open Practices Statement.
  - Open Mind: code, data and AI statements.
  - PNAS Nexus: data and code in a public repository.
- **Cost.** None of the top five lists an APC (TMLR is explicitly free). Registration and travel apply to ACL, COLM, CogSci and AAAI; their fees were not checked.

## Gaps

- **Not announced as of Nov 6, 2026:**
  - Deadlines for COLM 2027, NeurIPS 2027, ICML 2027, ICLR 2028, AAAI-28, CogSci 2027, CoNLL 2027, *SEM 2027 and BlackboxNLP 2027.
  - The ACL 2027 commitment and notification dates.
  - ARR cycles after Jan 2027.
  - Workshop lists for ICLR, NAACL, ACL and ICML 2027.
  - The CSV gives last year's dates for reference.
- **Pages that returned 403 or couldn't be read:**
  - Wiley (*Cognitive Science* author guidelines; the 12,000-word limit comes from a search snippet).
  - cell.com (all of Patterns, including the USD 4,900 APC, which comes from snippets).
  - royalsocietypublishing.org (RSOS Registered Report policy and APC).
  - direct.mit.edu (Open Mind journal pages; its Janeway submission site was used instead).
  - pnas.org.
  - OpenReview forum pages, which sit behind a browser check; I didn't bypass it.
  - eScholarship pages, which are rendered by script.
  - Springer and Nature pages were read only through the publishers' cookie-free redirect. A curl attempt was blocked by the session's permission classifier and not retried.
- **Not verified on any official page:**
  - The PNAS Nexus APC (shown only in a calculator).
  - The RSOS APC.
  - The CoNLL 2026 call (seen only in mailing-list copies).
  - Review-type and preprint rules for BRM, CBB and Open Mind.
- **Review times.** Only TACL (2020 figures), Computational Linguistics (an old announcement), Nature Machine Intelligence, Nature Human Behaviour, RSOS and CBB publish statistics. For conferences I used their published cycle dates instead.
- **Inconsistencies on official pages:**
  - ARR's no-anonymity-period policy vs the ACL 2027 one-month rule.
  - ACL 2027 workshop days: Aug 18–19 on the ACL 2027 site, Aug 21–22 in the joint workshop call.
  - The ICLR 2027 workshop call says "2026", apparently a typo.
- **Example papers.** These were found through searches limited to official domains. Six pages were checked directly: the COLM 2025 accepted list, the TMLR paper list, the Findings of EMNLP 2025 paper, the PNAS Nexus 2025 paper, the ICLR 2026 poster and the CogSci FAQ pages. The other examples rely on titles and URLs from the venues' own domains.
- **Raw data.** No raw files were saved under `../raw/venues/`, because no API was used and WebFetch returns summaries. No instructions aimed at LLM readers were seen in any fetched page.
- **Re-verify before each submission.** Policies changed in 2026: the ARR sustainable reviewing policy, the ICLR caps and the ACL 2027 preprint rule.

## Spot-check by the main session (2026-11-06)

Re-read on the official pages in the browser:
- AAAI-27 EvalAIScientists (eval-ai-scientists.github.io/aaai27): submission 20 Nov 2026, 06:00 UTC; workshop 22 Feb 2027; full papers 6–8 pages (references excluded) in the AAAI-27 two-column kit; double-blind via OpenReview; non-archival; in person; LLM-as-a-judge reliability and calibration listed in scope; papers comparing systems must report at matched compute and token budget or explain why not.
- ACL 2027 first call (aclweb.org): ARR deadline 4 Jan 2027; commitment TBD; "no deanonymized preprint may be posted in the month prior to submission."
- ARR CfP (aclrollingreview.org/cfp): from October 2026, the sustainable reviewing policy applies; review is guaranteed only for submissions that name a qualified service contributor (max 2 submissions per contributor); others enter a lottery, and those not drawn are desk-rejected. The qualification criteria (which venues count, including CVPR/ICCV/ECCV/TPAMI) come from the ACL sustainable reviewing policy page as read by this stream; the main session could not reopen that page.
