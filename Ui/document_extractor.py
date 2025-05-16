import streamlit as st
import requests

def render():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("📄 Document Field Extractor")
        st.markdown("Upload a PDF or image file to extract data.")

        uploaded_file = st.file_uploader("Upload your document", type=["pdf", "jpg", "jpeg", "png"])

        if st.button("Extract Fields"):
            if not uploaded_file:
                st.warning("Please upload a file first.")
            else:
                with st.spinner("Extracting fields..."):
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                    try:
                        res = requests.post("https://rule-engine-validator.onrender.com/extract", files=files)
                        res.raise_for_status()
                        result = res.json()
                        st.success("Extraction completed.")
                        st.subheader("Extracted Fields:")
                        st.json(result.get("fields", {}))
                        if "error" in result:
                            st.error(f"LLM Parsing Error: {result['error']}")
                        # ✅ Save to session state
                        st.session_state["extracted_fields"] = result.get("fields", {})
                    except requests.exceptions.RequestException as e:
                        st.error(f"API Error: {str(e)}")
