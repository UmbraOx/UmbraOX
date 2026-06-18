from core.runtime.runtime_prompt_orchestrator import (
    RuntimePromptOrchestrator
)


def main():

    runtime = RuntimePromptOrchestrator()

    print("\n[UMBRA PROMPT RUNTIME ONLINE]\n")

    while True:

        prompt = input("Umbra Prompt > ")

        if prompt.lower() in [
            "exit",
            "quit"
        ]:
            break

        result = runtime.execute(
            prompt
        )

        print("\nRESULT:\n")

        print(result)

        print("\n")


if __name__ == "__main__":

    main()