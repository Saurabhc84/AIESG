import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")

st.title("Transparent ESG Score Monitoring – News driven scenarios")

# ----------------------------------------------------
# Load data generated in Step 11.3
# ----------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("esg_score_timeline.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# ----------------------------------------------------
# Sidebar filters
# ----------------------------------------------------
st.sidebar.header("Filters")

min_date = df["date"].min()
max_date = df["date"].max()

date_range = st.sidebar.slider(
    "Select date range",
    min_value=min_date.to_pydatetime(),
    max_value=max_date.to_pydatetime(),
    value=(min_date.to_pydatetime(), max_date.to_pydatetime())
)

all_scenarios = df["scenario"].unique().tolist()

selected_scenarios = st.sidebar.multiselect(
    "Select news scenarios",
    options=all_scenarios,
    default=all_scenarios
)

# ----------------------------------------------------
# Apply filters
# ----------------------------------------------------
filtered = df[
    (df["date"] >= pd.to_datetime(date_range[0])) &
    (df["date"] <= pd.to_datetime(date_range[1])) &
    (df["scenario"].isin(selected_scenarios))
]


"""
# ----------------------------------------------------
# Main ESG score chart
# ----------------------------------------------------
st.subheader("Total ESG score (news driven)")

base = alt.Chart(filtered).encode(
    x=alt.X(
        "date:T",
        title="Date",
        axis=alt.Axis(format="%Y-%m-%d")  # or "%d-%b-%Y"
    ),
    tooltip=["scenario", "date", "final_esg_score"]
)
line_total = base.mark_line(point=True).encode(
    y=alt.Y("final_esg_score:Q", title="Total ESG score")
)

st.altair_chart(line_total, use_container_width=True)
"""
# ----------------------------------------------------
# Small multiple charts for E, S, G
# ----------------------------------------------------
st.subheader("Pillar level contribution")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Environmental (E)**")
    chart_e = alt.Chart(filtered).mark_line(point=True).encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("E_score:Q", title="E score"),
        tooltip=["scenario", "date", "E_score"]
    )
    st.altair_chart(chart_e, use_container_width=True)

with col2:
    st.markdown("**Social (S)**")
    chart_s = alt.Chart(filtered).mark_line(point=True).encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("S_score:Q", title="S score"),
        tooltip=["scenario", "date", "S_score"]
    )
    st.altair_chart(chart_s, use_container_width=True)

with col3:
    st.markdown("**Governance (G)**")
    chart_g = alt.Chart(filtered).mark_line(point=True).encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("G_score:Q", title="G score"),
        tooltip=["scenario", "date", "G_score"]
    )
    st.altair_chart(chart_g, use_container_width=True)

# ----------------------------------------------------
# Scenario table for audit transparency
# ----------------------------------------------------
st.subheader("Scenario level audit table")

st.dataframe(
    filtered.sort_values("date")[
        ["date", "scenario", "final_esg_score", "E_score", "S_score", "G_score"]
    ],
    use_container_width=True
)

