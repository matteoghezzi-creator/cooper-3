#!/usr/bin/env python3
"""cooper_gate.py: Cooper 3.0 deterministic evidence gate (port of old Cooper gate v57).

Source: /workspace/cooper/audit/cooper_audit/runner/cooper_business_judgment_v56.py (v57, lines 52-288).
Contract: /workspace/CooperAI2/tools/evidence_schema.md. Standard library only.

It checks STRUCTURE AND CONSISTENCY of supplied facts only. It never opens a source, never
verifies truth, never calls a network, model, database or subprocess, and never executes
anything. Generator verdicts, scores and labels in the input are ignored (rule A1).
Verdicts: any fatal -> REJECT; else any unknown -> INVESTIGATE; else TEST_DESIGN (plan a test only).

CLI:
  cooper_gate.py evaluate <file.json>            result JSON; exit 0, or 2 on unreadable / non-object input
  cooper_gate.py run-dir <dir>                   {file: result} for every *.json (sorted); exit 2 if any file bad
  cooper_gate.py approval-hash <file.json>       prints the binding hash an approval must quote
  cooper_gate.py verify-approval <file.json> <h> exit 0 if <h> equals the current binding, else 1.
                                                 A match only proves the approval refers to this exact
                                                 input and verdict; it authorizes and runs nothing.
"""
import hashlib, json, math, os, sys
from datetime import date
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

GATE_VERSION = "v57-port-1"
PERIODS = {"monthly", "annual", "one_time"}
COLLECTION_PATHS = {"/reviews", "/pricing", "/help", "/support", "/category", "/categories", "/search", "/apps", "/products"}
CUSTOMER_CLASSES = {"reddit", "forum", "forums", "app_review", "app_reviews", "marketplace_review", "marketplace_reviews",
                    "customer_interview", "customer_interviews", "customer_support", "support_community"}
GENERATOR_LABEL_KEYS = ("verdict", "score", "status", "validated", "verified", "blockers", "label", "result")


def obj(x):
    return x if isinstance(x, dict) else {}


def words(x):
    return isinstance(x, str) and x.strip().casefold() not in ("", "unknown", "n/a", "tbd", "none")


def tokens(x):
    return {v.strip().casefold() for v in x if words(v)} if isinstance(x, list) else set()


def number(x):
    try:
        return type(x) in (int, float) and math.isfinite(x) and x >= 0
    except OverflowError:
        return False


def valid_date(x):
    try:
        date.fromisoformat(x)
        return True
    except (TypeError, ValueError):
        return False


def source_ok(row):
    row = obj(row)
    try:
        u = urlsplit(row.get("url") or "")
        path = (u.path or "").rstrip("/").casefold()
        return (u.scheme in ("http", "https") and bool(u.hostname) and path not in COLLECTION_PATHS
                and not u.username and not u.password and words(row.get("observation")))
    except (ValueError, TypeError):
        return False


def canonical_source_url(value):
    try:
        u = urlsplit(value or "")
        host = u.hostname.casefold() if u.hostname else ""
        port = u.port
        default_port = (u.scheme.casefold() == "http" and port == 80) or (u.scheme.casefold() == "https" and port == 443)
        netloc = host if port is None or default_port else host + ":" + str(port)
        query = urlencode(sorted((k, v) for k, v in parse_qsl(u.query, keep_blank_values=True)
                                 if not k.casefold().startswith("utm_") and k.casefold() not in ("gclid", "fbclid")))
        return urlunsplit(("https", netloc, u.path.rstrip("/"), query, "")) if host else None
    except (TypeError, ValueError):
        return None


def customer_evidence_audit(evidence):
    actors, platforms, records, platform_ids = set(), set(), set(), set()
    duplicates, excluded = 0, 0
    for row in evidence:
        row = obj(row)
        actor, sid, plat = row.get("independent_actor"), row.get("source_id"), row.get("source_platform")
        cls = str(row.get("source_class") or "").strip().casefold().replace("-", "_").replace(" ", "_")
        if not (source_ok(row) and row.get("claim_status") == "fact" and row.get("type") == "customer_behavior"
                and "customer_behavior" in tokens(row.get("supports"))
                and words(actor) and actor.strip().casefold() not in ("unknown", "unclear", "n/a")
                and words(sid) and sid.strip().casefold() not in ("unknown", "unclear", "n/a")
                and words(plat) and cls in CUSTOMER_CLASSES and valid_date(row.get("retrieved_at"))):
            excluded += 1
            continue
        a, p, s = actor.strip().casefold(), plat.strip().casefold(), sid.strip().casefold()
        identity, pid = (canonical_source_url(row.get("url")), s), (p, s)
        if identity in records or pid in platform_ids or a in actors:
            duplicates += 1
            continue
        records.add(identity); platform_ids.add(pid); actors.add(a); platforms.add(p)
    return {"structural_minimum_met": len(actors) >= 3 and len(platforms) >= 2,
            "unique_attributed_customer_accounts": len(actors), "source_platform_count": len(platforms),
            "duplicate_records": duplicates, "excluded_records": excluded, "source_truth_verified": False}


def same_period(a, b):
    return isinstance(a, str) and a in PERIODS and a == b


def period_total(amount, period, months):
    if not number(amount) or not isinstance(period, str) or period not in PERIODS:
        return None
    if period == "one_time":
        return amount
    if type(months) is not int or not 1 <= months <= 120:
        return None
    total = amount * (months if period == "monthly" else math.ceil(months / 12))
    return total if number(total) else None


def evaluate(candidate):
    candidate = obj(candidate)
    case = obj(candidate.get("business_case"))
    evidence = candidate.get("evidence")
    evidence = evidence if isinstance(evidence, list) else []
    findings = []

    def add(dim, status, reason):
        findings.append({"dimension": dim, "status": status, "reason": reason})

    def cited(section, dim):
        refs = section.get("refs")
        if not isinstance(refs, list) or not refs:
            return False
        for i in refs:
            if type(i) is not int or not 0 <= i < len(evidence):
                return False
            row = obj(evidence[i])
            if (not source_ok(row) or row.get("claim_status") != "fact" or dim not in tokens(row.get("supports"))
                    or not valid_date(row.get("retrieved_at"))):
                return False
        return True

    # A5 root cause
    root, action = obj(case.get("root_cause")), obj(case.get("intervention"))
    changes = tokens(action.get("changes_steps"))
    paths, causal_raw = root.get("failure_paths"), root.get("causal_steps")
    causal = tokens(causal_raw)
    valid_causal = isinstance(causal_raw, list) and bool(causal_raw) and len(causal) == len(causal_raw)
    valid_paths = (isinstance(paths, list) and bool(paths)
                   and all(isinstance(p, list) and bool(p) and all(words(n) for n in p) for p in paths))
    path_sets = [tokens(p) for p in paths] if valid_paths else []
    if not (words(root.get("mechanism")) and words(action.get("mechanism")) and changes):
        add("root_cause", "unknown", "Missing causal mechanism or intervention scope")
    elif not valid_paths:
        add("root_cause", "unknown", "Independent failure paths missing or malformed")
    elif not valid_causal:
        add("root_cause", "unknown", "Explicit causal steps are missing or malformed")
    elif not all(p & causal for p in path_sets):
        add("root_cause", "unknown", "A failure path has no declared causal step")
    elif not any(p & causal & changes for p in path_sets):
        add("root_cause", "fatal", "Intervention changes only downstream steps, not a declared causal step")
    elif not all(p & causal & changes for p in path_sets):
        add("root_cause", "unknown", "A causal step on an independent failure path remains unaddressed")
    elif not (cited(root, "root_cause") and cited(action, "intervention")):
        add("root_cause", "unknown", "Causal fit lacks traceable fact records")
    else:
        add("root_cause", "supported", "Intervention changes a declared causal step on every failure path (claims unverified)")

    # A6 platform control: any denied is fatal regardless of owner
    reqs = obj(case.get("platform")).get("requirements")
    if not isinstance(reqs, list) or not reqs:
        add("platform_control", "unknown", "Required capabilities and ownership not enumerated")
    else:
        for raw in reqs:
            r = obj(raw)
            if r.get("permission") == "denied":
                add("platform_control", "fatal", "Required capability unavailable: " + str(r.get("capability", "unknown")))
            elif not (words(r.get("capability")) and r.get("owner") in ("user", "vendor", "third_party")
                      and r.get("permission") == "granted" and cited(r, "platform_control")):
                add("platform_control", "unknown", "Permission, ownership or citation unresolved: " + str(r.get("capability") or "unspecified capability"))
        if not any(f["dimension"] == "platform_control" for f in findings):
            add("platform_control", "supported", "Every declared capability is granted and cited (claims unverified)")

    # A7 buyer
    buyer = obj(case.get("buyer"))
    price, budget = buyer.get("price_usd"), buyer.get("budget_usd")
    comparable = same_period(buyer.get("price_period"), buyer.get("budget_period"))
    if comparable and number(price) and number(budget) and price > budget:
        add("buyer", "fatal", "Proposed price exceeds stated buyer budget")
    elif not (words(buyer.get("role")) and words(buyer.get("purchase_process")) and number(price) and price > 0
              and number(budget) and comparable and cited(buyer, "buyer")):
        add("buyer", "unknown", "Budget owner, buying process, comparable price/budget or citation missing")
    else:
        add("buyer", "supported", "Budget owner and affordable price stated (payment intent unverified)")

    # A8 alternatives: fatal only if one option covers every required outcome at <= total cost
    alts = obj(case.get("alternatives"))
    required, options, months = tokens(alts.get("required_features")), alts.get("options"), alts.get("comparison_months")
    incomplete = not (required and isinstance(options, list) and options and cited(alts, "alternatives"))
    own_total = period_total(price, buyer.get("price_period"), months)
    dominated = []
    for raw in options if isinstance(options, list) else []:
        o = obj(raw)
        switch = o.get("switching_cost_usd")
        other_total = period_total(o.get("price_usd"), o.get("price_period"), months)
        if not (words(o.get("name")) and tokens(o.get("features")) and number(switch)
                and own_total is not None and other_total is not None):
            incomplete = True
        elif required <= tokens(o.get("features")) and other_total + switch <= own_total:
            dominated.append(str(o.get("name")))
    if dominated:
        add("alternatives", "fatal", "Substitute covers every required outcome at no greater total cost: " + ", ".join(dominated))
    elif incomplete:
        add("alternatives", "unknown", "Substitute coverage/cost comparison incomplete")
    else:
        add("alternatives", "supported", "No listed substitute covers every required outcome at no greater cost (competition is not a kill)")

    # A9 feasibility
    d = obj(case.get("delivery"))
    needed, available = tokens(d.get("required_resources")), tokens(d.get("available_resources"))
    days, cap, cost = d.get("days_needed"), d.get("days_available"), d.get("unit_cost_usd")
    margin_comparable = same_period(d.get("cost_period"), buyer.get("price_period"))
    if number(days) and number(cap) and days > cap:
        add("feasibility", "fatal", "Delivery exceeds stated time capacity")
    elif margin_comparable and number(cost) and number(price) and cost >= price:
        add("feasibility", "fatal", "Stated delivery cost leaves no positive gross margin")
    elif not (needed and needed <= available and number(days) and number(cap) and number(cost)
              and margin_comparable and cited(d, "feasibility")):
        add("feasibility", "unknown", "Resources, delivery estimates, period match or citation missing")
    else:
        add("feasibility", "supported", "Declared resources, time and unit economics fit")

    # A10 validation
    v = obj(case.get("validation"))
    if all(words(v.get(k)) for k in ("hypothesis", "method", "success", "kill")):
        add("validation", "supported", "Hypothesis, method, success and kill thresholds stated")
    else:
        add("validation", "unknown", "No falsifiable bounded test design")

    # A3 customer evidence
    audit = customer_evidence_audit(evidence)
    if audit["structural_minimum_met"]:
        add("customer_evidence", "supported", "At least 3 distinct attributed customer accounts across 2 platforms (identities unverified)")
    else:
        add("customer_evidence", "unknown", "Need 3 distinct attributed customer accounts across 2 platforms; found %d accounts across %d platforms"
            % (audit["unique_attributed_customer_accounts"], audit["source_platform_count"]))

    fatal = [f for f in findings if f["status"] == "fatal"]
    unknown = [f for f in findings if f["status"] == "unknown"]
    verdict = "REJECT" if fatal else "INVESTIGATE" if unknown else "TEST_DESIGN"
    ignored = sorted({"top:" + k for k in GENERATOR_LABEL_KEYS if k in candidate}
                     | {"business_case:" + k for k in GENERATOR_LABEL_KEYS if k in case})
    input_sha = hashlib.sha256(json.dumps(candidate, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()
    return {
        "gate_version": GATE_VERSION, "case_id": candidate.get("case_id"), "verdict": verdict,
        "reasons": [f["dimension"] + ": " + f["reason"] for f in fatal + unknown],
        "findings": findings, "customer_evidence_audit": audit,
        "ignored_generator_labels": ignored,
        "input_sha256": input_sha,
        "approval_binding_sha256": binding(input_sha, verdict),
        "build_authorized": False, "external_action_authorized": False,
        "source_truth_verified": False, "purchase_intent_verified": False,
        "scope": "Consistency review of supplied facts; not source verification or market validation",
    }


def binding(input_sha, verdict):
    return hashlib.sha256(("cooper_gate|%s|%s|%s" % (GATE_VERSION, input_sha, verdict)).encode("utf-8")).hexdigest()


def load(path):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError, UnicodeDecodeError) as e:
        return None, "unreadable or invalid JSON: %s" % type(e).__name__
    if not isinstance(data, dict):
        return None, "top level is not a JSON object"
    return data, None


def dump(x):
    return json.dumps(x, sort_keys=True, indent=2, ensure_ascii=False)


def main(argv):
    if len(argv) >= 2 and argv[0] == "evaluate" and len(argv) == 2:
        data, err = load(argv[1])
        if err:
            print(dump({"error": err, "file": argv[1]})); return 2
        print(dump(evaluate(data))); return 0
    if len(argv) == 2 and argv[0] == "run-dir":
        if not os.path.isdir(argv[1]):
            print(dump({"error": "not a directory", "dir": argv[1]})); return 2
        out, bad = {}, False
        for name in sorted(n for n in os.listdir(argv[1]) if n.endswith(".json")):
            data, err = load(os.path.join(argv[1], name))
            if err:
                out[name] = {"error": err}; bad = True
            else:
                out[name] = evaluate(data)
        print(dump(out)); return 2 if bad else 0
    if len(argv) == 2 and argv[0] == "approval-hash":
        data, err = load(argv[1])
        if err:
            print(dump({"error": err})); return 2
        r = evaluate(data)
        print(dump({"approval_binding_sha256": r["approval_binding_sha256"], "verdict": r["verdict"], "input_sha256": r["input_sha256"],
                    "gate_version": GATE_VERSION, "note": "Binding only; authorizes and executes nothing."})); return 0
    if len(argv) == 3 and argv[0] == "verify-approval":
        data, err = load(argv[1])
        if err:
            print(dump({"error": err})); return 2
        r = evaluate(data)
        ok = argv[2].strip().lower() == r["approval_binding_sha256"]
        print(dump({"match": ok, "verdict": r["verdict"], "build_authorized": False, "external_action_authorized": False,
                    "note": "A match proves the approval quotes this exact input and verdict; it executes nothing."}))
        return 0 if ok else 1
    sys.stderr.write(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
