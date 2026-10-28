# Cooper 3.0 — design draft v2 (Chief Of Staff, 2026-10-27, after CR-02 'Not yet'; NOT approved, not built)
Goal: find one US online business with recurring revenue (or >$100 purchases), validate it cheaply, get the first paying customer. 3.0 is judged only by verified findings, paying customers and profit.

## Why from scratch
Old Cooper (v1–v58, ~6 weeks): 5 always-on WSL services, OpenClaw agents, n8n, Postgres (~50 tables) + SQLite (25 tables), a 338 KB dashboard. Last model run Oct 19; 5 of last 10 missions failed; operator idle on two Oct 8 approvals; the main mission path skipped its own judgment gate (SE-01_keep D5). Worth keeping: the judgment rules, not the machinery.

## Shape: hybrid, small
| Seat | Bot | Owns | Never does |
|---|---|---|---|
| Coordinator | Chief Of Staff | task graph, briefs, checking artifacts, reports, approvals queue | research, building |
| Evidence | Cooper Researcher | bounded scans, evidence files (schema below), daily research routine | judge its own findings (rule A1) |
| Gate + verify | Cooper Critical Reviewer | runs the gate on evidence files, PASS/FAIL on every "done" | fix what it reviews |
| Build | Cooper Builder | tests and MVPs after a GO + Matteo approval | declare its own work verified |
| Maintenance | Cooper Systems Engineer | 3.0 skills, validator script, retiring the old stack | business research |
No new bots. Split a seat only when it becomes a bottleneck.

## Replacements (old → 3.0)
| Old | 3.0 |
|---|---|
| cooper-runner / command center / specialist + business APIs | bots + briefs (no servers) |
| OpenClaw gateway + gpt-5.6-sol agents | Grok bots |
| operator loop every 60 s + watchdog | 3 routines: daily research (Researcher), Monday loop, weekday check-in |
| Postgres + SQLite | plain files in /workspace/CooperAI2/loop (STATUS.md, decision-log.md, opportunities/<id>/evidence.json, approvals.md) |
| dashboard 8080 | one Grok Page built from STATUS.md, refreshed by the check-in |
| n8n webhooks | none needed |
| gate v57 inside the operator | skill "cooper-gate" + small validator script that enforces counts in code (B1, A3) |

## Data flow
Matteo → Chief (brief + pass/fail criteria) → Researcher (bounded scan, ≤4 searches/≤8 pages; writes evidence.json) → validator script (counts, dedupe, unknown→null) → Reviewer runs gate: REJECT / INVESTIGATE / TEST_DESIGN → Chief logs decision, updates STATUS.md and the Page → Matteo approves anything external/spend → Builder → Reviewer verifies → ship.
Evidence passes by file path, never "recent rows" (D4). One gate on every path (D5). One timeout owner: the routine/brief (D1).

## Rules carried over (SE-01_keep.md)
A1 gate ignores generator verdicts; A2 unknown is not pass; A3 ≥3 attributed customers on ≥2 platforms; A4 source hygiene; A5–A9 fatal kills (root cause, platform control, budget, substitute, no margin, no time); A10 pre-set success and kill thresholds; A11 unknown stays null; C1 nothing is an approval except Matteo; C2 approval bound to a hash of the exact payload; D12 no state changes on reads.

## Honest limits
- Budgets in prompts aren't hard enforcement (C5). Grok routines limit runtime, and the run log plus the check-in catch overruns, but per-tool-call caps are not enforced by code.
- The validator checks structure, not truth. The Reviewer still opens sources.
- 3.0 has never been tested on a real case yet.

## Rule order (fixes CR-02 #5)
1. Gate v57 (REJECT / INVESTIGATE / TEST_DESIGN) runs first on every case, including videos and articles Matteo sends.
2. Only TEST_DESIGN cases get the 5-dimension score (pass at 35/50).
3. Consequential calls (validate, build, kill, spend) also get the six-gate review.
Usage limit on a call = don't retry that call in a loop; the job continues on free sources and logs the shortfall (consistent with "credits never stop a job").
Approvals expire after 7 days: then closed as "expired" and re-asked only if still needed. Every approval is tied to a hash of the exact payload.

## Business target (APPROVED by Matteo, 2026-10-27 5:33 PM CT)
At least 1 paid deposit from a real customer within 60 days of 3.0 going live (by Dec 26, 2026). Miss = Matteo reviews whether Cooper continues.

## Build stages (each: owner, acceptance, rollback)
0. Safety net (Systems Engineer). Daily versioned backup of loop/ to E:\CooperAI2 plus one restore test. Accept: a deleted test file is restored from backup. Rollback: remove the backup job.
1. Port gate v57 code as the validator (Systems Engineer; Reviewer verifies). Not an LLM skill. Accept: ≥8 test cases with expected outcomes fixed in advance, including at least 1 blind case written by the Reviewer, all correct; any wrong = FAIL. Rollback: delete the script.
2. Evidence schema + Researcher brief template. Accept: one live question produces an evidence file that passes the validator AND the Reviewer opens 3 sources and confirms them. Rollback: previous brief template kept.
3. Research cadence: daily research stays as is (Matteo, 2026-10-27). Its findings go through the gate before any score or verdict. Accept: next daily run leaves a run-log line and its daily note on disk; the check-in verifies both.
4. One real case through the gate to a pre-registered test, then Matteo's approval for any outreach. Accept: test design with success/kill thresholds signed off by the Reviewer.
5. Status Page, only after stage 4 passes. Accept: Page matches STATUS.md item for item.
R. Retire the old stack on the PC per SE-01_shutdown.md once CR-01 passes. Priority: Postgres (55432) and n8n (5678) listen on all network interfaces, and an unauthenticated API can arm a Vercel deploy. Needs Matteo's approval; backups first.
Not rerunning the Shopify case.
