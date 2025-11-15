import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Analyst OS – Sketch to Insight", page_icon="🧩", layout="wide")

@st.cache_data(ttl=300)
def load_csv(path_or_url: str):
    return pd.read_csv(path_or_url)

def dataset_loader():
    st.sidebar.header("Datasets")
    src_a = st.sidebar.radio("Source A", ["Upload", "Repo"], index=1)
    src_b = st.sidebar.radio("Source B", ["Upload", "Repo"], index=1)
    df_a = None; df_b = None
    if src_a == "Upload":
        f = st.sidebar.file_uploader("Upload A (CSV)", type=["csv"], key="a")
        if f: df_a = pd.read_csv(f)
    else:
        p = st.sidebar.text_input("Repo path A", value="data/sample_a.csv")
        df_a = load_csv(p)
    if src_b == "Upload":
        f2 = st.sidebar.file_uploader("Upload B (CSV)", type=["csv"], key="b")
        if f2: df_b = pd.read_csv(f2)
    else:
        p2 = st.sidebar.text_input("Repo path B", value="data/sample_b.csv")
        df_b = load_csv(p2)
    return df_a, df_b

def page_translate(df_a, df_b):
    st.subheader("Data dialect translator")
    sql = st.text_area("Sketch SQL (demo only)", value="SELECT * FROM A LIMIT 20")
    st.caption("Tip: Replace with DuckDB integration later.")
    st.dataframe(df_a.head(20))
    st.dataframe(df_b.head(20))

def page_temporal(df_a, df_b):
    st.subheader("Temporal fusion (demo)")
    st.caption("Select time columns to align nearest timestamps (full logic in temporal.py).")
    st.dataframe(df_a.head(10))
    st.dataframe(df_b.head(10))

def page_scenario(df_a):
    st.subheader("Scenario lab (demo)")
    cols = df_a.select_dtypes(include="number").columns.tolist()
    mult_target = st.multiselect("Targets", cols, default=cols[:1] if cols else [])
    mult_val = st.slider("Multiplier", 0.5, 1.5, 1.1)
    out = df_a.copy()
    for c in mult_target:
        out[c] = out[c] * mult_val
    st.dataframe(out.head(20))

def main():
    st.title("🧩 Analyst OS – Sketch to Insight")
    st.caption("Dialects → Temporal joins → Scenarios → Provenance → Briefs")

    df_a, df_b = dataset_loader()
    if df_a is None or df_b is None or df_a.empty or df_b.empty:
        st.info("Load two datasets (A and B) from repo or upload via sidebar.")
        return

    tabs = st.tabs(["Translate", "Temporal fusion", "Scenario"])
    with tabs[0]:
        page_translate(df_a, df_b)
    with tabs[1]:
        page_temporal(df_a, df_b)
    with tabs[2]:
        page_scenario(df_a)

if __name__ == "__main__":
    main()
