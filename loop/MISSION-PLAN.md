# Mission plan (draft, not executed) — 2026-10-27
Mission: find one US online business with recurring revenue (or >$100/purchase), validate it as cheaply as possible (any spend discussed with Matteo first), and reach the first paying customer. Channels: inbound plus cold outreach by email, text or social posts; no live sales calls.

## Team (smallest that completes it)
### Chief Of Staff
- Role: mission owner and coordinator; does no specialist work.
- Inputs: Matteo's requests, RULES.md, decision-log, specialist handoffs.
- Actions: break goal into tasks, map dependencies, route work, track STATUS.md, require evidence, send to Reviewer, keep decision log.
- Output: plans, status board, 5-line reports, approval requests.
- Tools: files, web search, nopaywall, memory, routines.
- Constraints: no send/publish/spend/delete/contact/new sign-in/production change without Matteo.
- Acceptance: every claim sourced or labeled; nothing unfinished reported as done.
- Handoff: Matteo (approvals, results); Researcher; Reviewer.
### Cooper Researcher
- Role: evidence sourcing and segment screening.
- Inputs: one segment or hypothesis + kill gate + question from CoS.
- Actions: mine complaints, rival matrix, pricing, existing spend, cross-check sources.
- Output: evidence file with links and labels; 5-dimension score draft.
- Tools: web search/fetch, X reads, TubeAlfred, vidIQ (capped 20/day, 60/Monday).
- Constraints: read-only, licensed data, no scraping behind logins, no contact.
- Acceptance: 3+ independent sources on pain AND on existing payment; every line labeled.
- Handoff: CoS.
### Cooper Critical Reviewer
- Role: independent verification.
- Inputs: raw evidence file + proposed decision (not CoS's reasoning).
- Actions: six-gate review, premortem, red-team test designs and results.
- Output: GO / HOLD / KILL with reasons first.
- Tools: files, web for spot checks.
- Constraints: no new research beyond spot checks; no edits to evidence.
- Acceptance: each gate passed/failed with a cited line.
- Handoff: CoS.

Not on team: Correct MSG (grammar only). Out of scope: Systems Engineer (Cooper software only). Deferred: one Builder/Growth specialist, created when stage 4 says GO (test design, page, copy, outreach drafts, later MVP).

## Stages
1. Contract — CoS fixes goal, budget (proposed to Matteo), pass/fail metric, deadline.
2. Screen — Researcher screens 3-5 segments through kill gate.
3. Evidence + score — Researcher deepens top 1-2 and scores; Reviewer checks scores; only >=35/50 continue.
4. Independent review — Reviewer GO/HOLD/KILL.
5. Test design — Builder/Growth specialist (created at this stage) drafts preregistered test (landing page + pre-sale/waitlist with price); Reviewer red-teams.
   GATE A (Matteo): approve test, any new account, any spend.
6. Assets — Builder/Growth specialist drafts page and copy; Reviewer checks claims. GATE B (Matteo): publish.
7. Reach — inbound plus cold email/text/social posts; CoS asks Matteo for needed logins. GATE C (Matteo): every outreach message.
8. Read result — Reviewer red-teams numbers vs preregistered bar. GATE D (Matteo): pursue / park / kill.
9. Build MVP — create Builder; reuse/no-code first. GATE E (Matteo): spend, deploy, payments setup.

## Failure points
- Reach: cold email/text/social now allowed, but deliverability, spam rules (CAN-SPAM, TCPA for texts) and platform bans are the risk; set minimum reach bar in stage 1.
- Signal confusion: complaints and views mistaken for willingness to pay.
- Score inflation by CoS; Reviewer anchored if handed CoS's reasoning.
- Access limits: login walls (ask Matteo for logins); credit caps never stop a job, switch to free sources.
- Approval stalls: unattended runs skip gated steps; mission waits on Matteo.
- Payments/accounts need sign-ins -> blocked until Matteo approves.
- Lost context: import already wiped files once; keep backups of loop/.
