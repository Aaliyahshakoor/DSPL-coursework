
import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="🌿 Sri Lanka Environmental Dashboard", layout="wide")
st.title("🇱🇰 Sri Lanka Environmental Indicators Dashboard")

# Intro
st.markdown("""
Welcome to the **Sri Lanka Environmental Indicators Dashboard**  
Use the sidebar to explore key environmental trends and statistics for Sri Lanka.
""")

# Load data
@st.cache_data
def load_data():
    df_raw = pd.read_csv("clean_environment_lka.csv")
    df_raw.columns = df_raw.columns.str.strip()
    df_raw["Country Name"] = df_raw["Country Name"].str.strip()
    df_raw["Indicator Name"] = df_raw["Indicator Name"].str.strip()

    df = df_raw[df_raw["Country Name"] == "Sri Lanka"].copy()
    df.rename(columns={"Value": "Indicator Value"}, inplace=True)
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["Indicator Value"] = pd.to_numeric(df["Indicator Value"], errors="coerce")
    df = df.dropna(subset=["Year", "Indicator Value"])
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"🚫 Failed to load data: {e}")
    st.stop()

# Sidebar - Indicator selector
st.sidebar.header("🔎 Filter Options")
indicator = st.sidebar.selectbox(
    "Choose an Environmental Indicator",
    sorted(df["Indicator Name"].unique())
)

filtered_df = df[df["Indicator Name"] == indicator]
indicator_code = filtered_df["Indicator Code"].iloc[0] if not filtered_df.empty else "N/A"
st.sidebar.markdown(f"**Indicator Code:** `{indicator_code}`")

# Display content
st.markdown("---")
st.subheader(f"📊 Data Table: {indicator}")
st.dataframe(
    filtered_df[["Year", "Indicator Value"]].sort_values("Year"),
    use_container_width=True,
    hide_index=True
)

# Line chart
st.subheader("📈 Indicator Trend Over Time")
st.line_chart(filtered_df.set_index("Year")["Indicator Value"])

# Summary statistics
st.markdown("### 📌 Summary Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Mean", f"{filtered_df['Indicator Value'].mean():.2f}")
col2.metric("Max", f"{filtered_df['Indicator Value'].max():.2f}")
col3.metric("Min", f"{filtered_df['Indicator Value'].min():.2f}")

# Download button
st.markdown("### ⬇ Download Data")
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name=f"{indicator}_SriLanka.csv",
    mime="text/csv"
)

