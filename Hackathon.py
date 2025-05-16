import streamlit as st
import pandas as pd
import io

st.title("Excel Data Quality Checker")

st.write("""
Upload your data file and DQ rulebook (both as Excel files).
The app will apply your rules and let you download the results.
""")

# File uploaders
data_file = st.file_uploader("Upload Data Excel File", type=["xlsx"])
rules_file = st.file_uploader("Upload DQ Rulebook Excel File", type=["xlsx"])

if data_file and rules_file:
    # Read files
    data_df = pd.read_excel(data_file)
    rules_df = pd.read_excel(rules_file)

    st.subheader("Preview of Data")
    st.dataframe(data_df.head())

    st.subheader("Preview of DQ Rulebook")
    st.dataframe(rules_df.head())

    # Apply rules
    for idx, rule_row in rules_df.iterrows():
        field = rule_row['Field Name']
        dq_dim = rule_row['DQ Dimension']
        rule = rule_row['Python Syntax Rule']
        col_name = f"{field}_{dq_dim}"
        local_env = {'df': data_df}
        try:
            result = eval(rule, {"__builtins__": None}, local_env)
            data_df[col_name] = result
        except Exception as e:
            st.warning(f"Error applying rule {col_name}: {e}")
            data_df[col_name] = None

    st.subheader("Data with DQ Results")
    st.dataframe(data_df.head(20))

    # Download button
    output = io.BytesIO()
    data_df.to_excel(output, index=False)
    output.seek(0)
    st.download_button(
        label="Download DQ Report as Excel",
        data=output,
        file_name="data_with_dq_results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("Please upload both the data file and the DQ rulebook to proceed.")