"""
Prompt templates for different task types.
Better prompts = better code from Umbra's LLM.
"""

TEMPLATES = {
    "python_script": """You are an expert Python developer writing production-quality scripts.
Task: {objective}

Requirements:
- Write complete, runnable Python code
- Include proper imports at the top
- Add a docstring explaining what the script does
- Include error handling with try/except where appropriate
- Add a if __name__ == '__main__' block
- Add inline comments for complex logic
- Make the code PEP 8 compliant

Wrap your code in a Python code block using triple backticks with python tag.
Output ONLY the code block, no other text before or after.""",

    "python_class": """You are an expert Python developer writing clean, well-structured classes.
Task: {objective}

Requirements:
- Write a complete Python class with __init__, methods, and docstrings
- Include type hints where appropriate
- Add a to_dict() method if the class holds data
- Include proper error handling
- Make it importable and testable

Wrap your code in a Python code block using triple backticks with python tag.""",

    "python_test": """You are an expert Python developer writing pytest test suites.
Task: {objective}

Requirements:
- Use pytest conventions (def test_*, fixtures)
- Test the main happy path
- Test at least one error/edge case
- Use meaningful assertion messages
- Mock external dependencies with unittest.mock
- Each test function tests ONE thing
- Import the module being tested at the top

Wrap your code in a Python code block using triple backticks with python tag.""",

    "python_api": """You are an expert Python developer building REST APIs.
Task: {objective}

Requirements:
- Use standard Python libraries or Flask/FastAPI if needed
- Define clear route handlers
- Include request validation
- Return JSON responses with appropriate status codes
- Include error handling
- Add docstrings to each route

Wrap your code in a Python code block using triple backticks with python tag.""",

    "data_analysis": """You are an expert Python data scientist.
Task: {objective}

Requirements:
- Use pandas for data manipulation
- Use standard statistical methods
- Print clear, formatted output
- Handle missing data gracefully
- Include column type detection
- Add comments explaining the analysis steps

Wrap your code in a Python code block using triple backticks with python tag.""",

    "automation": """You are an expert Python automation engineer.
Task: {objective}

Requirements:
- Use Python stdlib where possible (os, pathlib, shutil, subprocess)
- Handle file/path errors gracefully
- Add progress output so the user knows what's happening
- Make paths configurable (accept as arguments or constants at top)
- Include a dry-run option where applicable

Wrap your code in a Python code block using triple backticks with python tag.""",

    "default": """You are Umbra's expert Python code generator.
Task: {objective}

Write clean, complete, working Python code that solves this task.
Include imports, docstrings, and error handling.
Make the code immediately runnable.

Wrap your code in a Python code block using triple backticks with python tag.""",
}


def detect_template(objective: str) -> str:
    obj_lower = objective.lower()
    if any(w in obj_lower for w in ("test", "pytest", "unit test", "spec")):
        return "python_test"
    if any(w in obj_lower for w in ("api", "endpoint", "rest", "route", "flask", "fastapi")):
        return "python_api"
    if any(w in obj_lower for w in ("csv", "dataframe", "pandas", "statistics", "analysis", "data")):
        return "data_analysis"
    if any(w in obj_lower for w in ("class", "object", "model", "entity", "dataclass")):
        return "python_class"
    if any(w in obj_lower for w in ("automate", "automation", "file", "folder", "directory", "scan", "move", "copy", "rename")):
        return "automation"
    if any(w in obj_lower for w in ("script", "tool", "utility", "program", "write a python")):
        return "python_script"
    return "default"


def get_prompt(objective: str, template_name: str = None) -> str:
    name = template_name or detect_template(objective)
    template = TEMPLATES.get(name, TEMPLATES["default"])
    return template.format(objective=objective)


class RuntimePromptTemplates:

    def __init__(self):
        self.templates = dict(TEMPLATES)
        self.usage_count = {}

    def get_prompt(self, objective: str, template_name: str = None) -> str:
        name = template_name or detect_template(objective)
        self.usage_count[name] = self.usage_count.get(name, 0) + 1
        template = self.templates.get(name, self.templates["default"])
        return template.format(objective=objective)

    def detect_template(self, objective: str) -> str:
        return detect_template(objective)

    def add_template(self, name: str, template: str):
        self.templates[name] = template

    def list_templates(self):
        return list(self.templates.keys())

    def get_usage_stats(self):
        return dict(self.usage_count)