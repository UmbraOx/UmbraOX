import json


def print_summary(report):
    print("\n=== UMBRA SELF REPAIR REPORT ===\n")

    for r in report["results"]:
        print(f"{r['action']} | score={r['score']} | {r['path']}")
        for reason in r["reasons"]:
            print(f"   - {reason}")

    print("\n=================================\n")


if __name__ == "__main__":
    with open("repair_report.json", "r") as f:
        data = json.load(f)

    print_summary(data)