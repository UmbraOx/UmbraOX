# UMBRA Self-Upgrade Prompt v2.0

Copy and paste the following prompt directly into Umbra's interactive mode to have Umbra
plan and build its own GUI, image generation, video generation, and extended features.

---

## PASTE THIS INTO: umbra>
---------------------------------------------------------------------------------
You are Umbra, an autonomous AI runtime OS. You are about to upgrade yourself.
Your current capabilities are documented in C:\Umbra\README.md and your core runtime
is in C:\Umbra\core\runtime. You have 600+ passing tests.
Your upgrade mission is to build a web-based GUI dashboard for yourself using Python.
Build all of the following as separate Python files in C:\Umbra\gui:

gui_server.py

Flask-based web server (or use http.server if Flask not installed)
Serves a dashboard at http://localhost:7860
REST endpoints: /api/status, /api/run, /api/history, /api/metrics, /api/health
WebSocket support for real-time run output streaming
Static file serving from gui/static/


gui_dashboard.html

Single-page app with dark theme
Left sidebar: status panel, model info, memory stats
Main area: prompt input box, run button, output display
History tab: list of past runs with file counts
Metrics tab: success rate, files written, charts
Health tab: real-time health check display
Responsive layout that works at 1080p and 1440p


gui_image_generator.py

Integration with local Stable Diffusion via automatic1111 API (localhost:7861)
Fallback to requesting image generation description if SD not running
Saves generated images to C:\Umbra\workspaces\images\
Endpoint: /api/generate_image


gui_voice_input.py

Optional: speech-to-text using Python SpeechRecognition library
Microphone input for voice commands to Umbra
Transcribes and sends as prompt to pipeline


gui_file_browser.py

Browse C:\Umbra\workspaces\ directory tree
Preview generated Python files in browser
Download individual files
Show file metadata (lines, validation score, created_at)


gui_settings.py

Web UI for editing umbra_config.json
Provider switcher (ollama/groq/openai)
Model selector (shows available ollama models)
Resource manager settings
Save/reload config without restart



After building all files, write a startup script gui_start.py that:

Installs required packages (flask, flask-cors) if not present
Starts the GUI server on port 7860
Opens the browser automatically
Keeps running until Ctrl+C

Also write test files for each module in core/tests/test_gui_*.py

---

## HOW TO USE THIS PROMPT

1. Start Umbra:
python umbra.py

2. Paste the prompt above at the `umbra>` prompt

3. Umbra will decompose it into ~7 tasks and generate all the GUI files

4. After completion, start the GUI:
python gui_start.py

5. Open browser to: http://localhost:7860

---

## ADDITIONAL PROMPTS FOR EXTENDED FEATURES

### For video generation support:
Build gui_video_generator.py that integrates with local video generation tools.
Support ComfyUI API at localhost:8188 for video generation.
Create an interface at /api/generate_video that accepts a text prompt,
generates a video sequence, and saves to C:\Umbra\workspaces\videos.
Include progress tracking and a gallery view in the dashboard.

### For multi-model support:
Build gui_model_manager.py that shows all installed Ollama models,
allows pulling new models with progress display, switching models
without restarting Umbra, and benchmarking models with a test prompt.

### For autonomous scheduling:
Build gui_task_scheduler.py that allows scheduling recurring Umbra tasks.
Users can set up tasks like "every day at 9am: analyze my project at C:\MyProject"
or "every hour: check disk usage and alert if > 90%".
Tasks run in background threads and results appear in the dashboard.

### For code project management:
Build gui_project_manager.py that treats each Umbra workspace run as a project.
Allow naming projects, adding notes, viewing all generated files,
running validation and code review from the GUI,
and exporting projects as zip files.