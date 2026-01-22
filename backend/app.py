# backend/app.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from parsers import detect_and_parse
from generators import generate_bash_script, generate_powershell_script, generate_dockerfile

app = FastAPI(title="Smart Environment Setup Assistant")

# Allow local dev origins used by Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-script/")
async def generate_script(file: UploadFile = File(...), type: str = Form("bash")):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded.")
    contents = await file.read()
    deps = detect_and_parse(file.filename or "requirements.txt", contents)

    if type == "bash":
        script = generate_bash_script(deps)
    elif type == "powershell":
        script = generate_powershell_script(deps)
    elif type == "docker":
        script = generate_dockerfile(deps)
    else:
        raise HTTPException(status_code=400, detail="Unknown script type requested.")

    response = {"script": script}
    if type == "docker":
        pip_deps = [d for d in deps if "@" not in d]
        if pip_deps:
            response["requirements_txt"] = "\n".join(pip_deps) + "\n"
    return response