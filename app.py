"""
Invisible Until Invited — The Rural Pre-Faculty Readiness Matrix
BNGAP 2026, NYC

Streamlit app companion to the abstract:
"Invisible Until Invited: Rewriting the Pre-Faculty Pipeline in
Rural Medical Schools Through Data, Identity, and Academic Socialization"

Author: Dr. Paris N. Johnson
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Invisible Until Invited — BNGAP 2026",
    page_icon="🪞",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# COLORS & CONSTANTS
# ============================================================
QUADRANT_COLORS = {
    "Emerging Faculty": "#5A8A47",
    "Invisible Scholars": "#D8A032",
    "Aspirational": "#4877A8",
    "Unexposed": "#C76841",
}

QUADRANT_MEANING = {
    "Emerging Faculty": {
        "label": "Already Invited",
        "desc": "Identity infrastructure and engagement converge. Pipeline visible and operating.",
    },
    "Invisible Scholars": {
        "label": "Invisible Until Invited",
        "desc": "Engagement is high; identity infrastructure is thin. Trainees self-exclude before invitation.",
    },
    "Aspirational": {
        "label": "Capacity Without Mission",
        "desc": "Identity infrastructure exists; engagement softer. Capacity outpaces mission integration.",
    },
    "Unexposed": {
        "label": "Pre-Pipeline",
        "desc": "Neither identity nor engagement signals strong. Highest-priority structural gap.",
    },
}

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    df = pd.read_csv("appalachian_medical_schools.csv")
    return df

df = load_data()

# ============================================================
# HEADER
# ============================================================
st.markdown(
    """
    <div style='border-bottom:3px solid #1F3864;padding-bottom:8px;margin-bottom:16px;'>
      <h1 style='color:#1F3864;margin-bottom:4px;'>Invisible Until Invited</h1>
      <p style='color:#666;font-size:15px;font-style:italic;margin:0;'>
        Rewriting the Pre-Faculty Pipeline in Rural Medical Schools — BNGAP 2026, NYC
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR — FILTERS
# ============================================================
st.sidebar.header("Filters")

degree_filter = st.sidebar.multiselect(
    "Degree", options=sorted(df["Degree"].unique()), default=sorted(df["Degree"].unique())
)

state_filter = st.sidebar.multiselect(
    "State", options=sorted(df["State"].unique()), default=sorted(df["State"].unique())
)

arc_scope = st.sidebar.radio(
    "ARC scope",
    ["All (20)", "Strict ARC (17)", "Outside ARC (3)"],
    index=0,
)

quadrant_filter = st.sidebar.multiselect(
    "Pipeline state",
    options=list(QUADRANT_COLORS.keys()),
    default=list(QUADRANT_COLORS.keys()),
)

inst_type_filter = st.sidebar.multiselect(
    "Institution type",
    options=sorted(df["Institution_Type"].unique()),
    default=sorted(df["Institution_Type"].unique()),
)

rural_filter = st.sidebar.radio(
    "Rural mission",
    ["Both", "Rural-mission only", "Non-rural only"],
    index=0,
)

distressed_only = st.sidebar.toggle("Distressed/at-risk counties only")

# Apply filters
filtered = df.copy()
filtered = filtered[filtered["Degree"].isin(degree_filter)]
filtered = filtered[filtered["State"].isin(state_filter)]
if arc_scope == "Strict ARC (17)":
    filtered = filtered[filtered["In_ARC"] == 1]
elif arc_scope == "Outside ARC (3)":
    filtered = filtered[filtered["In_ARC"] == 0]
filtered = filtered[filtered["Quadrant"].isin(quadrant_filter)]
filtered = filtered[filtered["Institution_Type"].isin(inst_type_filter)]
if rural_filter == "Rural-mission only":
    filtered = filtered[filtered["Rural_Focus"] == 1]
elif rural_filter == "Non-rural only":
    filtered = filtered[filtered["Rural_Focus"] == 0]
if distressed_only:
    filtered = filtered[filtered["Distressed_Flag"] == 1]

# ============================================================
# KPIs
# ============================================================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Schools", len(filtered))
with col2:
    st.metric("Matriculants/yr", f"{int(filtered['Matriculants_Annual'].sum()):,}")
with col3:
    invisible = len(filtered[filtered["Quadrant"] == "Invisible Scholars"])
    st.metric("Invisible Scholars", invisible)
with col4:
    distressed = len(filtered[filtered["Distressed_Flag"] == 1])
    st.metric("Distressed/at-risk", distressed)

st.markdown("---")

# ============================================================
# THE MATRIX
# ============================================================
st.header("The Rural Pre-Faculty Readiness Matrix")
st.caption("Each circle is a medical school. Color = pipeline state. Size = mentorship density. Hover any dot for details.")

def build_matrix(data, with_self=False, self_x=None, self_y=None, self_name=None, self_q=None):
    fig = go.Figure()

    # Quadrant background tints
    fig.add_shape(type="rect", x0=50, x1=100, y0=50, y1=100,
                  fillcolor="#5A8A47", opacity=0.07, line_width=0, layer="below")
    fig.add_shape(type="rect", x0=0, x1=50, y0=50, y1=100,
                  fillcolor="#D8A032", opacity=0.10, line_width=0, layer="below")
    fig.add_shape(type="rect", x0=50, x1=100, y0=0, y1=50,
                  fillcolor="#4877A8", opacity=0.07, line_width=0, layer="below")
    fig.add_shape(type="rect", x0=0, x1=50, y0=0, y1=50,
                  fillcolor="#C76841", opacity=0.07, line_width=0, layer="below")

    # Boundary lines
    fig.add_hline(y=50, line_dash="dash", line_color="#666", line_width=1)
    fig.add_vline(x=50, line_dash="dash", line_color="#666", line_width=1)

    # Quadrant labels
    labels = [
        (75, 97, "EMERGING FACULTY", "#5A8A47"),
        (25, 97, "INVISIBLE SCHOLARS", "#D8A032"),
        (75, 3, "ASPIRATIONAL", "#4877A8"),
        (25, 3, "UNEXPOSED", "#C76841"),
    ]
    for x, y, txt, color in labels:
        fig.add_annotation(x=x, y=y, text=f"<b>{txt}</b>", showarrow=False,
                           font=dict(color=color, size=11), opacity=0.7)

    # School dots
    for q, color in QUADRANT_COLORS.items():
        sub = data[data["Quadrant"] == q]
        if len(sub) == 0:
            continue
        fig.add_trace(go.Scatter(
            x=sub["Identity_Score"],
            y=sub["Engagement_Score"],
            mode="markers",
            marker=dict(
                size=np.sqrt(sub["Mentorship_Score"]) * 3.5,
                color=color,
                line=dict(color="white", width=1.6),
                opacity=0.92,
            ),
            name=q,
            customdata=np.stack([
                sub["School_Name"],
                sub["City"] + ", " + sub["State"],
                sub["Quadrant"],
                sub["Identity_Score"],
                sub["Engagement_Score"],
                sub["Mentorship_Score"],
                sub["Visibility_Score"],
                sub["Matriculants_Annual"],
                sub["Pct_In_State"],
                sub["NIH_Funding_Millions"],
                sub["Faculty_Count"],
                sub["ARC_Economic_Status"],
            ], axis=-1),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "%{customdata[1]}<br>"
                "<b>%{customdata[2]}</b><br>"
                "<br>"
                "Identity: %{customdata[3]} | Engagement: %{customdata[4]}<br>"
                "Mentorship: %{customdata[5]} | Visibility: %{customdata[6]}<br>"
                "<br>"
                "Matriculants: %{customdata[7]}/yr (%{customdata[8]}% in-state)<br>"
                "NIH: $%{customdata[9]}M | Faculty: %{customdata[10]}<br>"
                "ARC: %{customdata[11]}"
                "<extra></extra>"
            ),
        ))

    # Self placement star
    if with_self and self_x is not None:
        fig.add_trace(go.Scatter(
            x=[self_x],
            y=[self_y],
            mode="markers+text",
            marker=dict(symbol="star", size=22, color="#000",
                        line=dict(color="white", width=2)),
            text=[self_name],
            textposition="middle right",
            textfont=dict(size=13, color="#000"),
            name="Your institution",
            hovertemplate=(
                f"<b>{self_name}</b><br>"
                f"Quadrant: {self_q}<br>"
                f"Identity: {self_x} | Engagement: {self_y}"
                "<extra></extra>"
            ),
            showlegend=True,
        ))

    fig.update_layout(
        xaxis=dict(title="Identity Score →", range=[0, 100], showgrid=True, gridcolor="#eee"),
        yaxis=dict(title="↑ Engagement Score", range=[0, 100], showgrid=True, gridcolor="#eee"),
        height=620,
        plot_bgcolor="white",
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=1.15),
        margin=dict(l=60, r=140, t=20, b=60),
    )
    return fig

st.plotly_chart(build_matrix(filtered), use_container_width=True)

st.markdown("---")

# ============================================================
# MAP
# ============================================================
st.header("Geographic Distribution")
st.caption("Hover any school for its full profile. Color = pipeline state. Size = matriculants.")

map_fig = go.Figure()
for q, color in QUADRANT_COLORS.items():
    sub = filtered[filtered["Quadrant"] == q]
    if len(sub) == 0:
        continue
    map_fig.add_trace(go.Scattergeo(
        lon=sub["Longitude"],
        lat=sub["Latitude"],
        text=sub["School_Name"],
        marker=dict(
            size=np.sqrt(sub["Matriculants_Annual"]) * 1.5,
            color=color,
            line=dict(color="white", width=1.5),
            opacity=0.92,
        ),
        name=q,
        customdata=np.stack([
            sub["School_Name"],
            sub["City"] + ", " + sub["State"],
            sub["County"],
            sub["Quadrant"],
            sub["Degree"],
            sub["Matriculants_Annual"],
            sub["Faculty_Count"],
            sub["NIH_Funding_Millions"],
            sub["ARC_Economic_Status"],
        ], axis=-1),
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "%{customdata[1]} — %{customdata[2]} County<br>"
            "<b>%{customdata[3]}</b><br>"
            "<br>"
            "Degree: %{customdata[4]}<br>"
            "Matriculants: %{customdata[5]}/yr<br>"
            "Faculty: %{customdata[6]}<br>"
            "NIH: $%{customdata[7]}M<br>"
            "ARC: %{customdata[8]}"
            "<extra></extra>"
        ),
    ))

map_fig.update_layout(
    geo=dict(
        scope="usa",
        projection=dict(type="albers usa"),
        showland=True,
        landcolor="#f5f5f5",
        showsubunits=True,
        subunitcolor="#ddd",
    ),
    height=520,
    margin=dict(l=0, r=0, t=10, b=0),
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
)

st.plotly_chart(map_fig, use_container_width=True)

st.markdown("---")

# ============================================================
# RESOURCE GAP
# ============================================================
st.header("The Resource Asymmetry")
st.caption("Total NIH research funding by pipeline state.")

if len(filtered) > 0:
    nih_by_q = filtered.groupby("Quadrant", as_index=False)["NIH_Funding_Millions"].sum()
    nih_by_q = nih_by_q.sort_values("NIH_Funding_Millions", ascending=False)
    nih_by_q["color"] = nih_by_q["Quadrant"].map(QUADRANT_COLORS)

    nih_fig = go.Figure(go.Bar(
        x=nih_by_q["Quadrant"],
        y=nih_by_q["NIH_Funding_Millions"],
        marker_color=nih_by_q["color"],
        text=[f"${v:,.0f}M" for v in nih_by_q["NIH_Funding_Millions"]],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Total NIH: $%{y}M<extra></extra>",
    ))
    nih_fig.update_layout(
        yaxis_title="Total NIH funding ($M)",
        height=360,
        plot_bgcolor="white",
        margin=dict(l=60, r=20, t=20, b=60),
    )
    st.plotly_chart(nih_fig, use_container_width=True)

st.markdown("---")

# ============================================================
# PILLAR PROFILE
# ============================================================
st.header("The Five Pillars of Pre-Faculty Readiness")

if len(filtered) == 0:
    st.warning("No schools match the current filters. Adjust the sidebar to see the pillar profile.")
else:
    pillar_school = st.selectbox(
        "Select a school to view its pillar profile:",
        options=sorted(filtered["School_Name"].tolist()),
    )
    s = filtered[filtered["School_Name"] == pillar_school].iloc[0]
    c = QUADRANT_COLORS[s["Quadrant"]]

    pillars = [
        ("Identity", s["Identity_Score"]),
        ("Engagement", s["Engagement_Score"]),
        ("Mentorship", s["Mentorship_Score"]),
        ("Protected Time", s["Protected_Time_Ratio"] * 100),
        ("Messaging", s["Messaging_Exposure"]),
    ]
    p_df = pd.DataFrame(pillars, columns=["pillar", "value"])

    pillar_fig = go.Figure(go.Bar(
        x=p_df["value"],
        y=p_df["pillar"],
        orientation="h",
        marker=dict(color=c, opacity=0.85),
        text=[f"{v:.0f}" for v in p_df["value"]],
        textposition="outside",
        hovertemplate="<b>%{y}</b>: %{x:.0f}/100<extra></extra>",
    ))
    pillar_fig.add_vline(x=50, line_dash="dash", line_color="#999")
    pillar_fig.update_layout(
        xaxis=dict(range=[0, 110], title="0–100"),
        height=290,
        plot_bgcolor="white",
        margin=dict(l=130, r=40, t=20, b=40),
    )
    st.plotly_chart(pillar_fig, use_container_width=True)

st.markdown("---")

# ============================================================
# COMPARE TWO SCHOOLS
# ============================================================
st.header("Compare Two Schools")
st.caption("Side-by-side view of any two institutions.")

col_a, col_b = st.columns(2)
all_schools = sorted(df["School_Name"].tolist())

with col_a:
    school_a_name = st.selectbox(
        "School A",
        options=all_schools,
        index=all_schools.index("University of Pikeville Kentucky College of Osteopathic Medicine")
            if "University of Pikeville Kentucky College of Osteopathic Medicine" in all_schools else 0,
        key="school_a",
    )
with col_b:
    school_b_name = st.selectbox(
        "School B",
        options=all_schools,
        index=all_schools.index("University of Pittsburgh School of Medicine")
            if "University of Pittsburgh School of Medicine" in all_schools else 0,
        key="school_b",
    )

a = df[df["School_Name"] == school_a_name].iloc[0]
b = df[df["School_Name"] == school_b_name].iloc[0]
ca = QUADRANT_COLORS[a["Quadrant"]]
cb = QUADRANT_COLORS[b["Quadrant"]]

cmp_col1, cmp_col2 = st.columns(2)
with cmp_col1:
    st.markdown(
        f"<div style='padding:14px;border:2px solid {ca};border-radius:10px;background:#fafafa;'>"
        f"<div style='font-weight:700;color:#1F3864;font-size:14px;'>{a['School_Name']}</div>"
        f"<div style='display:inline-block;background:{ca};color:white;padding:3px 10px;"
        f"border-radius:4px;font-size:10px;font-weight:700;letter-spacing:0.5px;margin-top:4px;'>"
        f"{a['Quadrant'].upper()}</div></div>",
        unsafe_allow_html=True,
    )
with cmp_col2:
    st.markdown(
        f"<div style='padding:14px;border:2px solid {cb};border-radius:10px;background:#fafafa;'>"
        f"<div style='font-weight:700;color:#1F3864;font-size:14px;'>{b['School_Name']}</div>"
        f"<div style='display:inline-block;background:{cb};color:white;padding:3px 10px;"
        f"border-radius:4px;font-size:10px;font-weight:700;letter-spacing:0.5px;margin-top:4px;'>"
        f"{b['Quadrant'].upper()}</div></div>",
        unsafe_allow_html=True,
    )

cmp_rows = [
    ("Location", f"{a['City']}, {a['State']}", f"{b['City']}, {b['State']}"),
    ("County · ARC", f"{a['County']} · {a['ARC_Economic_Status']}",
                     f"{b['County']} · {b['ARC_Economic_Status']}"),
    ("Degree · Type", f"{a['Degree']} · {a['Institution_Type']}",
                      f"{b['Degree']} · {b['Institution_Type']}"),
    ("Matriculants/yr", f"{a['Matriculants_Annual']}", f"{b['Matriculants_Annual']}"),
    ("% In-state", f"{a['Pct_In_State']}%", f"{b['Pct_In_State']}%"),
    ("Faculty", f"{a['Faculty_Count']:,}", f"{b['Faculty_Count']:,}"),
    ("Trainees / faculty",
        f"{a['Matriculants_Annual'] / a['Faculty_Count']:.2f}",
        f"{b['Matriculants_Annual'] / b['Faculty_Count']:.2f}"),
    ("NIH ($M)", f"${a['NIH_Funding_Millions']}M", f"${b['NIH_Funding_Millions']}M"),
    ("Identity Score", f"{a['Identity_Score']}", f"{b['Identity_Score']}"),
    ("Engagement Score", f"{a['Engagement_Score']}", f"{b['Engagement_Score']}"),
    ("Mentorship Score", f"{a['Mentorship_Score']}", f"{b['Mentorship_Score']}"),
    ("Protected Time Ratio", f"{a['Protected_Time_Ratio']}", f"{b['Protected_Time_Ratio']}"),
    ("Messaging Exposure", f"{a['Messaging_Exposure']}", f"{b['Messaging_Exposure']}"),
    ("Visibility Score", f"{a['Visibility_Score']}", f"{b['Visibility_Score']}"),
]
cmp_df = pd.DataFrame(cmp_rows, columns=["Field", school_a_name, school_b_name])
st.dataframe(cmp_df, use_container_width=True, hide_index=True)

st.markdown("---")

# ============================================================
# APPLY TO YOUR INSTITUTION
# ============================================================
st.header("Apply to Your Institution")
st.caption(
    "Place your own school on the matrix. Pick a real school to use as a starting point, "
    "or switch to manual mode and use the sliders to model your own."
)

mode = st.radio(
    "Mode",
    ["Use a school's actual scores", "Enter scores for my institution"],
    horizontal=True,
)

if mode == "Use a school's actual scores":
    pick_name = st.selectbox(
        "Pick a school",
        options=all_schools,
        index=all_schools.index("University of Pikeville Kentucky College of Osteopathic Medicine")
            if "University of Pikeville Kentucky College of Osteopathic Medicine" in all_schools else 0,
        key="self_pick",
    )
    s_pick = df[df["School_Name"] == pick_name].iloc[0]
    default_name = s_pick["School_Name"]
    default_id = int(s_pick["Identity_Score"])
    default_eng = int(s_pick["Engagement_Score"])
    default_men = int(s_pick["Mentorship_Score"])
    default_pt = float(s_pick["Protected_Time_Ratio"])
    default_msg = int(s_pick["Messaging_Exposure"])
else:
    default_name = "Your Institution"
    default_id = 40
    default_eng = 70
    default_men = 45
    default_pt = 0.10
    default_msg = 35

self_name = st.text_input("Institution name", value=default_name)

self_col1, self_col2 = st.columns(2)
with self_col1:
    self_identity = st.slider(
        "Identity (visibility of academic role models, research density)",
        0, 100, default_id,
    )
    self_engagement = st.slider(
        "Engagement (mission alignment, community-engaged training)",
        0, 100, default_eng,
    )
    self_mentorship = st.slider(
        "Mentorship (faculty access for academic-track interest)",
        0, 100, default_men,
    )
with self_col2:
    self_protected = st.slider(
        "Protected time (fraction for scholarship)",
        0.0, 1.0, default_pt, step=0.01,
    )
    self_messaging = st.slider(
        "Messaging (institutional signaling re: academic medicine)",
        0, 100, default_msg,
    )

# Compute quadrant
if self_identity >= 50 and self_engagement >= 50:
    self_quadrant = "Emerging Faculty"
elif self_identity < 50 and self_engagement >= 50:
    self_quadrant = "Invisible Scholars"
elif self_identity < 50 and self_engagement < 50:
    self_quadrant = "Unexposed"
else:
    self_quadrant = "Aspirational"

self_color = QUADRANT_COLORS[self_quadrant]

# Render matrix with self
st.plotly_chart(
    build_matrix(df, with_self=True, self_x=self_identity, self_y=self_engagement,
                 self_name=self_name, self_q=self_quadrant),
    use_container_width=True,
)

# Tailored interpretation
lowest_pillar = sorted([
    ("Identity", self_identity),
    ("Mentorship", self_mentorship),
    ("Protected time", self_protected * 100),
    ("Messaging", self_messaging),
], key=lambda x: x[1])[0]

st.markdown(
    f"""
    <div style='border:2px solid {self_color};border-radius:10px;padding:18px;
                margin:14px 0;background:#fafafa;'>
      <div style='display:inline-block;background:{self_color};color:white;
                  padding:5px 12px;border-radius:4px;font-weight:700;
                  font-size:12px;letter-spacing:0.5px;'>
        {self_quadrant.upper()} · {QUADRANT_MEANING[self_quadrant]['label'].upper()}
      </div>
      <h3 style='margin:10px 0 4px 0;color:#1F3864;font-size:18px;'>{self_name}</h3>
      <p style='margin:6px 0;color:#333;line-height:1.5;'>
        {QUADRANT_MEANING[self_quadrant]['desc']}
      </p>
      <p style='margin:6px 0 0 0;color:#666;font-size:13px;'>
        <strong>Lowest pillar:</strong> {lowest_pillar[0]} ({lowest_pillar[1]:.0f}).
        Most actionable lever for moving toward Emerging Faculty.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# ============================================================
# SORTABLE TABLE
# ============================================================
st.header("All Schools — Sortable")

display_cols = [
    "School_Name", "Degree", "State", "Quadrant",
    "Identity_Score", "Engagement_Score", "Mentorship_Score",
    "Visibility_Score", "Matriculants_Annual", "Pct_In_State",
    "NIH_Funding_Millions", "Faculty_Count",
    "ARC_Economic_Status", "Distressed_Flag",
]

st.dataframe(
    filtered[display_cols].sort_values("Identity_Score", ascending=False),
    use_container_width=True,
    hide_index=True,
    column_config={
        "School_Name": "School",
        "NIH_Funding_Millions": st.column_config.NumberColumn("NIH ($M)", format="$%dM"),
        "Pct_In_State": st.column_config.NumberColumn("% In-state", format="%d%%"),
        "ARC_Economic_Status": "ARC",
        "Distressed_Flag": st.column_config.NumberColumn("Distressed"),
    },
)

# ============================================================
# FOOTER
# ============================================================
st.markdown(
    """
    <div style='text-align:center;color:#888;font-size:11px;
                margin-top:30px;padding-top:14px;border-top:1px solid #ddd;'>
      <i>Dr. Paris N. Johnson · BNGAP 2026, NYC ·
      The Rural Pre-Faculty Readiness Matrix</i>
    </div>
    """,
    unsafe_allow_html=True,
)
