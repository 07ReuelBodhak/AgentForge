import sys
import json

def parse_tester_result(output: str):
    lines = [line.strip() for line in output.strip().split("\n") if line.strip()]
    if not lines:
        return {"status": "INVALID_TESTER_OUTPUT"}

    if lines[0].startswith("RESULT: PASS"):
        # Extract optional evidence if provided
        evidence = []
        in_evidence = False
        for line in lines[1:]:
            if line.startswith("EVIDENCE:"):
                in_evidence = True
                ev = line[len("EVIDENCE:"):].strip()
                if ev:
                    evidence.append(ev)
            elif in_evidence and line.startswith("-"):
                evidence.append(line.lstrip("- ").strip())
        
        result = {"status": "PASS"}
        if evidence:
            result["evidence"] = evidence
        return result
        
    if lines[0] == "RESULT: FAIL":
        standard_keys = ["FAILURE:", "RELEVANT_FILES:", "FAILING_TESTS:", "RECOMMENDATION:", "DEVIATIONS:", "EVIDENCE:"]
        found_keys = {}
        current_key = None
        
        for line in lines[1:]:
            is_key = False
            for rk in standard_keys:
                if line.startswith(rk):
                    current_key = rk
                    found_keys[rk] = line[len(rk):].strip()
                    is_key = True
                    break
            if not is_key and current_key:
                found_keys[current_key] += "\n" + line
                
        # Mandatory failure sections
        required_keys = ["FAILURE:", "RELEVANT_FILES:", "FAILING_TESTS:", "RECOMMENDATION:"]
        if all(k in found_keys for k in required_keys):
            res = {
                "status": "FAIL",
                "failure": found_keys["FAILURE:"].strip(),
                "relevant_files": found_keys["RELEVANT_FILES:"].strip(),
                "failing_tests": found_keys["FAILING_TESTS:"].strip(),
                "recommendation": found_keys["RECOMMENDATION:"].strip(),
            }
            if "DEVIATIONS:" in found_keys and found_keys["DEVIATIONS:"].strip():
                res["deviations"] = found_keys["DEVIATIONS:"].strip()
            if "EVIDENCE:" in found_keys and found_keys["EVIDENCE:"].strip():
                res["evidence"] = found_keys["EVIDENCE:"].strip()
            return res
            
        return {"status": "INVALID_TESTER_OUTPUT"}
        
    return {"status": "INVALID_TESTER_OUTPUT"}

if __name__ == "__main__":
    content = sys.stdin.read()
    result = parse_tester_result(content)
    print(json.dumps(result, indent=2))
