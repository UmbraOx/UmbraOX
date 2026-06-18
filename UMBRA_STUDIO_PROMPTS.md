# UMBRA AI Studio Suite — Build Prompts

These prompts build specialized agents inside Umbra.
Paste each one into the Umbra CLI or GUI chat.

---

## AGENT 1: Character Design Agent

write a single complete Python script for a character design AI agent.
The agent should: accept a character description in plain English,
ask follow-up questions about personality traits, physical appearance,
backstory, abilities, and role in the story,
generate a structured character sheet as JSON with fields:
name, age, appearance, personality, backstory, abilities, weaknesses,
relationships, voice_description, and role,
save the character sheet to a file named after the character,
allow the user to request modifications by describing what to change,
maintain conversation history so context is preserved across turns,
use Ollama at localhost:11434 with the model qwen2.5-coder:14b via urllib only,
run as a command-line application,
single file all imports included, if __name__ == '__main__': main()

---

## AGENT 2: World Builder Agent

write a single complete Python script for a world building AI agent.
The agent should: accept a world concept in plain English,
generate a structured world document including: world name, geography,
climate, factions, political systems, economy, magic or technology system,
history timeline, notable locations with descriptions, and cultural details,
save the world document as a markdown file and JSON,
allow iterative expansion by asking questions like
"tell me more about the northern faction" or "add a mountain range",
track what has been created so it can reference previous world elements,
use Ollama at localhost:11434 via urllib only,
single file all imports, if __name__ == '__main__': main()

---

## AGENT 3: Game Mechanic Designer Agent

write a single complete Python script for a game mechanics AI agent.
The agent should: accept a game concept description,
generate detailed game mechanics including: core gameplay loop,
player abilities and stats, progression system, combat system,
economy and crafting, level design principles, difficulty scaling,
enemy AI behavior patterns, and win/loss conditions,
output each mechanic as structured data with description and implementation notes,
suggest how mechanics interact with each other,
save the full game design document as markdown,
use Ollama at localhost:11434 via urllib only,
single file, if __name__ == '__main__': main()

---

## AGENT 4: NPC Behavior Agent

write a single complete Python script that generates NPC AI behavior systems.
The agent should: accept an NPC description and game context,
generate: daily routine schedules, dialogue trees in JSON format,
behavioral states (idle, patrol, hostile, friendly, fleeing),
decision trees for different player interactions,
memory system so NPCs remember what the player did,
emotional state tracking that affects dialogue,
output as both a JSON behavior file and a Python class ready to use in pygame,
use Ollama at localhost:11434 via urllib only,
single file, if __name__ == '__main__': main()

---

## AGENT 5: Quest and Story Generator

write a single complete Python script for a quest and story generation agent.
The agent should: accept a setting and story premise,
generate: main questline with objectives and rewards,
side quests that connect to the main story,
branching dialogue that changes based on player choices,
consequences that affect the game world state,
a narrative timeline showing how events connect,
output everything as structured JSON and markdown,
use Ollama at localhost:11434 via urllib only,
single file, if __name__ == '__main__': main()

---

## AGENT 6: Code Review and Bug Fix Agent

write a single complete Python script that reviews Python files for bugs.
The agent should: accept a file path as argument,
read the file and analyze it for: syntax errors, runtime errors,
logic bugs, missing error handling, security issues, performance problems,
generate a detailed bug report with line numbers and severity,
automatically generate a fixed version of the file,
save the fixed file as filename_fixed.py,
run the fixed file and report if it works,
use Ollama at localhost:11434 via urllib only,
single file, if __name__ == '__main__': main()

---

## AGENT 7: TikTok/Content Script Generator

write a single complete Python script for a content creation agent.
The agent should: accept a topic and target audience,
generate: video script with timestamps and scene descriptions,
hook for the first 3 seconds, main content breakdown,
call to action, hashtag suggestions, and caption,
also generate variations for different platforms:
TikTok (60 seconds), YouTube Shorts (60 seconds),
Instagram Reels (30 seconds),
save all outputs as text files,
use Ollama at localhost:11434 via urllib only,
single file, if __name__ == '__main__': main()

---

## AGENT 8: Desktop Overlay App Generator

write a single complete Python script that generates desktop overlay applications.
The agent should: accept a description of what the overlay should do,
generate a complete working Python application using tkinter with:
always-on-top transparent window,
customizable position and size,
minimize to system tray,
hotkey to show/hide,
the specific functionality the user described,
output a complete runnable overlay app Python file,
use Ollama at localhost:11434 via urllib only,
single file, if __name__ == '__main__': main()

---

## AGENT 9: AI Companion/Girlfriend Personality Agent

write a single complete Python script for an AI companion personality agent.
The agent should: accept a personality description and relationship type,
generate: personality profile with traits, communication style,
interests and knowledge areas, emotional responses to different situations,
memory of conversations stored in JSON,
a conversation loop that responds in-character,
mood system that changes based on conversation context,
save conversation history and personality profile to files,
use Ollama at localhost:11434 via urllib only,
single file, if __name__ == '__main__': main()

---

## AGENT 10: Studio Orchestrator (runs all agents)

write a single complete Python script that acts as an AI studio orchestrator.
The orchestrator should: present a menu of available agents,
accept a project description from the user,
determine which agents are needed for the project,
run each required agent in sequence passing context between them,
compile all outputs into a project folder with:
a project summary markdown file,
all generated assets (characters, world, mechanics, quests),
a README with how to use everything,
track project progress and allow resuming,
use Ollama at localhost:11434 via urllib only,
single file, if __name__ == '__main__': main()

---

## HOW TO RUN EACH AGENT PROMPT

1. Start Umbra: python umbra.py
2. Paste the prompt exactly as written above
3. Umbra generates the agent file in workspaces/
4. Go to Files tab, click the file to preview
5. Click Play button to run the agent
6. The agent then runs in its own console window

## RECOMMENDED ORDER

1. Start with Agent 6 (Bug Fixer) — useful for fixing other agents
2. Then Agent 1 (Character Design) to test conversation flow
3. Then Agent 2 (World Builder) for your biggest project needs
4. Then Agent 10 (Orchestrator) to tie everything together