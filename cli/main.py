from core.boss_agent import BossAgent

boss = BossAgent()

while True:

    user = input("\nUmbra> ")

    if user.lower() in ["exit", "quit"]:
        break

    boss.run(user)