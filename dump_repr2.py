with open("Umbra.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in range(722, 748):
    if i < len(lines):
        print(f"{i+1}: {repr(lines[i])}")