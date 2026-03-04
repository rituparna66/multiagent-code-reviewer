import streamlit as st
from graph.workflow import build_graph
import tempfile
import os
import pandas as pd
import json

st.set_page_config(page_title="Multi-Agent Code Reviewer", layout="wide")

st.title("🤖 Multi-Agent Code Review System")
st.caption("Fintech-grade | Security · Performance · Code Quality")

uploaded_files = st.file_uploader("Upload Python file(s)", type=["py"], accept_multiple_files=True)

if uploaded_files:
    if st.button("Analyze Code"):
        with st.spinner("Running multi-agent analysis..."):
            graph = build_graph()

            all_final_issues = []
            combined_summary = {
                "total_issues": 0,
                "critical": 0,
                "serious": 0,
                "moderate": 0,
                "low": 0,
            }
            last_result = None

            for file in uploaded_files:  # ✅ fixed: was reusing uploaded_files variable
                with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
                    tmp.write(file.read())
                    file_path = tmp.name

                try:
                    result = graph.invoke({
                        "file_path": file_path,
                        "results": []
                    })

                    if isinstance(result, dict) and "final_issues" in result:
                        all_final_issues.extend(result["final_issues"])
                        summary = result.get("summary", {})
                        for key in combined_summary:
                            combined_summary[key] += summary.get(key, 0)
                        last_result = result

                finally:
                    if os.path.exists(file_path):
                        os.remove(file_path)  # ✅ fixed: single remove inside finally block

        # ── Summary ──────────────────────────────────────────
        st.subheader("📊 Combined Summary")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🔴 Critical", combined_summary["critical"])
        col2.metric("🟠 Serious",  combined_summary["serious"])
        col3.metric("🟡 Moderate", combined_summary["moderate"])
        col4.metric("🟢 Low",      combined_summary["low"])

        # ── Issues ───────────────────────────────────────────
        st.subheader("🔎 Issues Across Project")

        if not all_final_issues:
            st.success("No issues found!")
        else:
            for issue in all_final_issues:
                if issue.severity >= 4:
                    label = f"🔴 [Severity {issue.severity}] {issue.issue_type.upper()} — {issue.description[:60]}..."
                elif issue.severity == 3:
                    label = f"🟡 [Severity {issue.severity}] {issue.issue_type.upper()} — {issue.description[:60]}..."
                else:
                    label = f"🟢 [Severity {issue.severity}] {issue.issue_type.upper()} — {issue.description[:60]}..."

                with st.expander(label):
                    st.write(f"**File:** {issue.file_path}")
                    st.write(f"**Line:** {issue.line_number if issue.line_number else 'N/A'}")
                    st.write(f"**Description:** {issue.description}")
                    st.write(f"**Suggested Fix:** {issue.suggested_fix if issue.suggested_fix else 'N/A'}")

        # ── Chart ─────────────────────────────────────────────
        st.subheader("📈 Severity Distribution")
        chart_data = pd.DataFrame({
            "Severity": ["Critical", "Serious", "Moderate", "Low"],
            "Count": [
                combined_summary["critical"],
                combined_summary["serious"],
                combined_summary["moderate"],
                combined_summary["low"],
            ]
        })
        st.bar_chart(chart_data.set_index("Severity"))

        # ── Download ──────────────────────────────────────────
        report_json = {
            "summary": combined_summary,  # ✅ fixed: use combined_summary not last summary
            "issues": [issue.model_dump() for issue in all_final_issues]
        }

        st.download_button(
            label="⬇️ Download JSON Report",
            data=json.dumps(report_json, indent=2),
            file_name="review_report.json",
            mime="application/json"
        )