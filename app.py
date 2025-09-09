# app.py
import os
import pathlib
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import asyncio

# --------------------------
# 1) Env + external client
# --------------------------
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise RuntimeError("GEMINI_API_KEY not set in environment (.env).")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

# --------------------------
# 2) Agent (dummy about yourself)
# --------------------------
agent = Agent(
    name="AboutMeAgent",
    instructions=(
        "You are a helpful assistant that only answers questions "
        "about Abid Ali. Abid Ali is an AI agents developer from Pakistan. "
        "He loves Python, FastAPI, Postgres, and RAG systems. "
        "He is currently learning AWS deployment."
    ),
    tools=[],
    model=model,
)

# --------------------------
# 3) FastAPI app
# --------------------------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test")
def test():
    return {"status": "working", "message": "Dummy agent is running!"}

@app.get("/chat")
async def chat(message: str):
    """Ask something about Abid Ali"""
    result = await Runner.run(agent, message)
    return {"message": message, "response": result.final_output}

@app.get("/", response_class=HTMLResponse)
def root():
    # ✅ Simple HTML UI
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Abid's Dummy Agent</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            #chatbox { border: 1px solid #ccc; padding: 10px; height: 300px; overflow-y: auto; }
            .user { color: blue; margin: 5px 0; }
            .agent { color: green; margin: 5px 0; }
            input { width: 80%; padding: 10px; }
            button { padding: 10px; }
        </style>
    </head>
    <body>
        <h2>🤖 Abid's Dummy Agent</h2>
        <div id="chatbox"></div>
        <br>
        <input id="message" type="text" placeholder="Ask me something about Abid Ali..." />
        <button onclick="sendMessage()">Send</button>

        <script>
            async function sendMessage() {
                const msg = document.getElementById("message").value;
                if (!msg) return;

                const chatbox = document.getElementById("chatbox");
                chatbox.innerHTML += "<div class='user'><b>You:</b> " + msg + "</div>";

                const res = await fetch("/chat?message=" + encodeURIComponent(msg));
                const data = await res.json();

                chatbox.innerHTML += "<div class='agent'><b>Agent:</b> " + data.response + "</div>";
                chatbox.scrollTop = chatbox.scrollHeight;
                document.getElementById("message").value = "";
            }
        </script>
    </body>
    </html>
    """

# --------------------------
# 4) Optional CLI loop
# --------------------------
if __name__ == "__main__":
    async def cli_loop():
        print("🤖 AboutMeAgent CLI is ready! Type 'exit' to quit.\n")
        while True:
            q = input("You: ")
            if q.lower() in ["exit", "quit"]:
                print("👋 Goodbye!")
                break
            result = await Runner.run(agent, q)
            print(f"Agent: {result.final_output}\n")
    asyncio.run(cli_loop())
