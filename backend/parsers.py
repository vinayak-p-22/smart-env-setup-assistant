# backend/parsers.py
import json
import re
from typing import List

def parse_requirements_txt(contents: str) -> List[str]:
    """
    Parse a requirements.txt style content into a list of dependency strings.
    Ignores comments and empty lines.
    """
    deps = []
    for line in contents.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # ignore editable installs and local paths for now
        if line.startswith("-e") or line.startswith(".") or line.startswith("/"):
            continue
        deps.append(line)
    return deps

def parse_package_json(contents: str) -> List[str]:
    """
    Parse package.json content and return dependencies with versions.
    Returns both dependencies and devDependencies.
    """
    try:
        data = json.loads(contents)
    except json.JSONDecodeError:
        return []
    deps = []
    for key in ("dependencies", "devDependencies"):
        section = data.get(key, {})
        for name, ver in section.items():
            deps.append(f"{name}@{ver}")
    return deps

def parse_pyproject_toml(contents: str) -> List[str]:
    """
    Lightweight TOML parsing for poetry/pyproject dependencies.
    Extracts lines under [tool.poetry.dependencies] or [project.dependencies].
    """
    deps = []
    lines = contents.splitlines()
    current_section = None
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            current_section = line.strip()
            continue
        if current_section in ("[tool.poetry.dependencies]", "[project.dependencies]"):
            # expect lines like: package = "^1.2.3" or package = { version = "^1.2", extras = ["x"] }
            m = re.match(r'([A-Za-z0-9_\-]+)\s*=\s*(.+)', line)
            if m:
                name = m.group(1)
                val = m.group(2).strip()
                # clean quotes and braces
                val = val.split(",")[0].strip()
                val = val.strip('"').strip("'")
                # If val looks like a version specifier, include it; otherwise include name only
                if val and any(ch.isdigit() for ch in val):
                    deps.append(f"{name}=={val}")
                else:
                    deps.append(name)
    return deps

def detect_and_parse(filename: str, contents: bytes):
    """
    Detect file type by filename and parse accordingly.
    Returns a list of dependency strings.
    """
    text = contents.decode(errors="ignore")
    fname = (filename or "").lower()
    if fname.endswith("requirements.txt") or fname.endswith(".txt"):
        return parse_requirements_txt(text)
    if fname.endswith("package.json"):
        return parse_package_json(text)
    if fname.endswith("pyproject.toml"):
        return parse_pyproject_toml(text)
    # fallback: try requirements style
    return parse_requirements_txt(text)