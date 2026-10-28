# Cooper 3.0 — design draft (Chief Of Staff, 2026-10-27, NOT approved, not built)
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

## Build stages (each: owner, acceptance, rollback)
1. Gate skill + validator (Systems Engineer; Reviewer verifies). Accept: on 3 test files it gives REJECT for the travel-appeals case, INVESTIGATE for the motorcycle desk, INVESTIGATE for a seeded file with 2 accounts on 1 platform. Rollback: delete the skill (internal).
2. Evidence schema + Researcher brief template (Systems Engineer). Accept: Researcher produces one valid file on a live question.
3. Status Page (Chief). Accept: Page matches STATUS.md item for item.
4. Move daily research routine to the Researcher (Chief). Accept: one run delivers with the run-log line.
5. Retire the old stack on the PC per SE-01_shutdown.md after CR-01 PASS. Needs Matteo's approval; backups first.
Not rerunning the Shopify case.
