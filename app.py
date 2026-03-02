import streamlit as st
from graph.workflow import build_graph
import tempfile
import os
import pandas as pd

st.set_page_config(page_title="Multi-Agent Code Reviewer", layout="wide")

st.title("🤖 Multi-Agent Code Review System")
uploaded_file = st.file_uploader("Upload Python file", type=["py"], accept_multiple_files=True)

if uploaded_file:
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

            for uploaded_file in uploaded_file:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
                    tmp.write(uploaded_file.read())
                    file_path = tmp.name

                result = graph.invoke({
                    "file_path": file_path,
                    "results": []
                })

                if isinstance(result, dict) and "final_issues" in result:
                    all_final_issues.extend(result["final_issues"])

                    summary = result.get("summary", {})
                    for key in combined_summary:
                        combined_summary[key] += summary.get(key, 0)

                os.remove(file_path)

        st.subheader("📊 Combined Summary")
        st.json(combined_summary)

        st.subheader("🔎 Issues Across Project")

        for issue in all_final_issues:
            if issue.severity >= 4:
                label = f"🔴 [Severity {issue.severity}] {issue.issue_type}"
            elif issue.severity == 3:
                label = f"🟡 [Severity {issue.severity}] {issue.issue_type}"
            else:
                label = f"🟢 [Severity {issue.severity}] {issue.issue_type}"

            with st.expander(label):
                st.write(f"**File:** {issue.file_path}")
                st.write(f"**Line:** {issue.line_number}")
                st.write(f"**Description:** {issue.description}")
                st.write(f"**Suggested Fix:** {issue.suggested_fix}")
        os.remove(file_path)
        import json

        report_json = {
            "summary": summary,
            "issues": [issue.model_dump() for issue in result.get("final_issues", [])]
        }

        st.download_button(
            label="Download JSON Report",
            data=json.dumps(report_json, indent=2),
            file_name="review_report.json",
            mime="application/json"
        )

        if summary:
            chart_data = pd.DataFrame({
                "Severity": ["Critical", "Serious", "Moderate", "Low"],
                "Count": [
                    summary.get("critical", 0),
                    summary.get("serious", 0),
                    summary.get("moderate", 0),
                    summary.get("low", 0),
                ]
            })

            st.subheader("📈 Severity Distribution")
            st.bar_chart(chart_data.set_index("Severity"))