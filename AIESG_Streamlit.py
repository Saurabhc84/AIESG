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

## New code start

base = alt.Chart(filtered).encode(
    x=alt.X(
        "date:T",
        title="Date",
        axis=alt.Axis(
            format="%d-%b",
            labelAngle=-45,
            grid=False
        )
    ),
    tooltip=[
        alt.Tooltip("scenario:N", title="Scenario"),
        alt.Tooltip("date:T", title="Date", format="%d-%b-%Y"),
        alt.Tooltip("final_esg_score:Q", title="Total ESG Score", format=".2f")
    ]
)

line_total = base.mark_line(
    point=True,
    strokeWidth=3
).encode(
    y=alt.Y(
        "final_esg_score:Q",
        title="Total ESG Score",
        scale=alt.Scale(domain=[0, 100])
    )
)

st.altair_chart(line_total, use_container_width=True)

##New Code end

nearest = alt.selection_point(nearest=True, on="mouseover", fields=["date"], empty=False)

line = alt.Chart(filtered).mark_line(strokeWidth=3).encode(
    x=alt.X("date:T", axis=alt.Axis(format="%d-%b", labelAngle=-45)),
    y=alt.Y("final_esg_score:Q", title="Total ESG Score"),
)

points = line.mark_circle(size=80).encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
).add_params(nearest)

tooltips = alt.Chart(filtered).mark_rule(color="gray").encode(
    x="date:T",
    opacity=alt.condition(nearest, alt.value(0.4), alt.value(0)),
    tooltip=[
        alt.Tooltip("date:T", format="%d-%b-%Y"),
        alt.Tooltip("final_esg_score:Q", title="ESG Score", format=".2f")
    ],
).add_params(nearest)

chart = line + points + tooltips

st.altair_chart(chart, use_container_width=True)



line_total = alt.Chart(filtered).mark_line(point=True, strokeWidth=3).encode(
    x=alt.X("date:T", axis=alt.Axis(format="%d-%b", labelAngle=-45)),
    y=alt.Y("final_esg_score:Q", title="Total ESG Score"),
    color=alt.condition(
        alt.datum.final_esg_score >= 70,
        alt.value("#2ca02c"),  # green
        alt.value("#d62728")   # red
    ),
    tooltip=["date:T", "final_esg_score"]
)
