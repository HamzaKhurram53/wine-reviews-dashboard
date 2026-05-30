"""
app.py — Wine Reviews Dashboard (Direct Mirror)
Main Streamlit application with dark luxury theme, KPI cards,
10 chart types, and 6 interactive filters.
"""

import streamlit as st
import pandas as pd
import numpy as np
from filters import load_and_merge_data, get_filter_options, apply_filters
from charts import (
    pie_chart, histogram, line_chart, bar_chart, scatter_plot,
    box_plot, heatmap, area_chart, count_plot, violin_plot,
)

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Wine Reviews Dashboard",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS — Dark Luxury Theme ────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lato:wght@300;400;600&display=swap');

/* Main background */
.stApp {
    background-color: #0B1120;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0F1629 !important;
    border-right: 1px solid rgba(201, 168, 76, 0.15);
}
[data-testid="stSidebar"] * {
    color: #E8E0D0 !important;
}

/* Header */
header[data-testid="stHeader"] {
    background-color: #0B1120 !important;
}

/* All headings */
h1 {
    font-family: 'Playfair Display', serif !important;
    color: #C9A84C !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px;
}
h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #C9A84C !important;
    font-weight: 600 !important;
}

/* Body text */
p, span, label, .stMarkdown, div {
    font-family: 'Lato', sans-serif !important;
    color: #E8E0D0;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #141B2D 0%, #0F1629 100%);
    border: 1px solid rgba(201, 168, 76, 0.25);
    border-radius: 10px;
    padding: 16px 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}
[data-testid="stMetric"] label {
    color: #9A8C72 !important;
    font-size: 0.8rem !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}
[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #C9A84C !important;
    font-family: 'Playfair Display', serif !important;
    font-weight: 700 !important;
    font-size: 1.6rem !important;
}

/* Streamlit widgets */
.stSelectbox > div > div,
.stMultiSelect > div > div,
.stTextInput > div > div > input,
.stSlider > div {
    background-color: #141B2D !important;
    border-color: rgba(201, 168, 76, 0.2) !important;
    color: #E8E0D0 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #C9A84C 0%, #8B6914 100%) !important;
    color: #0B1120 !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-family: 'Lato', sans-serif !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 8px 24px !important;
    transition: all 0.3s ease;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #D4AF37 0%, #A07D10 100%) !important;
    box-shadow: 0 4px 15px rgba(201, 168, 76, 0.3);
}

/* Divider */
hr {
    border-color: rgba(201, 168, 76, 0.15) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 1px solid rgba(201, 168, 76, 0.15);
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    color: #9A8C72 !important;
    border-radius: 6px 6px 0 0;
    padding: 8px 20px;
    font-family: 'Lato', sans-serif !important;
}
.stTabs [aria-selected="true"] {
    background-color: rgba(201, 168, 76, 0.1) !important;
    color: #C9A84C !important;
    border-bottom: 2px solid #C9A84C;
}

/* Expander */
.streamlit-expanderHeader {
    color: #C9A84C !important;
    font-family: 'Playfair Display', serif !important;
}

/* Section divider styling */
.section-header {
    color: #C9A84C;
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    font-weight: 600;
    border-bottom: 1px solid rgba(201, 168, 76, 0.2);
    padding-bottom: 8px;
    margin-top: 2rem;
    margin-bottom: 1rem;
}

/* Chart containers */
.stPlotlyChart, [data-testid="stImage"], .stPyplot {
    background: #141B2D;
    border: 1px solid rgba(201, 168, 76, 0.12);
    border-radius: 10px;
    padding: 4px;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0B1120; }
::-webkit-scrollbar-thumb { background: #C9A84C44; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── Load Data ─────────────────────────────────────────────────────────────────
df = load_and_merge_data()
opts = get_filter_options(df)


# ── Sidebar Filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🍷 Filters")
    st.markdown("---")

    # Country multi-select
    selected_countries = st.multiselect(
        "🌍 Country",
        options=opts["countries"],
        default=[],
        placeholder="All countries",
    )

    # Variety multi-select
    selected_varieties = st.multiselect(
        "🍇 Variety",
        options=opts["varieties"],
        default=[],
        placeholder="All varieties",
    )

    st.markdown("---")

    # Points range slider
    points_range = st.slider(
        "⭐ Points Range",
        min_value=opts["points_range"][0],
        max_value=opts["points_range"][1],
        value=opts["points_range"],
    )

    # Price range slider
    price_range = st.slider(
        "💰 Price Range ($)",
        min_value=0.0,
        max_value=min(opts["price_range"][1], 1000.0),
        value=(0.0, min(opts["price_range"][1], 1000.0)),
        step=5.0,
    )

    st.markdown("---")

    # Text search
    search_text = st.text_input("🔍 Search Description", placeholder="e.g. fruity, oak, cherry")

    st.markdown("---")

    # Reset button
    if st.button("↺ Reset All Filters", use_container_width=True):
        st.rerun()


# ── Apply Filters ─────────────────────────────────────────────────────────────
filters_dict = {
    "selected_countries": selected_countries,
    "selected_varieties": selected_varieties,
    "points_range": points_range,
    "price_range": price_range,
    "search_text": search_text,
}

filtered_df = apply_filters(df, filters_dict)


# ── Dashboard Title ───────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 1rem 0 0.5rem 0;">
    <h1 style="font-size: 2.4rem; margin-bottom: 0.2rem;">🍷 Wine Reviews Dashboard</h1>
    <p style="color: #9A8C72; font-size: 1rem; font-style: italic; margin-top: 0;">
        Exploring {total:,} wine reviews from Wine Enthusiast · {countries} countries · {varieties} varieties
    </p>
</div>
""".format(
    total=len(filtered_df),
    countries=filtered_df["country"].nunique(),
    varieties=filtered_df["variety"].nunique(),
), unsafe_allow_html=True)

st.markdown("---")

# ── KPI Cards ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5, k6 = st.columns(6)

with k1:
    st.metric("Total Reviews", f"{len(filtered_df):,}")
with k2:
    st.metric("Countries", f"{filtered_df['country'].nunique()}")
with k3:
    avg_pts = filtered_df["points"].mean()
    st.metric("Avg Points", f"{avg_pts:.1f}" if pd.notna(avg_pts) else "—")
with k4:
    avg_price = filtered_df["price"].mean()
    st.metric("Avg Price", f"${avg_price:.0f}" if pd.notna(avg_price) else "—")
with k5:
    if len(filtered_df) > 0 and filtered_df["points"].notna().any():
        best = filtered_df.loc[filtered_df["points"].idxmax()]
        st.metric("Highest Rated", f"{int(best['points'])} pts")
    else:
        st.metric("Highest Rated", "—")
with k6:
    if len(filtered_df) > 0 and filtered_df["price"].notna().any():
        pricey = filtered_df.loc[filtered_df["price"].idxmax()]
        st.metric("Most Expensive", f"${pricey['price']:,.0f}")
    else:
        st.metric("Most Expensive", "—")

st.markdown("")

# ── Guard: empty data ─────────────────────────────────────────────────────────
if len(filtered_df) == 0:
    st.warning("No data matches the current filters. Please adjust your selections.")
    st.stop()


# ── Charts ────────────────────────────────────────────────────────────────────

# Section 1: Distribution Overview
st.markdown('<p class="section-header">📊 Distribution Overview</p>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.pyplot(pie_chart(filtered_df))
with col2:
    st.pyplot(histogram(filtered_df))

# Section 2: Price & Ratings Analysis
st.markdown('<p class="section-header">💎 Price & Ratings Analysis</p>', unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    st.pyplot(line_chart(filtered_df))
with col4:
    st.pyplot(scatter_plot(filtered_df))

# Section 3: Comparative Analysis
st.markdown('<p class="section-header">📈 Comparative Analysis</p>', unsafe_allow_html=True)
col5, col6 = st.columns(2)
with col5:
    st.pyplot(bar_chart(filtered_df))
with col6:
    st.pyplot(box_plot(filtered_df))

# Section 4: Deep Dive
st.markdown('<p class="section-header">🔬 Deep Dive</p>', unsafe_allow_html=True)
col7, col8 = st.columns(2)
with col7:
    st.pyplot(heatmap(filtered_df))
with col8:
    st.pyplot(area_chart(filtered_df))

# Section 5: Category Insights
st.markdown('<p class="section-header">🏷️ Category Insights</p>', unsafe_allow_html=True)
col9, col10 = st.columns(2)
with col9:
    st.pyplot(count_plot(filtered_df))
with col10:
    st.pyplot(violin_plot(filtered_df))


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding: 1rem 0; color: #9A8C72;">
    <p style="font-size: 0.85rem;">
        Wine Reviews Dashboard · Data: Wine Enthusiast · Built with Streamlit, Pandas, Matplotlib & Seaborn
    </p>
</div>
""", unsafe_allow_html=True)
