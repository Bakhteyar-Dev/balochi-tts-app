import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# ----------------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------------
# Two separate fine-tuned models power the two output scripts:
#   - Arabic script  -> mBART model  (Bakhteyar/mbart-en-to-bal-19k)
#   - Latin script   -> MarianMT model (Bakhteyar/Balochi-Model)

STAR_LABELS = ["Poor", "Fair", "Good", "Very Good", "Excellent"]

TRANSLATION_MODELS = {
    "latin": {
        "id": "Bakhteyar/Balochi-Model",
        "label": "Latin",
        "direction": "ltr",
        "align": "left",
        "font": "'Inter', sans-serif",
    },
    "arabic": {
        "id": "Bakhteyar/mbart-en-to-bal-19k",
        "label": "Arabic",
        "direction": "rtl",
        "align": "right",
        "font": "'Noto Naskh Arabic', serif",
    },
}

# ----------------------------------------------------------------------------
# STYLES (matches the Bakhteyar-AI look used on the other pages)
# ----------------------------------------------------------------------------

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Naskh+Arabic:wght@400;500;700&display=swap');

:root {
    --bv-ink: var(--text-color);
    --bv-muted: color-mix(in srgb, var(--text-color) 60%, transparent);
    --bv-border: color-mix(in srgb, var(--text-color) 16%, transparent);
    --bv-bg-soft: var(--secondary-background-color);
    --bv-card-bg: var(--secondary-background-color);
    --bv-purple: #8a5cf0;
    --bv-purple-dark: #6f3fdc;
    --bv-card-radius: 16px;
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: var(--bv-ink); }
.block-container { padding-top: 3.2rem; max-width: 820px; }

.bv-brand { display: flex; align-items: center; gap: 12px; }
.bv-logo-mark {
    width: 38px;
    height: 38px;
    border-radius: 10px;
    background: linear-gradient(135deg, #8a5cf0, var(--bv-purple-dark));
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.bv-brand-name {
    font-size: 1.4rem;
    font-weight: 700;
    white-space: nowrap;
}
.bv-brand-name .accent { color: var(--bv-purple); }

.bv-hero-title {
    font-size: 2.3rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 8px;
    line-height: 1.15;
}
.bv-hero-sub {
    font-size: 1rem;
    color: var(--bv-muted);
    max-width: 620px;
    line-height: 1.55;
    margin-bottom: 28px;
}

.st-key-input_card, .st-key-result_card {
    background: var(--bv-card-bg);
    border: 1px solid var(--bv-border);
    border-radius: var(--bv-card-radius);
    padding: 24px 26px 8px 26px;
    margin-bottom: 20px;
}
.st-key-input_card > div, .st-key-result_card > div { gap: 0 !important; }
.bv-section-title { font-size: 1.15rem; font-weight: 700; margin-bottom: 4px; }
.bv-section-caption { font-size: 0.85rem; color: var(--bv-muted); margin-bottom: 18px; }

.st-key-script_switch {
    max-width: 320px;
    margin: 0 auto 22px auto;
    background: var(--bv-bg-soft);
    border: 1px solid var(--bv-border);
    border-radius: 999px;
    padding: 4px;
}
.st-key-script_switch div[data-testid="stHorizontalBlock"] { gap: 4px; }
.st-key-script_switch button {
    border-radius: 999px !important;
    font-weight: 700 !important;
    border: none !important;
    transition: all 0.15s ease;
}
.st-key-script_switch button[kind="primary"] {
    background: linear-gradient(135deg, #8a5cf0, var(--bv-purple-dark)) !important;
    color: white !important;
    box-shadow: 0 4px 10px rgba(111, 63, 220, 0.3);
}
.st-key-script_switch button[kind="secondary"] {
    background: transparent !important;
    color: var(--bv-muted) !important;
    box-shadow: none !important;
}
.st-key-script_switch button[kind="secondary"]:hover {
    color: var(--bv-ink) !important;
}

div[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(135deg, var(--bv-purple), var(--bv-purple-dark));
    border: none;
    border-radius: 12px;
    padding: 0.65rem 1.4rem;
    font-weight: 700;
    box-shadow: 0 6px 16px rgba(111, 63, 220, 0.28);
}

.st-key-topbar { border-bottom: 1px solid var(--bv-border); margin-bottom: 30px; padding-bottom: 14px; }
.st-key-topbar div[data-testid="stHorizontalBlock"] { align-items: center; }

.bv-result-text {
    border: 1px solid var(--bv-border);
    border-radius: 12px;
    padding: 16px 18px;
    min-height: 100px;
    font-size: 1.1rem;
    line-height: 1.7;
    background: var(--background-color);
    margin-bottom: 16px;
}

.bv-avg-rating { font-size: 0.85rem; color: var(--bv-muted); margin-top: 6px; }

.st-key-btn_clear button {
    background: linear-gradient(135deg, #22c55e, #16a34a) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    box-shadow: 0 6px 16px rgba(34, 197, 94, 0.28) !important;
}
.st-key-btn_clear button:hover {
    background: linear-gradient(135deg, #16a34a, #15803d) !important;
    color: white !important;
}

@media screen and (max-width: 600px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; padding-top: 3.5rem; }
    .bv-hero-title { font-size: 1.8rem; }
    .bv-hero-sub { font-size: 0.9rem; margin-bottom: 20px; }
    .st-key-input_card, .st-key-result_card { padding: 18px 16px 8px 16px; border-radius: 14px; }
    .st-key-script_switch { max-width: 100%; width: 100%; padding: 5px; margin-bottom: 18px; }
    .st-key-script_switch div[data-testid="column"] { width: 50% !important; flex: 1 1 0 !important; min-width: 0 !important; }
    .st-key-script_switch button { width: 100% !important; min-height: 42px; font-size: 0.9rem !important; }
    div[data-testid="stTextArea"] textarea { font-size: 1rem !important; min-height: 140px !important; }
}

/* ---------- Sidebar navigation styling ---------- */
section[data-testid="stSidebarNav"] a {
    border-radius: 10px;
    margin: 2px 10px;
    padding: 8px 12px;
    color: var(--bv-ink) !important;
    font-weight: 600;
    transition: all 0.15s ease;
}
section[data-testid="stSidebarNav"] a span { color: inherit !important; }
section[data-testid="stSidebarNav"] a:hover {
    background: color-mix(in srgb, var(--bv-purple) 14%, transparent);
}
section[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: linear-gradient(135deg, #8a5cf0, var(--bv-purple-dark)) !important;
    color: white !important;
    box-shadow: 0 4px 10px rgba(111, 63, 220, 0.3);
}
section[data-testid="stSidebarNav"] a[aria-current="page"] span {
    color: white !important;
}
/* Hide default Streamlit navigation */
section[data-testid="stSidebarNav"] {
    display: none !important;
}
</style>
"""

LOGO_SVG = """
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="3" y="9" width="3" height="6" rx="1.5" fill="white" opacity="0.55"/>
    <rect x="8" y="5" width="3" height="14" rx="1.5" fill="white"/>
    <rect x="13" y="2" width="3" height="20" rx="1.5" fill="white" opacity="0.85"/>
    <rect x="18" y="7" width="3" height="10" rx="1.5" fill="white" opacity="0.55"/>
</svg>
"""

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


def translate_text(text: str, script_key: str) -> str:
    model_id = TRANSLATION_MODELS[script_key]["id"]
    tokenizer, model, device = load_translation_model(model_id)

    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        # NOTE: if the mBART model needs a specific forced target-language
        # token, set it here, e.g.:
        # generated = model.generate(**inputs, forced_bos_token_id=tokenizer.lang_code_to_id["bal_Arab"])
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
if "translation_result" not in st.session_state:
    st.session_state.translation_result = None
if "translation_feedback_log" not in st.session_state:
    st.session_state.translation_feedback_log = []

# ----------------------------------------------------------------------------
# PAGE SETUP
# ----------------------------------------------------------------------------

st.set_page_config(page_title="Bakhteyar-AI Translate", page_icon="🌐", layout="centered")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 12px 10px 20px 10px;">
            <div style="font-size: 1.35rem; font-weight: 800; margin-bottom: 4px;">
                Bakhteyar-AI
            </div>
            <div style="font-size: 0.85rem; color: #6b7280; margin-bottom: 22px;">
                Balochi Language Tools
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.page_link("app.py", label="Home", icon="🏠")
    st.page_link("pages/1_🌐_Translation.py", label="Translation", icon="🌐")
    st.page_link("pages/2_🔊_Text_to_Speech.py", label="Text to Speech", icon="🔊")

with st.container(key="topbar"):
    st.markdown(
        f"""
        <div class="bv-brand">
            <div class="bv-logo-mark">{LOGO_SVG}</div>
            <span class="bv-brand-name">Bakhteyar<span class="accent">-AI</span> Translate</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="bv-hero-title">English to Balochi Translation</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="bv-hero-sub">
        Type English text and translate it into Balochi. Choose whether you want the
        result in Latin or Arabic script.
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# INPUT CARD
# ----------------------------------------------------------------------------

with st.container(key="input_card"):
    st.markdown('<div class="bv-section-title">Enter your text</div>', unsafe_allow_html=True)
    st.markdown('<div class="bv-section-caption">Choose the output script, then type your English text below.</div>', unsafe_allow_html=True)

    with st.container(key="script_switch"):
        sw_col1, sw_col2 = st.columns(2)
        with sw_col1:
            if st.button(
                "Balochi-Latin",
                type="primary" if st.session_state.translate_script_key == "latin" else "secondary",
                use_container_width=True,
                key="btn_translate_latin",
            ):
                st.session_state.translate_script_key = "latin"
                st.rerun()
        with sw_col2:
            if st.button(
                "Balochi-Arabic",
                type="primary" if st.session_state.translate_script_key == "arabic" else "secondary",
                use_container_width=True,
                key="btn_translate_arabic",
            ):
                st.session_state.translate_script_key = "arabic"
                st.rerun()

    script_choice = st.session_state.translate_script_key
    current = TRANSLATION_MODELS[script_choice]

    text = st.text_area(
        "Enter English text",
        height=160,
        placeholder="Type English text here... (e.g. The weather is nice today.)",
        label_visibility="collapsed",
        key="bv_translate_input",
    )

    btn_col1, btn_col2 = st.columns([3, 1])
    with btn_col1:
        translate_clicked = st.button(
            "Translate",
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
# TRANSLATION
# ----------------------------------------------------------------------------

if translate_clicked:
    clean_text = text.strip()

    if not clean_text:
        st.warning("Please enter English text first.")
    else:
        with st.spinner(f"Translating to Balochi ({current['label']} script)..."):
            try:
                translated = translate_text(clean_text, script_choice)
                st.session_state.translation_result = {
                    "text": translated,
                    "source": clean_text,
                    "script": script_choice,
                    "rated": False,
                }
            except Exception as error:
                st.session_state.translation_result = None
                st.error(f"Could not translate text: {error}")

# ----------------------------------------------------------------------------
# RESULT
# ----------------------------------------------------------------------------

if st.session_state.translation_result:
    result = st.session_state.translation_result
    result_script = TRANSLATION_MODELS[result["script"]]

    with st.container(key="result_card"):
        st.markdown('<div class="bv-section-title">Translation</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="bv-section-caption">{result_script["label"]} script</div>', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="bv-result-text" style="
                direction:{result_script['direction']};
                text-align:{result_script['align']};
                font-family:{result_script['font']};">
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

        st.markdown('<div class="bv-section-title" style="font-size:0.95rem; margin-top:20px;">Rate this translation</div>', unsafe_allow_html=True)

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
                st.session_state.translation_feedback_log.append(STAR_LABELS.index(rating_label) + 1)
                st.session_state.translation_result["rated"] = True
                st.toast(f"Thanks for rating it {rating_label}!", icon="⭐")

        if st.session_state.translation_feedback_log:
            avg = sum(st.session_state.translation_feedback_log) / len(st.session_state.translation_feedback_log)
            st.markdown(
                f'<div class="bv-avg-rating">Average rating: {avg:.1f} / 5 '
                f'from {len(st.session_state.translation_feedback_log)} rating(s)</div>',
                unsafe_allow_html=True,
            )
