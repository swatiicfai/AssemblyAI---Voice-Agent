import json
import os
import copy
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from lib import aai, read_agent, publish_agent, stored_agent_id

app = FastAPI()

def resolve_agent() -> dict:
    name = "aerorescue"
    known = os.environ.get("AGENT_ID", "")
    if known:
        return {"id": known, "name": "AeroRescue"}
    
    agent = read_agent(name)
    result = publish_agent(agent, name=name, reuse_by_name=True)
    return {"id": result["id"], "name": agent["name"]}

def public_agent(agent: dict) -> dict:
    copied = copy.deepcopy(agent)
    for tool in copied.get("tools", []):
        for header in tool.get("http", {}).get("headers", []):
            header["value"] = "<hidden>"
    for llm in copied.get("llm", []):
        llm.pop("api_key", None)
    return copied

@app.get("/token")
def get_token():
    try:
        token = aai("/token?product=voice_agent&expires_in_seconds=60")
        return JSONResponse(content=token)
    except Exception as err:
        print(err)
        raise HTTPException(status_code=502, detail="token request failed")

@app.get("/agent")
def get_agent():
    agent_info = resolve_agent()
    try:
        agent = aai(f"/agents/{agent_info['id']}")
        return JSONResponse(content=public_agent(agent))
    except Exception as err:
        print(err)
        raise HTTPException(status_code=502, detail="could not load the agent")

@app.get("/")
def serve_index():
    agent_info = resolve_agent()
    with open("public/index.html", "r") as f:
        html = f.read()
    
    html = html.replace("{{AGENT_NAME}}", agent_info["name"])
    html = html.replace("{{AGENT_JSON}}", json.dumps(agent_info).replace("<", "\\u003c"))
    return HTMLResponse(content=html)
