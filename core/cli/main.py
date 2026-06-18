from core.boss_agent import BossAgent


def main():

    boss = BossAgent()

    print("\n=== UMBRA CONTROL INTERFACE ===")
    print("Type 'exit' to quit\n")

    while True:

        try:
            user_input = input("Umbra> ").strip()

            if user_input.lower() in ["exit", "quit"]:
                break

            if not user_input:
                continue

            result = boss.run(user_input)

            # Always show raw return for debugging consistency
            print("\n[DEBUG RETURN]")
            print(result)

        except KeyboardInterrupt:
            print("\n[EXIT]")
            break

        except Exception as e:
            print("[CLI ERROR]", str(e))


if __name__ == "__main__":
    main()