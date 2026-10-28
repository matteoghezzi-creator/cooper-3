"""Runs gate_tests/cases against expected.json (frozen; see FREEZE.txt). Checks FREEZE hashes first."""
import hashlib, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); GATE = os.path.join(HERE, "..", "cooper_gate.py")
for line in open(os.path.join(HERE, "FREEZE.txt")):
    parts = line.split()
    if len(parts) == 2 and len(parts[0]) == 64:
        actual = hashlib.sha256(open(os.path.join(HERE, parts[1]), "rb").read()).hexdigest()
        if actual != parts[0]:
            sys.exit("FREEZE MISMATCH: " + parts[1])
print("freeze hashes: all match")
runs = [subprocess.run([sys.executable, GATE, "run-dir", os.path.join(HERE, "cases")], capture_output=True) for _ in range(2)]
print("run-dir exit codes:", [r.returncode for r in runs], "| byte-identical:", runs[0].stdout == runs[1].stdout,
      "| sha256:", hashlib.sha256(runs[0].stdout).hexdigest())
out = json.loads(runs[0].stdout); exp = json.load(open(os.path.join(HERE, "expected.json")))
fails = 0
for cid in sorted(k for k in exp if not k.startswith("_")):
    e, r = exp[cid], out.get(cid + ".json")
    if r is None:
        print("FAIL", cid, "missing"); fails += 1; continue
    fat = sorted({f["dimension"] for f in r["findings"] if f["status"] == "fatal"})
    unk = {f["dimension"] for f in r["findings"] if f["status"] == "unknown"}
    a = r["customer_evidence_audit"]
    problems = []
    if r["verdict"] != e["verdict"]: problems.append("verdict %s != %s" % (r["verdict"], e["verdict"]))
    if fat != sorted(e["fatal"]): problems.append("fatal %s != %s" % (fat, e["fatal"]))
    miss = set(e.get("unknown_includes", [])) - unk
    if miss: problems.append("missing unknown %s" % sorted(miss))
    if "accounts" in e and a["unique_attributed_customer_accounts"] != e["accounts"]: problems.append("accounts %d" % a["unique_attributed_customer_accounts"])
    if "platforms" in e and a["source_platform_count"] != e["platforms"]: problems.append("platforms %d" % a["source_platform_count"])
    if (r["build_authorized"], r["external_action_authorized"], r["source_truth_verified"]) != (False, False, False): problems.append("authorization flags")
    fails += bool(problems)
    print(("FAIL " if problems else "PASS ") + cid.ljust(32), r["verdict"].ljust(12), "fatal=" + ",".join(fat) if fat else "", "; ".join(problems),
          ("ignored=" + ",".join(r["ignored_generator_labels"])) if r["ignored_generator_labels"] else "")
print("RESULT: %d/%d passed" % (len([k for k in exp if not k.startswith('_')]) - fails, len([k for k in exp if not k.startswith('_')])))
sys.exit(1 if fails else 0)
