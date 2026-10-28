# Decision log (rebuilt 2026-10-27; original lost in the import)
- 2026-10-23: Killed dementia caregiver segment (free Medicaid help + legal-advice risk).
- 2026-10-26: Dropped pet-business software; rejected Jobber and HighLevel marketplace pivots.
- 2026-10-26: Horizon Report Vault test paused (Horizon shuts down Dec 15, 2026). Chief Of Staff recommends kill (Google Drive is a free substitute); awaiting Matteo.
- 2026-10-27: Amazon returns - shopper pickup killed (live handoffs, driver logistics); seller reimbursement parked (crowded, 25% contingency rivals, $19/mo tool exists).
- 2026-10-27: Kept the original Cooper team; imported duplicates removed.
- 2026-10-27: Videos analysed and killed: AI creative freelancing (20/50), rank-and-rent phone version (25/50), AI agency (16/50), AI employees/templates (15/50), SaaS clones (23/50; pre-sell method kept).

## 2026-10-27 — Chief of Staff mandate and minimum team
Decision: CoS owns missions end to end. Mission team = CoS + Cooper Researcher + Cooper Critical Reviewer. Systems Engineer stays outside the mission (maintains Cooper software only). Correct MSG proposed for removal (CoS rewrites messages reliably; skill casual-american-english-message-rewrite exists). Builder created only after a test passes.
Why: Matteo t99u-t101u. Each kept role needs different context (high-volume sourcing) or independence (review). Status: Correct MSG removal awaits Matteo; only he can delete bots.

## 2026-10-27 — Rule corrections from Matteo (t102u)
Budget not $0, spend discussed first; Correct MSG off team (grammar only); written cold outreach allowed (email, text, social posts), no live calls; ask Matteo for logins when needed; credit limits never stop a job.

## 2026-10-27 — CoS is coordinator only (t104u)
Decision: CoS stops drafting/scoring itself; scoring moves to Researcher (checked by Reviewer); test design, page, copy and outreach go to one Builder/Growth specialist created only at stage 4 GO. Status tracked in STATUS.md; "done" needs evidence.

## 2026-10-27 — Decision ladder adopted (t106u)
Bot decides reversible internal; CoS decides verified technical; Matteo decides irreversible/consequential. Unsure means one level up.

## 2026-10-27 — Horizon Report Vault: KILLED (Matteo, t107u)
Was paused since 2026-10-26 (no drafts/posts/emails). CoS had recommended kill. Files kept, no work continues; reopen only if Matteo asks.

## 2026-10-27 — Team growth rule (t112u)
Core four seats; split only on proven bottleneck; target hierarchy recorded in RULES.md. No new bots now: no seat is a bottleneck.

## 2026-10-27 — Context rule (t113u)
Task briefs with file pointers instead of shared conversation; workers get the smallest useful context.

## 2026-10-27 — Pipeline adopted (t114u)
Matteo diagram adopted with two changes: approval moved before Ship for irreversible steps; retry capped at 2 changed attempts then BLOCKED.

## 2026-10-27 — CNBC Ryan Hogue POD article (t116u): PARK
Unverified self-reported $49k/mo across 10+ streams incl. YouTube + course (personal brand). POD fails price filter except brand route; already covered by queue item golf apparel (#15). Note for that item: POD = $0 inventory way to test a brand. No new task.

## 2026-10-27 5:03 PM CT: v3 profile conflicts resolved (Matteo, t120u)
- Kept everything built today. Business scope is US only (Italy dropped from v3).
- Bots: use as many as the work needs; new bot when a role is a real bottleneck (replaces "default to one agent").
- Chief Of Staff is a generalist coordinator and does no research; research, analysis and building go to specialists.
- Profile updated; previous text backed up at /workspace/desc_backup_2026-10-27.txt.

## 2026-10-27 5:18 PM CT: Cooper 3.0 on Grok (Matteo, t123u)
- Matteo: "now that we moved everything here to Grok, we are going to build Cooper AI Ver 3.0".
- Chief call: the audit becomes the parts list for 3.0 (port / keep on PC / drop). The old WSL stack stays running and untouched until 3.0 covers its functions.
- Dashboard facts (5:18 PM CT): services up; newest run Oct 19, newest job Oct 16; operator idle with 2 approvals stuck since Oct 8; Command API restarted ~hourly by watchdog; /operator/enabled and n8n cooper-dashboard webhook return 500. Proposal: 3.0 dashboard = one Grok Page built from STATUS.md.

## 2026-10-27 5:19 PM CT: OpenClaw dropped from 3.0 (Matteo, t124u)
- 3.0 uses Grok bots instead of OpenClaw (gateway, sandbox, openai/gpt-5.6-sol config). The old stack keeps running until 3.0 covers it; switch-off is one approval for Matteo, after a backup of ~/.openclaw (7 GB).

## 2026-10-27 5:22 PM CT: Cooper 3.0 from scratch (Matteo, t125u)
- Matteo is fine tossing the old Cooper. Decision: rebuild 3.0 from scratch on Grok; carry over only the judgment rules and lessons. Audit rescoped to SE-01_keep.md + SE-01_shutdown.md. Nothing is stopped or deleted without Matteo approving the shutdown list; backups first.

## 2026-10-27 5:33 PM CT: Cooper 3.0 target and cadence (Matteo)
- Target: at least 1 paid deposit from a real customer by Dec 26, 2026 (60 days). Miss = Matteo reviews whether Cooper continues.
- Daily research stays as is (Reviewer had proposed weekly); findings must pass the gate before scoring.

## 2026-10-27 5:47 PM CT: 3.0 stages 0 and 1 verified
- Gate v57 ported to tools/cooper_gate.py; 18/18 self tests (Chief re-ran) and 2/2 sealed blind cases (Reviewer). Checks consistency, not truth.
- Deviation accepted: missing failure path = INVESTIGATE, not REJECT.
- Files the Reviewer thought lost (tracker.csv, old reviews) were never imported; they are on the old Grok web account computer (README-imported.md). Not a new loss.

## 2026-10-27 6:29 PM CT: Old-Cooper shutdown plan frozen
- SE-01 v3.1 passed independent review (conditions C1-C6 are fail-closed checks run on the PC). No v3.2: the remaining notes are non-blocking. Running it needs Matteo per stage, his off-PC choice and the gpg passphrase. Deletion (S12) is separate, at least 30 days later.
- 2026-10-27 10:11 PM: Matteo declined Gmail search for old files; Researcher rebuilds killed-ideas list from notes (KIL-01). SE runbook notes delivered: /workspace/cooper/audit/artifacts/SE-01_RUNBOOK-NOTES.md.
- 2026-10-27 10:14 PM: KIL-01 done. killed-ideas.md has 42 rows (sha 3b2e2dc8…7d6); the old v45/46 memory and runner scripts added no kills. The old tracker's round 1-3 rows can't be recovered.
