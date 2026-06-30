with open("Umbra.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in range(709, 800):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}", end="")