import streamlit as st
import importlib

st.set_page_config(page_title="Document Rule Validator", layout="wide")

# Sidebar navigation
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📄 Document Extractor", "📘 Rule Parser", "✅ Validator"])

if page == "🏠 Home":
    # Create three columns and center content in the middle one
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # st.markdown("### 📄🧠✅")
        st.title("Document Rule Validator!")
        st.markdown(
            "_AI-powered automation for validating business documents against natural language rules._"
        )

        st.markdown("### What does this app do?")
        st.markdown("- 🔹 Parse human-readable rules to structured format")
        st.markdown("- 📄 Extract fields from PDFs or images")
        st.markdown("- ✅ Validate the extracted data against rules")
        st.markdown("- 📊 See pass/fail results in a clear report")

        st.info("Need help? Use real samples from the sidebar pages to test the flow.")

elif page == "📄 Document Extractor":
    mod = importlib.import_module("document_extractor")
    mod.render()

elif page == "📘 Rule Parser":
    mod = importlib.import_module("rule_parser")
    mod.render()

elif page == "✅ Validator":
    mod = importlib.import_module("validator")
    mod.render()
