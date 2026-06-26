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
        "bal_to_en": None, # Not supported for Latin
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
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id).to(device)
    model.eval()
    return tokenizer, model, device


def translate_text(text: str, script_key: str, direction: str) -> str:
    model_id = TRANSLATION_MODELS[script_key][direction]
    tokenizer, model, device = load_translation_model(model_id)

    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        generated = model.generate(**inputs, max_length=256, num_beams=4)

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

# Custom CSS for the Direction Toggle
st.markdown("""
    <style>
    /* Direction Toggle Button Styling */
    div.stButton > button[key="btn_toggle_dir"] {
        background: var(--bv-grad) !important;
        color: white !important;
        border: none !important;
        border-radius: 999px !important;
        font-weight: 700 !important;
        padding: 0.5rem 1rem !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button[key="btn_toggle_dir"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4) !important;
    }
    /* Disabled State */
    div.stButton > button[key="btn_toggle_dir_dis"] {
        background: #e2e8f0 !important;
        color: #94a3b8 !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 999px !important;
        font-weight: 600 !important;
        cursor: not-allowed !important;
    }
    [data-theme="dark"] div.stButton > button[key="btn_toggle_dir_dis"] {
        background: #1e293b !important;
        color: #475569 !important;
        border-color: #334155 !important;
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
    
    # Grid for Script and Direction
    set_col1, set_col2 = st.columns(2)
    
    with set_col1:
        st.markdown('<div class="bv-section-caption">Select Script</div>', unsafe_allow_html=True)
        with st.container(key="script_switch"):
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
        st.markdown('<div class="bv-section-caption">Select Direction</div>', unsafe_allow_html=True)
        
        # Disable direction toggle if current script doesn't support bidirectional
        is_latin = st.session_state.translate_script_key == "latin"
        if is_latin:
            st.session_state.translate_direction = "en_to_bal" # Force English to Balochi for Latin
            
        btn_label = f"🔄 {direction_label}"
        if is_latin:
            st.button(btn_label, use_container_width=True, key="btn_toggle_dir_dis", disabled=True, help="Latin script only supports English to Balochi.")
        else:
            if st.button(btn_label, use_container_width=True, key="btn_toggle_dir"):
                st.session_state.translate_direction = "bal_to_en" if st.session_state.translate_direction == "en_to_bal" else "en_to_bal"
                st.rerun()

    script_choice = st.session_state.translate_script_key
    current = TRANSLATION_MODELS[script_choice]
    
    # Input Area styling based on Source Language
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

# ----------------------------------------------------------------------------
# RESULT CARD
# ----------------------------------------------------------------------------

if st.session_state.translation_result:
    result = st.session_state.translation_result
    
    # Determine result styling
    if result["direction"] == "en_to_bal":
        res_dir = TRANSLATION_MODELS[result["script"]]["direction"]
        res_align = TRANSLATION_MODELS[result["script"]]["align"]
        res_font = TRANSLATION_MODELS[result["script"]]["font"]
        res_label = f"Balochi ({TRANSLATION_MODELS[result['script']]['label']} script)"
    else:
        res_dir = "ltr"
        res_align = "left"
        res_font = "'Inter', sans-serif"
        res_label = "English"

    with st.container(key="result_card"):
        st.markdown(f'<div class="bv-section-title">Translation Result</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="bv-section-caption">Output: {res_label}</div>', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="bv-result-text" style="
                direction:{res_dir};
                text-align:{res_align};
                font-family:{res_font};">
                {result['text']}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.download_button(
            "Download as Text",
            data=result["text"],
            file_name=f"bakhtai_translation_{result['script']}.txt",
            mime="text/plain",
            use_container_width=True,
        )

        st.markdown(
            '<div class="bv-section-title" style="font-size:0.95rem; margin-top:20px;">Rate this translation</div>',
            unsafe_allow_html=True,
        )

        has_native_feedback = hasattr(st, "feedback")

        if has_native_feedback:
            rating = st.feedback("stars", key=f"translation_rating_{id(result)}")

            if rating is not None and not result["rated"]:
                st.session_state.translation_feedback_log.append(rating + 1)
                st.session_state.translation_result["rated"] = True
                st.toast(f"Thanks for rating it {STAR_LABELS[rating]}!", icon="⭐")

        else:
            rating_label = st.radio(
                "Rate this translation",
                options=STAR_LABELS,
                horizontal=True,
                label_visibility="collapsed",
                key=f"translation_rating_fallback_{id(result)}",
                index=None,
            )

            if rating_label and not result["rated"]:
                st.session_state.translation_feedback_log.append(
                    STAR_LABELS.index(rating_label) + 1
                )
                st.session_state.translation_result["rated"] = True
                st.toast(f"Thanks for rating it {rating_label}!", icon="⭐")

        if st.session_state.translation_feedback_log:
            avg = sum(st.session_state.translation_feedback_log) / len(
                st.session_state.translation_feedback_log
            )

            st.markdown(
                f'<div class="bv-avg-rating">Average rating: {avg:.1f} / 5 '
                f'from {len(st.session_state.translation_feedback_log)} rating(s)</div>',
                unsafe_allow_html=True,
            )

render_footer()
