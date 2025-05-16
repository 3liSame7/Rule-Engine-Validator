import streamlit as st
import requests
import json

def render():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("✅ Rule Validator")
        st.markdown("Fields and rules are auto-filled from the previous steps.")

        if "summary_totals" not in st.session_state:
            st.session_state.summary_totals = {"total": 0, "passed": 0, "failed": 0}
        if "last_payload" not in st.session_state:
            st.session_state.last_payload = {}

        default_fields = json.dumps(st.session_state.get("extracted_fields", {}), indent=2)
        default_rules = json.dumps(st.session_state.get("parsed_rules", []), indent=2)

        st.markdown("#### 📥 Extracted Fields (JSON)")
        fields_input = st.text_area("Auto-filled fields", value=default_fields, height=200)

        st.markdown("#### 📥 Parsed Rules (JSON)")
        rules_input = st.text_area("Auto-filled rules", value=default_rules, height=200)

        col_validate, col_clear = st.columns(2)

        with col_validate:
            if st.button("✅ Validate"):
                try:
                    fields = json.loads(fields_input)
                    rules = json.loads(rules_input)

                    if not isinstance(fields, dict):
                        st.error("❌ 'Extracted Fields' must be a JSON object.")
                        return
                    if not isinstance(rules, list):
                        st.error("❌ 'Parsed Rules' must be a JSON array.")
                        return

                    payload = {"fields": fields, "rules": rules}

                    # Detect repeated validations (same data)
                    if payload == st.session_state.last_payload:
                        st.info("ℹ️ Same input detected. Skipping duplicate validation.")
                        return

                    res = requests.post("https://rule-engine-validator.onrender.com/validate", json=payload)
                    res.raise_for_status()
                    result = res.json()

                    summary = result.get("summary", {})
                    st.session_state.summary_totals["total"] += summary.get("total", 0)
                    st.session_state.summary_totals["passed"] += summary.get("passed", 0)
                    st.session_state.summary_totals["failed"] += summary.get("failed", 0)

                    st.session_state.last_payload = payload
                    st.success("✅ Validation summary updated")

                except json.JSONDecodeError:
                    st.error("❌ Invalid JSON format.")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ API Error: {str(e)}")

        with col_clear:
            if st.button("🗑️ Clear"):
                st.session_state.summary_totals = {"total": 0, "passed": 0, "failed": 0}
                st.session_state.last_payload = {}
                st.info("Summary has been reset.")

        st.markdown("### 📊 Summary")
        st.json(st.session_state.summary_totals)
