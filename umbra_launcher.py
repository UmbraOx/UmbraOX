from core.agents.boss_agent import BossAgent
import time


def main():
    boss = BossAgent(r"C:\Umbra")

    print("UMBRA OS BOOTING...")

    while True:
        cycle = boss.run_cycle()

        print("\n--- CYCLE REPORT ---")
        print(cycle)

        next_task = boss.execute_next()

        if next_task and "proposal" in next_task:
            print("\nPATCH READY FOR REVIEW")
            print(next_task["diff"] if "diff" in next_task else next_task)

        time.sleep(10)


if __name__ == "__main__":
    main()