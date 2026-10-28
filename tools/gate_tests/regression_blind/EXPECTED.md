# Blind regression fixtures (graded PASS by Cooper Critical Reviewer, 2026-10-27 17:46 CT)
Gate: cooper_gate.py sha256 609bfe31cbd8ff0650e1d3d5c878d5661dc38a9067be501fdabee99f2fc3f697
Sealed expectations (reviewer's store) sha256 7b6ed4c11d93a2800bb95da66f8c89ca03593294b6660bf3a869a448fd8c455c
- BLIND-01 (input 5c0d6056...2b6d): REJECT; alternatives fatal; buyer, customer_evidence unknown; 3 accounts, 1 platform, 1 duplicate, 4 excluded
- BLIND-02 (input dc529014...c065): TEST_DESIGN; all 7 supported; 3 accounts, 2 platforms, 1 duplicate, 4 excluded
Run: python3 ../../cooper_gate.py run-dir .  (compare against ../../../../cooper/audit/artifacts/SE-02_blind_run.json)
