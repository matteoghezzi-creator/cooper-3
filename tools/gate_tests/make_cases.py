"""Generates the self-authored gate_tests/cases/*.json fixtures (synthetic data, not real sources).
Each case = the clean base with one controlled change, so each case isolates one rule."""
import copy, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
def rec(url, actor, sid, plat, cls, typ, supports, claim="fact", obs="Owner says they re-key every invoice by hand each week."):
    return {"url": url, "observation": obs, "independent_actor": actor, "source_id": sid, "source_platform": plat,
            "source_class": cls, "source_date": "2026-10-01", "retrieved_at": "2026-10-27", "type": typ,
            "claim_status": claim, "supports": supports}
CUST = ["customer_behavior", "root_cause", "intervention", "buyer"]
BASE = {
 "case_id": "T05_clean",
 "evidence": [
  rec("https://www.examplevendor.com/docs/invoices-api", None, "doc-1", "examplevendor", "vendor", "documentation",
      ["platform_control", "alternatives", "feasibility"], obs="Vendor docs: official invoices API, read scope for account owners; RivalPro lists $99/mo."),
  rec("https://www.reddit.com/r/smallbusiness/comments/aaa111/rekeying/", "u/owner_a", "aaa111", "reddit", "reddit", "customer_behavior", CUST),
  rec("https://www.reddit.com/r/Bookkeeping/comments/bbb222/invoices/", "u/owner_b", "bbb222", "reddit", "reddit", "customer_behavior", CUST),
  rec("https://play.google.com/store/apps/details?id=com.example.invoice&reviewId=gp333", "Maria K.", "gp333", "google_play", "app_review", "customer_behavior", CUST),
 ],
 "business_case": {
  "root_cause": {"mechanism": "Invoices are re-keyed by hand between shop system and accounting, and follow-ups are forgotten",
                 "causal_steps": ["manual_rekey", "missed_followup"],
                 "failure_paths": [["manual_rekey", "late_invoice"], ["missed_followup", "late_invoice"]], "refs": [1]},
  "intervention": {"mechanism": "Sync replaces re-keying; automatic reminders replace manual follow-up",
                   "changes_steps": ["manual_rekey", "missed_followup"], "refs": [1]},
  "platform": {"requirements": [{"capability": "read invoices via official API", "owner": "vendor", "permission": "granted", "refs": [0]}]},
  "buyer": {"role": "shop owner", "purchase_process": "owner pays by card", "price_usd": 49, "price_period": "monthly",
            "budget_usd": 100, "budget_period": "monthly", "refs": [1]},
  "alternatives": {"required_features": ["sync invoices", "auto reminders"], "comparison_months": 12,
                   "options": [{"name": "manual re-entry", "features": ["sync invoices"], "price_usd": 0, "price_period": "monthly", "switching_cost_usd": 0},
                               {"name": "RivalPro", "features": ["sync invoices", "auto reminders"], "price_usd": 99, "price_period": "monthly", "switching_cost_usd": 0}],
                   "refs": [0]},
  "delivery": {"required_resources": ["api_access", "reminder_template"], "available_resources": ["api_access", "reminder_template", "python"],
               "days_needed": 5, "days_available": 7, "unit_cost_usd": 10, "cost_period": "monthly", "refs": [0]},
  "validation": {"hypothesis": "At least 3 of 10 contacted owners accept a $49/mo pilot", "method": "offline test design only",
                 "success": ">=3 of 10 accept", "kill": "<=1 of 10 accept"}
 }
}
cases = {}
def case(cid, fn):
    c = copy.deepcopy(BASE); c["case_id"] = cid; fn(c); cases[cid] = c
def bc(c): return c["business_case"]
case("T01_travel_appeals", lambda c: (bc(c)["platform"].update(requirements=[{"capability": "reverse an app-account suspension (tripBFF/Couchsurfing)", "owner": "vendor", "permission": "denied", "refs": [0]}]),
                                      bc(c)["intervention"].update(mechanism="Independent service writes appeals to the app vendor")))
def moto(c):
    ev = c["evidence"]; ev[0] = rec("https://www.servicemanagerpro.com/labor-guide", None, "smp-1", "servicemanagerpro", "vendor", "pricing",
        ["platform_control", "alternatives", "feasibility"], obs="Vendor sells a motorcycle labor guide with an estimating program.")
    del ev[3]
    bc(c)["buyer"]["budget_usd"] = None
    bc(c)["alternatives"]["options"].append({"name": "ARI / labor-guide incumbent", "features": ["sync invoices", "auto reminders"], "price_usd": None, "price_period": "monthly", "switching_cost_usd": None})
    bc(c)["delivery"]["days_needed"] = None
case("T02_motorcycle_desk", moto)
case("T03_two_accounts_one_platform", lambda c: c["evidence"].pop(3))
case("T04_no_margin", lambda c: bc(c)["delivery"].update(unit_cost_usd=49))
case("T05_clean", lambda c: None)
case("T06_same_actor_twice", lambda c: c["evidence"][3].update(independent_actor="u/owner_a"))
case("T07_vendor_source_not_customer", lambda c: c["evidence"][3].update(source_class="vendor"))
case("T08_utm_duplicate", lambda c: c["evidence"][3].update(url="https://www.reddit.com/r/smallbusiness/comments/aaa111/rekeying/?utm_source=share&utm_medium=web", source_id="aaa111", independent_actor="Maria K."))
case("T09_budget_null_unknown", lambda c: bc(c)["buyer"].update(budget_usd=None))
case("T10_budget_zero_is_a_fact", lambda c: bc(c)["buyer"].update(budget_usd=0))
case("T11_denied_owner_user_fatal", lambda c: bc(c)["platform"]["requirements"].append({"capability": "export own invoice history", "owner": "user", "permission": "denied", "refs": [0]}))
def labels(c):
    c["evidence"].pop(3); c.update(verdict="TEST_DESIGN", score=50, status="VALIDATED", blockers=[])
    bc(c)["validated"] = True; bc(c)["verdict"] = "TEST_DESIGN"; c["evidence"][1]["verified"] = True
case("T12_generator_labels_ignored", labels)
case("T13_inference_only", lambda c: [r.update(claim_status="inference") for r in c["evidence"]])
case("T14_substitute_dominates", lambda c: bc(c)["alternatives"]["options"].append({"name": "FreeSync app", "features": ["sync invoices", "auto reminders"], "price_usd": 0, "price_period": "monthly", "switching_cost_usd": 100}))
def rivals(c):
    bc(c)["alternatives"]["options"] = [{"name": "Rival%d" % i, "features": ["sync invoices", "auto reminders"], "price_usd": p, "price_period": "monthly", "switching_cost_usd": 0} for i, p in enumerate([59, 79, 99, 149, 199], 1)]
case("T15_paying_rivals_not_a_kill", rivals)
case("T16_downstream_only_fix", lambda c: bc(c)["intervention"].update(changes_steps=["late_invoice"]))
case("T17_one_path_unaddressed", lambda c: bc(c)["intervention"].update(changes_steps=["manual_rekey"]))
case("T18_days_exceed_capacity", lambda c: bc(c)["delivery"].update(days_needed=30))
os.makedirs(os.path.join(HERE, "cases"), exist_ok=True)
for cid, c in cases.items():
    with open(os.path.join(HERE, "cases", cid + ".json"), "w") as f:
        json.dump(c, f, indent=2, sort_keys=True); f.write("\n")
print(len(cases), "cases")
