# 🔥 MUST BE FIRST — Fix asyncio issue with Streamlit threads
import asyncio

try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# -------------------- IMPORTS --------------------
import streamlit as st
import logging
from pathlib import Path
import tempfile
import os
import sys

# -------------------- LOGGING --------------------
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

DEFAULT_OLLAMA_HOST = "http://localhost:11434"
DEFAULT_OLLAMA_MODEL = "llama3.2"


def is_vision_model(model_id: str) -> bool:
    normalized_model = model_id.lower()
    return any(keyword in normalized_model for keyword in ("vision", "llava", "bakllava", "minicpm-v"))


# -------------------- AGENT INITIALIZATION --------------------
def initialize_agents(model_id: str, ollama_host: str):
    try:
        from agno.agent import Agent
        from agno.models.ollama import Ollama

        model = Ollama(
            id=model_id,
            host=ollama_host,
        )

        therapist_agent = Agent(
            model=model,
            name="Therapist Agent",
            instructions=[
                "You are an empathetic therapist that:",
                "1. Listens with empathy and validates feelings",
                "2. Uses gentle humor to lighten the mood",
                "3. Shares relatable breakup experiences",
                "4. Offers comforting words and encouragement",
                "5. Analyzes both text and image inputs for emotional context",
            ],
            markdown=True
        )

        closure_agent = Agent(
            model=model,
            name="Closure Agent",
            instructions=[
                "You are a closure specialist that:",
                "1. Creates emotional messages for unsent feelings",
                "2. Helps express raw, honest emotions",
                "3. Formats messages clearly with headers",
                "4. Ensures tone is heartfelt and authentic",
            ],
            markdown=True
        )

        routine_planner_agent = Agent(
            model=model,
            name="Routine Planner Agent",
            instructions=[
                "You are a recovery routine planner that:",
                "1. Designs 7-day recovery challenges",
                "2. Includes fun activities and self-care tasks",
                "3. Suggests social media detox strategies",
                "4. Creates empowering playlists",
            ],
            markdown=True
        )

        brutal_honesty_agent = Agent(
            model=model,
            name="Brutal Honesty Agent",
            instructions=[
                "You are a direct feedback specialist that:",
                "1. Gives raw, objective feedback about breakups",
                "2. Explains relationship failures clearly",
                "3. Uses blunt, factual language",
                "4. Provides reasons to move forward",
            ],
            markdown=True
        )

        return therapist_agent, closure_agent, routine_planner_agent, brutal_honesty_agent

    except ImportError as e:
        st.error(
            "Dependency error while loading Agno/Ollama.\n\n"
            f"Current Python: `{sys.version.split()[0]}`\n\n"
            "Use the project Python 3.11 environment and update dependencies:\n"
            "`venv/bin/python3.11 -m pip install -U agno ollama`\n"
            "Run the app with:\n"
            "`venv/bin/python3.11 -m streamlit run ai_breakup_recovery_agent.py`\n\n"
            f"Original error: `{str(e)}`"
        )
        return None, None, None, None
    except Exception as e:
        st.error(f"Error initializing agents: {str(e)}")
        return None, None, None, None


# -------------------- STREAMLIT UI --------------------
st.set_page_config(
    page_title="💔 Breakup Recovery Squad",
    page_icon="💔",
    layout="wide"
)

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.header("🦙 Ollama Configuration")

    if "ollama_host_input" not in st.session_state:
        st.session_state.ollama_host_input = DEFAULT_OLLAMA_HOST

    if "ollama_model_input" not in st.session_state:
        st.session_state.ollama_model_input = DEFAULT_OLLAMA_MODEL

    ollama_host = st.text_input(
        "Ollama host",
        value=st.session_state.ollama_host_input,
    )

    if ollama_host != st.session_state.ollama_host_input:
        st.session_state.ollama_host_input = ollama_host

    ollama_model = st.text_input(
        "Ollama model",
        value=st.session_state.ollama_model_input,
        help="Use `llama3.2` for text-only support or a vision-capable model like `llama3.2-vision` for screenshots.",
    )

    if ollama_model != st.session_state.ollama_model_input:
        st.session_state.ollama_model_input = ollama_model

    if ollama_host and ollama_model:
        st.success("Ollama configuration provided ✅")
    else:
        st.warning("Please enter your Ollama host and model to proceed")


# -------------------- MAIN UI --------------------
st.title("💔 Breakup Recovery Squad")

st.markdown("""
### Your AI-powered breakup recovery team is here to help!
Share your feelings and chat screenshots, and we'll guide you through recovery.
""")

col1, col2 = st.columns(2)

with col1:
    user_input = st.text_area(
        "How are you feeling?",
        height=150,
        placeholder="Tell your story..."
    )

with col2:
    uploaded_files = st.file_uploader(
        "Upload chat screenshots (optional)",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for file in uploaded_files:
            st.image(file, caption=file.name, use_container_width=True)


# -------------------- IMAGE PROCESSING --------------------
def process_images(files):
    from agno.media import Image as AgnoImage

    processed_images = []

    for file in files:
        try:
            temp_path = os.path.join(tempfile.gettempdir(), file.name)

            with open(temp_path, "wb") as f:
                f.write(file.getvalue())

            processed_images.append(AgnoImage(filepath=Path(temp_path)))

        except Exception as e:
            logger.error(f"Image error: {str(e)}")

    return processed_images


# -------------------- MAIN LOGIC --------------------
if st.button("Get Recovery Plan 💝"):

    if not ollama_host or not ollama_model:
        st.warning("Please enter your Ollama host and model first")
        st.stop()

    if uploaded_files and not is_vision_model(ollama_model):
        st.warning(
            "Your selected Ollama model does not look vision-capable. "
            "Use a model like `llama3.2-vision` if you want screenshot analysis."
        )
        st.stop()

    agents = initialize_agents(ollama_model, ollama_host)

    if not all(agents):
        st.error("Agent initialization failed")
        st.stop()

    if not user_input and not uploaded_files:
        st.warning("Please enter feelings or upload images")
        st.stop()

    therapist_agent, closure_agent, routine_agent, honesty_agent = agents

    images = process_images(uploaded_files) if uploaded_files else []

    st.header("Your Recovery Plan")

    # ---------------- Therapist ----------------
    with st.spinner("🤗 Emotional Support..."):
        response = therapist_agent.run(user_input, images=images)
        st.subheader("🤗 Emotional Support")
        st.markdown(response.content)

    # ---------------- Closure ----------------
    with st.spinner("✍️ Closure..."):
        response = closure_agent.run(user_input, images=images)
        st.subheader("✍️ Closure")
        st.markdown(response.content)

    # ---------------- Routine ----------------
    with st.spinner("📅 Recovery Plan..."):
        response = routine_agent.run(user_input, images=images)
        st.subheader("📅 Recovery Plan")
        st.markdown(response.content)

    # ---------------- Honesty ----------------
    with st.spinner("💪 Honest Feedback..."):
        response = honesty_agent.run(user_input, images=images)
        st.subheader("💪 Honest Perspective")
        st.markdown(response.content)


# -------------------- FOOTER --------------------
st.markdown("---")
st.markdown(
    "<center>Made with ❤️ | Breakup Recovery Squad</center>",
    unsafe_allow_html=True
)
