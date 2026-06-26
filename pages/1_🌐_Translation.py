import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from bv_ui import inject_theme, render_footer, render_sidebar, render_topbar

# ----------------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------------

STAR_LABELS = ["Poor", "Fair", "Good", "Very Good", "Excellent"]

TRANSLATION_MODELS = {
    "latin": {
        "en_to_bal": "Bakhteyar/Balochi-Model",
        "bal_to_en": None,
        "label": "Latin",
        "direction": "ltr",
        "align": "left",
        "font": "'Inter', sans-serif",
    },
    "arabic": {
        "en_to_bal": "Bakhteyar/mbart-en-to-bal-19k",
        "bal_to_en": "Bakhteyar/nllb-balochi-to-english-lora",
        "label": "Arabic",
        "direction": "rtl",
        "align": "right",
        "font": "'Noto Naskh Arabic', serif",
    },
}

# ----------------------------------------------------------------------------
# MODEL LOADING / INFERENCE
# ----------------------------------------------------------------------------

@st.cache_resource(show_spinner=False)
def load_translation_model(model_id: str):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    if "lora" in model_id.lower():
        from peft import PeftModel, PeftConfig
        
        config = PeftConfig.from_pretrained(model_id)
        base_model_id = config.base_model_name_or_path
        
        tokenizer = AutoTokenizer.from_pretrained(base_model_id)
        base_model = AutoModelForSeq2SeqLM.from_pretrained(
            base_model_id, device_map="auto"
        )
        base_model.resize_token_embeddings(len(tokenizer))
        model = PeftModel.from_pretrained(base_model, model_id)
    else:
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForSeq2SeqLM.from_pretrained(
            model_id, device_map="auto"
        )
        
    model.eval()
    return tokenizer, model, device


def translate_text(text: str, script_key: str, direction: str) -> str:
    model_id = TRANSLATION_MODELS[script_key][direction]
    tokenizer, model, device = load_translation_model(model_id)

    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        generated = model.generate(**inputs, max_length=256, num_beams=1)

    return tokenizer.batch_decode(generated, skip_special_tokens=True)[0].strip()

# ----------------------------------------------------------------------------
# CLEAR INPUT
# ----------------------------------------------------------------------------

def clear_input():
    st.session_state["bv_translate_input"] = ""
    st.session_state.translation_result = None

# ----------------------------------------------------------------------------
# SESSION STATE
# ----------------------------------------------------------------------------

if "translate_script_key" not in st.session_state:
    st.session_state.translate_script_key = "latin"

if "translate_direction" not in st.session_state:
    st.session_state.translate_direction = "en_to_bal"

if "translation_result" not in st.session_state:
    st.session_state.translation_result = None

if "translation_feedback_log" not in st.session_state:
    st.session_state.translation_feedback_log = []

# ----------------------------------------------------------------------------
# PAGE SETUP
# ----------------------------------------------------------------------------

st.set_page_config(
    page_title="Bakhteyar-AI Translate",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="expanded",
)
inject_theme()

st.markdown("""
    <style>
    .st-key-direction_switch {
        background: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 999px !important;
        padding: 2px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: fit-content !important;
        margin: 0 auto !important;
        height: 42px !important;
        min-width: 180px !important;
    }
    
    .st-key-dir_green_track { background: #22c55e !important; border-radius: 999px !important; }
    .st-key-dir_blue_track { background: #3b82f6 !important; border-radius: 999px !important; }
    
    .st-key-direction_switch [data-testid="stHorizontalBlock"] {
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        gap: 0 !important;
    }

    .st-key-direction_switch button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 0.8rem !important;
        height: 38px !important;
        padding: 0 12px !important;
        min-width: 0 !important;
        width: auto !important;
    }
    
    .st-key-dir_mid_btn button {
        background: white !important;
        color: #64748b !important;
        width: 34px !important;
        height: 34px !important;
        min-width: 34px !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        margin: 0 8px !important;
        font-size: 1rem !important;
    }
    
    .st-key-dir_mid_btn button p { color: #64748b !important; }

    [data-theme="dark"] .st-key-direction_switch { background: #1e293b !important; border-color: #334155 !important; }
    [data-theme="dark"] .st-key-dir_mid_btn button { background: #f8fafc !important; }
    
    [data-testid="column"] .stButton {
        display: flex !important;
        justify-content: center !important;
    }

    @media screen and (max-width: 640px) {
        .st-key-settings_grid [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            gap: 1.5rem !important;
        }
        .bv-hero-title { margin-top: 15px !important; }
    }
    </style>
""", unsafe_allow_html=True)

render_sidebar()
render_topbar("Translate")

# ----------------------------------------------------------------------------
# HERO
# ----------------------------------------------------------------------------

direction_label = "English → Balochi" if st.session_state.translate_direction == "en_to_bal" else "Balochi → English"
st.markdown(f'<span class="bv-eyebrow">{direction_label}</span>', unsafe_allow_html=True)

st.markdown(
    '<div class="bv-hero-title">Text <span class="grad">Translation</span></div>',
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="bv-hero-sub">
        Translate between English and Balochi. Currently translating in <b>{direction_label}</b> direction using the fine-tuned neural models.
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# INPUT CARD
# ----------------------------------------------------------------------------

with st.container(key="input_card"):
    st.markdown('<div class="bv-section-title">Translation Settings</div>', unsafe_allow_html=True)
    
    with st.container(key="settings_grid"):
        set_col1, set_col2 = st.columns(2)
        
        with set_col1:
            st.markdown('<div class="bv-section-caption">Select Script</div>', unsafe_allow_html=True)
            st.markdown("""
                <style>
                .st-key-script_switch_container button {
                    border-radius: 999px !important;
                    font-weight: 700 !important;
                    height: 42px !important;
                    transition: all 0.2s ease !important;
                }
                .st-key-script_switch_container div[data-testid="column"]:first-child button[kind="primary"],
                .st-key-script_switch_container div[data-testid="column"]:last-child button[kind="primary"] {
                    background: var(--bv-grad) !important;
                    border: none !important;
                    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3) !important;
                }
                </style>
            """, unsafe_allow_html=True)
            
            with st.container(key="script_switch_container"):
                sw_col1, sw_col2 = st.columns(2)
                with sw_col1:
                    if st.button("Latin", type="primary" if st.session_state.translate_script_key == "latin" else "secondary", use_container_width=True, key="btn_lat"):
                        st.session_state.translate_script_key = "latin"
                        st.rerun()
                with sw_col2:
                    if st.button("Arabic", type="primary" if st.session_state.translate_script_key == "arabic" else "secondary", use_container_width=True, key="btn_arb"):
                        st.session_state.translate_script_key = "arabic"
                        st.rerun()

        with set_col2:
            is_latin = st.session_state.translate_script_key == "latin"
            if not is_latin:
                st.markdown('<div class="bv-section-caption" style="text-align:center;">Select Direction</div>', unsafe_allow_html=True)
                
                is_en_to_bal = st.session_state.translate_direction == "en_to_bal"
                track_color = "#22c55e" if is_en_to_bal else "#3b82f6"
                
                st.markdown(f"""
                    <style>
                    .st-key-dir_pill_toggle button {{
                        background: {track_color} !important;
                        color: white !important;
                        border-radius: 999px !important;
                        padding: 0 24px !important;
                        height: 42px !important;
                        border: none !important;
                        font-weight: 700 !important;
                        font-size: 0.9rem !important;
                        width: auto !important;
                        min-width: 180px !important;
                        margin: 0 auto !important;
                        display: block !important;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
                        transition: all 0.2s ease !important;
                    }}
                    .st-key-dir_pill_toggle button:hover {{
                        transform: scale(1.02);
                        opacity: 0.9;
                    }}
                    </style>
                """, unsafe_allow_html=True)
                
                if st.button("ENG    ⇄    بلوچی", key="dir_pill_toggle"):
                    st.session_state.translate_direction = "bal_to_en" if is_en_to_bal else "en_to_bal"
                    st.rerun()
            else:
                st.session_state.translate_direction = "en_to_bal"
                st.markdown('<div style="margin-top: 32px;"></div>', unsafe_allow_html=True)

    script_choice = st.session_state.translate_script_key
    current = TRANSLATION_MODELS[script_choice]
    
    source_dir = "ltr" if st.session_state.translate_direction == "en_to_bal" else current["direction"]
    source_align = "left" if st.session_state.translate_direction == "en_to_bal" else current["align"]
    source_font = "'Inter', sans-serif" if st.session_state.translate_direction == "en_to_bal" else current["font"]
    
    st.markdown(f"""
        <style>
        div[data-testid="stTextArea"] textarea {{
            direction: {source_dir};
            text-align: {source_align};
            font-family: {source_font};
        }}
        </style>
    """, unsafe_allow_html=True)

    input_placeholder = "Type English text here..." if st.session_state.translate_direction == "en_to_bal" else f"Type Balochi ({script_choice}) text here..."
    
    text = st.text_area(
        "Input Text",
        height=160,
        placeholder=input_placeholder,
        label_visibility="collapsed",
        key="bv_translate_input",
    )

    btn_col1, btn_col2 = st.columns([3, 1])

    with btn_col1:
        translate_clicked = st.button(
            "Translate Now",
            type="primary",
            use_container_width=True,
            key="btn_translate",
        )

    with btn_col2:
        st.button(
            "Clear",
            use_container_width=True,
            key="btn_clear",
            on_click=clear_input,
        )

# ----------------------------------------------------------------------------
# TRANSLATION LOGIC
# ----------------------------------------------------------------------------

if translate_clicked:
    clean_text = text.strip()

    if not clean_text:
        st.warning("Please enter some text first.")
    else:
        with st.spinner(f"Translating... ({direction_label})"):
            try:
                translated = translate_text(clean_text, script_choice, st.session_state.translate_direction)

                st.session_state.translation_result = {
                    "text": translated,
                    "source": clean_text,
                    "script": script_choice,
                    "direction": st.session_state.translate_direction,
                    "rated": False,
                }

            except Exception as error:
                st.session_state.translation_result = None
                st.error(f"Could not translate text: {error}")
                st.exception(error)

# --------------------------------------
