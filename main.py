"""Run the synthetic code repair demo: python main.py"""

from repair_agent.runner import repair_demo


def main():
    result = repair_demo()
    print("=== AUTONOMOUS CODE REPAIR: STARTER PROTOTYPE ===")
    print("Baseline passed:", result["baseline_passed"])
    print("Candidates evaluated:", result["candidates_considered"])
    print("Verified patch found:", result["repair_found"])
    if result["repair_found"]:
        print("Change:", result["validated_change"])
        print("Saved: artifacts/proposed_fix.patch and artifacts/report.json")
    else:
        print(result.get("message", "No validated fix found."))


if __name__ == "__main__":
    main()
