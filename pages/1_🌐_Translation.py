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
inject_theme()
render_sidebar()
render_topbar("Translate")

# ----------------------------------------------------------------------------
# HERO
# ----------------------------------------------------------------------------

st.markdown('<span class="bv-eyebrow">English → Balochi</span>', unsafe_allow_html=True)

st.markdown(
    '<div class="bv-hero-title">Text <span class="grad">Translation</span></div>',
    unsafe_allow_html=True,
)

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
    st.markdown(
        '<div class="bv-section-caption">Choose the output script, then type your English text below.</div>',
        unsafe_allow_html=True,
    )

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
        st.markdown(
            f'<div class="bv-section-caption">{result_script["label"]} script</div>',
            unsafe_allow_html=True,
        )

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
