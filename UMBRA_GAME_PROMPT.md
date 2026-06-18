# UMBRA Game Building Prompts

## HOW TO USE

Start Umbra CLI:
    python umbra.py

Or use the Desktop app / GUI.

Paste ANY of these prompts exactly as-is. They are crafted to produce
a SINGLE complete, runnable Python file.

---

## PROMPT: Simple Pygame Game (Verified Working)

Paste this entire block as ONE message:

write a single complete Python pygame script saved as one file called game.py. The game must: initialize pygame, create a 800x600 window titled "Umbra Game", have a blue player rectangle (40x40) at center that moves with arrow keys at 4 pixels per step, have a red enemy rectangle (40x40) that starts at top-right and moves toward the player at 2 pixels per step every frame, show player health as 3 hearts or HP:3 in white text top-left, reduce health by 1 when enemy touches player and respawn player at center with 1 second invincibility, show GAME OVER in red center screen when health reaches 0 with "Press R to restart" below it, restart the game when R is pressed, run at 60 FPS with pygame.time.Clock, include all imports at top, wrap everything in a main() function, call main() with if __name__ == '__main__'. Output ONLY the complete Python code block, nothing else.

## HOW TO RUN THE GAME

After Umbra finishes:
1. Open Files tab in Desktop app or GUI
2. Find the run folder (e.g. run_0001)
3. Look for game.py
4. Double-click or click ▶ Run

OR from command line:
    cd C:\Umbra\workspaces\run_0001\code
    python game.py

---

## PROMPT: Data Analysis Script

write a single complete Python script that reads a CSV file, shows basic statistics (mean, median, min, max for numeric columns), counts missing values, prints a summary report, and saves the report to output_report.txt. Include sample data generation if no CSV is provided. All in one file with main() function.

---

## PROMPT: REST API Server

write a single complete Python Flask REST API with endpoints: GET /api/health returns status ok, GET /api/items returns a list of items, POST /api/items creates a new item with name and description, GET /api/items/id returns one item, DELETE /api/items/id deletes an item. Use in-memory storage. Include if __name__ == '__main__' that runs on port 5000. Single file, all imports included.

---

## PROMPT: File Organizer Tool

write a single complete Python script that organizes files in a directory by extension into subfolders (Images, Documents, Videos, Audio, Archives, Code, Other), shows a summary of what was moved, has a dry-run mode that shows what would happen without moving files, accepts the directory path as a command line argument. Single file with main() function.

---

## PROMPT: AI Agent (uses Ollama)

write a single complete Python script that connects to Ollama at localhost:11434, maintains a conversation history, sends messages and receives responses using urllib (no external HTTP libraries), has a simple command loop where the user types messages and sees responses, supports /quit to exit, /clear to clear history, /history to show history. Single file, all imports included, runs from command line.

