import streamlit as st
import requests

def render():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("📘 Rule Parser")
        st.markdown("Enter your rule in natural language and get its JSON format.")

        rule_text = st.text_area("Enter your rule in plain English")

        if st.button("Parse Rule"):
            if not rule_text.strip():
                st.warning("Please provide rule text before parsing.")
            else:
                try:
                    res = requests.post("http://rule-engine:8000/parse-rule", json={"rule_text": rule_text})
                    res.raise_for_status()
                    parsed_rule = res.json()["parsed_rule"]
                    st.success("Parsed Rule:")
                    st.json([parsed_rule])
                    # ✅ Save to session state
                    st.session_state["parsed_rules"] = [parsed_rule]
                except requests.exceptions.RequestException as e:
                    st.error(f"API Error: {str(e)}")
