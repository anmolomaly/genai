import streamlit as st
from pdfreader import extract_text_from_file
from llm_engine import get_system_prompt, stream_llm_response

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="GRAMMARLY-LITE",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODERN DESIGN SYSTEM (CSS) ---
st.markdown("""
    <style>
    :root {
        --primary-color: #4CAF50;
        --secondary-color: #2E7D32;
        --background-color: #f8f9fa;
        --text-color: #2c3e50;
    }

    /* Main App Container */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Headers and Text */
    h1, h2, h3 {
        color: #1b5e20 !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700 !important;
    }

    /* Text Area Styling */
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 2px solid #e0e0e0 !important;
        transition: all 0.3s ease;
        font-size: 15px !important;
        background-color: white !important;
        padding: 15px !important;
    }
    .stTextArea textarea:focus {
        border-color: #4CAF50 !important;
        box-shadow: 0 0 10px rgba(76, 175, 80, 0.2) !important;
    }

    /* Button Styling */
    div.stButton > button {
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div.stButton > button[kind="primary"] {
        background-color: #2E7D32 !important;
        border: none !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #1b5e20 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }

    /* Sidebar Styling */
    .css-1d391kg {
        background-color: #ffffff !important;
    }

    /* Mode Selection Cards */
    .mode-card {
        padding: 20px;
        border-radius: 15px;
        background: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid #eee;
    }
    </style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'user_text' not in st.session_state: st.session_state.user_text = ""
if 'app_mode' not in st.session_state: st.session_state.app_mode = None

# --- SIDEBAR & NAVIGATION ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/grammar.png", width=60)
    st.title("GRAMMARLY-LITE")
    st.caption("AI-Powered Writing Assistant")
    st.divider()

    if st.session_state.app_mode:
        if st.button("⬅️ Switch Mode", use_container_width=True):
            st.session_state.app_mode = None
            st.rerun()
        st.divider()

    st.subheader("⚙️ Settings")
    model_choice = st.selectbox("LLM Model", options=["llama3.2", "llama3.1", "llama3"], index=0, help="Choose the AI model size/version.")
    output_length = st.select_slider("Output Length", options=["Short", "Medium", "Long"], value="Medium")
    current_tone = st.text_input("Custom Tone", value="Professional", placeholder="e.g. Enthusiastic, Academic")
    
    st.divider()
    st.info("Ensure Ollama is running locally with the selected model pulled.")

# --- MAIN INTERFACE ---
if st.session_state.app_mode is None:
    st.markdown("<h1 style='text-align: center;'>Welcome to Grammarly-Lite</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #555;'>Enhance your writing with local AI power</p>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="mode-card">', unsafe_allow_html=True)
        st.subheader("📑 Summarize")
        st.write("Extract key points from long texts or PDFs.")
        if st.button("Open Summarizer", key="btn_sum", use_container_width=True):
            st.session_state.app_mode = "Summarization"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="mode-card">', unsafe_allow_html=True)
        st.subheader("✍️ Correct")
        st.write("Fix grammar, spelling, and style instantly.")
        if st.button("Open Corrector", key="btn_gram", use_container_width=True):
            st.session_state.app_mode = "Grammar Correction"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="mode-card">', unsafe_allow_html=True)
        st.subheader("💡 Create")
        st.write("Generate creative content from prompts.")
        if st.button("Open Creator", key="btn_creative", use_container_width=True):
            st.session_state.app_mode = "Creative Generation"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.title(f"{st.session_state.app_mode}")
    
    if st.session_state.app_mode in ["Summarization", "Grammar Correction"]:
        # File Uploader
        uploaded_file = st.file_uploader("📂 Upload a document (PDF or TXT)", type=["txt", "pdf"])
        
        if uploaded_file:
            if st.session_state.get("current_file") != uploaded_file.name:
                with st.spinner("Extracting text..."):
                    st.session_state.user_text = extract_text_from_file(uploaded_file)
                    st.session_state.current_file = uploaded_file.name
                st.rerun()

        # Input Area
        input_text = st.text_area("Original Text", key="user_text", height=300, placeholder="Paste your text here...")
        
        if st.button("🚀 Process Now", type="primary", use_container_width=True):
            if not input_text.strip():
                st.warning("⚠️ Please provide some text first.")
            else:
                system_prompt = get_system_prompt(st.session_state.app_mode, output_length, current_tone)
                
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.info("**Reference Input:**")
                    st.write(input_text if len(input_text) < 500 else input_text[:500] + "...")
                
                with res_col2:
                    st.success("**✨ AI Output:**")
                    res_p = st.empty()
                    full_res = ""
                    try:
                        for chunk in stream_llm_response(input_text, system_prompt, model=model_choice):
                            full_res += chunk
                            res_p.markdown(full_res + "▌")
                        res_p.markdown(full_res)
                    except Exception as e:
                        st.error(f"Error: {e}")

    else:
        # Creative Mode
        prompt_input = st.text_area("Writing Prompt", height=200, placeholder="What should I write for you today?")
        
        if st.button("🎨 Generate Magic", type="primary", use_container_width=True):
            if not prompt_input.strip():
                st.warning("⚠️ Please enter a prompt.")
            else:
                system_prompt = get_system_prompt(st.session_state.app_mode, output_length, current_tone)
                
                st.write("---")
                res_p = st.empty()
                full_res = ""
                for chunk in stream_llm_response(prompt_input, system_prompt, model=model_choice):
                    full_res += chunk
                    res_p.markdown(full_res + "▌")
                res_p.markdown(full_res)

