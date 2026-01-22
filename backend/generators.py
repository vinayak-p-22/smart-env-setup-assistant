# backend/generators.py
from typing import List

def generate_bash_script(dependencies: List[str]) -> str:
    lines = [
        "#!/bin/bash",
        "",
        "set -e",
        "",
        "# Create virtual environment",
        "python3 -m venv venv",
        "source venv/bin/activate",
        "",
        "# Upgrade pip",
        "pip install --upgrade pip",
        ""
    ]
    if dependencies:
        pip_deps = [d for d in dependencies if "@" not in d]
        if pip_deps:
            lines.append("# Install Python dependencies")
            for dep in pip_deps:
                lines.append(f"pip install {dep}")
    else:
        lines.append("# No dependencies detected")
    return "\n".join(lines)

def generate_powershell_script(dependencies: List[str]) -> str:
    lines = [
        "# PowerShell setup script",
        "Set-StrictMode -Version Latest",
        "",
        "# Create virtual environment",
        "python -m venv venv",
        "venv\\Scripts\\Activate.ps1",
        "",
        "# Upgrade pip",
        "python -m pip install --upgrade pip",
        ""
    ]
    if dependencies:
        pip_deps = [d for d in dependencies if "@" not in d]
        if pip_deps:
            lines.append("# Install Python dependencies")
            for dep in pip_deps:
                lines.append(f"python -m pip install {dep}")
    else:
        lines.append("# No dependencies detected")
    return "\n".join(lines)

def generate_dockerfile(dependencies: List[str]) -> str:
    lines = [
        "FROM python:3.10-slim",
        "WORKDIR /app",
        "",
        "# Copy project files (adjust as needed)",
        "COPY . /app",
        "",
        "# Install build dependencies",
        "RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*",
        "",
        "# Create virtual environment",
        "RUN python -m venv /opt/venv",
        "ENV PATH=\"/opt/venv/bin:$PATH\"",
        "",
        "RUN pip install --upgrade pip",
    ]
    pip_deps = [d for d in dependencies if "@" not in d]
    if pip_deps:
        lines.append("COPY requirements.txt /app/requirements.txt")
        lines.append("RUN pip install -r /app/requirements.txt")
    else:
        lines.append("# No Python dependencies detected; adjust Dockerfile as needed")
    lines.append("")
    lines.append('CMD ["bash"]')
    return "\n".join(lines)