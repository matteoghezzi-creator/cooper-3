# Cooper 3.0 evidence file schema: input to `cooper_gate.py` (gate v57 port)
Version: 1 (2026-10-27, Cooper Systems Engineer). Source rules: `/workspace/cooper/audit/cooper_audit/runner/cooper_business_judgment_v56.py` (v57 inside, contract at lines 10-50, rules at 52-288) and `/workspace/cooper/audit/artifacts/SE-01_keep.md` A1-A11.
Status: the schema is final for stage 1. The script `/workspace/CooperAI2/tools/cooper_gate.py` is being written to this spec. Until it ships, treat this file as the contract.

## File format
One UTF-8 JSON object per file. Unknown keys are ignored. **Any verdict, score, "validated" label or blocker list written by the researcher is ignored (rule A1).** That includes keys such as `verdict`, `score` and `status`, and any free text. Unknown values must be `null` (or omitted), **never 0 or ""** (A11). The strings `""`, `"unknown"`, `"n/a"`, `"tbd"` and `"none"` count as missing. Numbers must be JSON numbers that are finite and ≥ 0. Booleans and numeric strings are not numbers. Amounts are USD.

```
{
  "case_id": "string, for reporting only",
  "evidence": [ <evidence record>, ... ],      // zero-based indices are used by "refs"
  "business_case": {
    "root_cause":   {"mechanism": str, "causal_steps": [str], "failure_paths": [[str, ...], ...], "refs": [int]},
    "intervention": {"mechanism": str, "changes_steps": [str], "refs": [int]},
    "platform":     {"requirements": [{"capability": str, "owner": "user|vendor|third_party",
                                       "permission": "granted|denied|unknown", "refs": [int]}]},
    "buyer":        {"role": str, "purchase_process": str, "price_usd": num, "price_period": P,
                     "budget_usd": num, "budget_period": P, "refs": [int]},
    "alternatives": {"required_features": [str], "comparison_months": int 1-120,
                     "options": [{"name": str, "features": [str], "price_usd": num, "price_period": P,
                                  "switching_cost_usd": num}], "refs": [int]},
    "delivery":     {"required_resources": [str], "available_resources": [str], "days_needed": num,
                     "days_available": num, "unit_cost_usd": num, "cost_period": P, "refs": [int]},
    "validation":   {"hypothesis": str, "method": str, "success": str, "kill": str}
  }
}
P = "monthly" | "annual" | "one_time"
```

### Evidence record
| Field | Meaning |
|---|---|
| `url` | Direct link to the single item (post, review, page). Must be http/https with a host and no user:password. Collection pages (`/reviews`, `/pricing`, `/help`, `/support`, `/category`, `/categories`, `/search`, `/apps`, `/products`) are rejected. |
| `observation` | Non-empty text saying what the source shows. |
| `independent_actor` | Who said or did it (username or reviewer). Use null if not attributed. |
| `source_id` | Stable id of the item within its platform (post id, review id). |
| `source_platform` | e.g. `reddit`, `google_play`, `apple_app_store`, `shopify_community`. |
| `source_class` | Customer classes: `reddit`, `forum(s)`, `app_review(s)`, `marketplace_review(s)`, `customer_interview(s)`, `customer_support`, `support_community`. Other classes (e.g. `vendor`, `docs`, `news`) can support other dimensions but never count as customers. |
| `source_date` | Date of the item, or null. |
| `retrieved_at` | ISO date `YYYY-MM-DD` the researcher opened it. **Required.** A record without it is excluded. |
| `type` | `customer_behavior` for individual customer accounts, otherwise free text (e.g. `pricing`, `documentation`). |
| `claim_status` | `fact`, `inference` or `hypothesis`. Only `fact` can support anything. |
| `supports` | List of dimensions this record backs: `customer_behavior`, `root_cause`, `intervention`, `platform_control`, `buyer`, `alternatives`, `feasibility`. |

**`refs` rule:** a section counts as cited only if `refs` is a non-empty list of valid indices. Every referenced record must pass the URL check, be `claim_status: "fact"`, have a valid `retrieved_at`, and list that section's dimension in `supports`. The dimension for `root_cause` is `root_cause`; `intervention` → `intervention`; each platform requirement → `platform_control`; `buyer` → `buyer`; `alternatives` → `alternatives`; `delivery` → `feasibility`.

## How the verdict is computed (deterministic)
Each dimension is scored `fatal`, `unknown` or `supported`. **Any fatal finding gives REJECT. Otherwise any unknown gives INVESTIGATE. Only when every dimension is supported does the result become TEST_DESIGN**, which permits planning a test and nothing else.
- **customer_evidence** (A3): requires ≥3 distinct attributed customer accounts across ≥2 platforms, else unknown. A record counts only if its URL passes the check, it is `fact`, it has `type` `customer_behavior` with `customer_behavior` in `supports`, it has a named actor, a `source_id`, a platform, a customer `source_class`, and a valid `retrieved_at`. Duplicates are dropped: same canonical URL+source_id (utm/gclid/fbclid stripped, scheme/port/trailing slash normalised), same platform+source_id, or the same actor seen again.
- **root_cause** (A5): needs both mechanisms, `changes_steps`, well-formed `failure_paths` and `causal_steps`, and every path must contain a causal step; otherwise unknown. If the intervention changes no causal step on any path, that is **fatal**. If it misses a causal step on some path, or the citations are missing, that is unknown.
- **platform_control** (A6): any requirement with `permission: "denied"` is **fatal** (e.g. only the vendor can perform the action). A requirement that is not `granted`, has an unclear owner or is uncited is unknown. An empty list is unknown.
- **buyer** (A7): price > budget in the same period is **fatal**. A missing role, process, price (>0), budget, matching periods or citation is unknown.
- **alternatives** (A8): an option whose `features` cover every `required_features` item at total cost (price over `comparison_months` + switching cost) ≤ the proposed price over the same horizon is **fatal**. Incomplete comparison data is unknown.
- **feasibility** (A9): `days_needed > days_available` is **fatal**. `unit_cost_usd ≥ price_usd` in the same period (no gross margin) is **fatal**. Missing resources (required ⊄ available), estimates, period match or citation is unknown.
- **validation** (A10): all of hypothesis/method/success/kill must be filled, else unknown.

The output always contains `build_authorized: false`, `external_action_authorized: false`, `source_truth_verified: false` and `purchase_intent_verified: false`, plus the A3 counts. **The gate checks structure and consistency only. It does not open sources or verify that anything is true.**

## Minimal example (shape only; see the note below it for the expected verdict)
```json
{
  "case_id": "EXAMPLE-shape-only",
  "verdict": "VALIDATED (ignored by the gate)",
  "evidence": [
    {"url": "https://www.reddit.com/r/example/comments/abc123/title/", "observation": "Owner says they spend 3 hours a week re-keying invoices.",
     "independent_actor": "u/example_owner", "source_id": "abc123", "source_platform": "reddit", "source_class": "reddit",
     "source_date": "2026-09-30", "retrieved_at": "2026-10-27", "type": "customer_behavior", "claim_status": "fact",
     "supports": ["customer_behavior", "root_cause", "buyer"]}
  ],
  "business_case": {
    "root_cause": {"mechanism": "Manual re-entry between two systems", "causal_steps": ["manual_rekey"],
                   "failure_paths": [["manual_rekey", "late_invoices"]], "refs": [0]},
    "intervention": {"mechanism": "Automated sync replaces re-entry", "changes_steps": ["manual_rekey"], "refs": [0]},
    "platform": {"requirements": [{"capability": "read invoices via API", "owner": "vendor", "permission": "unknown", "refs": [0]}]},
    "buyer": {"role": "shop owner", "purchase_process": "owner pays by card", "price_usd": 49, "price_period": "monthly",
              "budget_usd": null, "budget_period": "monthly", "refs": [0]},
    "alternatives": {"required_features": ["sync invoices"], "comparison_months": 12,
                     "options": [{"name": "manual re-entry", "features": ["sync invoices"], "price_usd": 0, "price_period": "monthly", "switching_cost_usd": 0}],
                     "refs": [0]},
    "delivery": {"required_resources": ["api_access"], "available_resources": [], "days_needed": null, "days_available": 7,
                 "unit_cost_usd": null, "cost_period": "monthly", "refs": [0]},
    "validation": {"hypothesis": "", "method": "", "success": "", "kill": ""}
  }
}
```
(In this example the manual option costs $0, which is ≤ $49×12, so alternatives would be **fatal** if the comparison were complete. That makes this example REJECT, not INVESTIGATE. This illustrates A8. Exact output will be confirmed when the script runs.)

## CLI
- `python3 /workspace/CooperAI2/tools/cooper_gate.py evaluate <file.json>`: prints the result JSON to stdout. Exit 0 = evaluated. Exit 2 = file unreadable or not a JSON object.
- `python3 /workspace/CooperAI2/tools/cooper_gate.py run-dir <dir>`: evaluates every `*.json` in a directory, sorted by name, and prints `{file: result}`.
- Runs are deterministic: the same input gives byte-identical output.

## Blind cases (Critical Reviewer only)
- Put them in `/workspace/CooperAI2/tools/gate_tests/blind/`, one case per file, named `BLIND-<nn>_<short-slug>.json` (e.g. `BLIND-01_x.json`).
- The file holds **only** the input above. Do not put the expected answer in this directory. Keep it in your own sealed file outside `tools/` and record its sha256 first, so the order can be shown.
- They will be run with `python3 /workspace/CooperAI2/tools/cooper_gate.py run-dir /workspace/CooperAI2/tools/gate_tests/blind/`. Systems Engineer reports the raw output without guessing, and the Reviewer compares it with the sealed answers.
