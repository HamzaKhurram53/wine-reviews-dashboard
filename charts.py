"""
charts.py — All chart/visualization functions for the Wine Reviews Dashboard.
Uses Matplotlib + Seaborn with a dark luxury color palette.
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import seaborn as sns
import numpy as np
import pandas as pd

# ── Color Palette ──────────────────────────────────────────────────────────────
GOLD = "#C9A84C"
DARK_BG = "#0B1120"
CARD_BG = "#141B2D"
TEXT_COLOR = "#E8E0D0"
TEAL = "#2A6B5E"
GRID_COLOR = "#1E2A3E"

PALETTE = [
    "#C9A84C", "#2A6B5E", "#D4AF37", "#3D8B74", "#8B6914",
    "#4A9E85", "#B8941F", "#245E4A", "#E6C35C", "#1A4A3D",
    "#F0D878", "#5AB89A", "#A07D10", "#6ECBAD", "#705B0A",
]

def _apply_dark_style(ax, fig):
    """Apply consistent dark theme to any axes."""
    fig.patch.set_facecolor(CARD_BG)
    ax.set_facecolor(CARD_BG)
    ax.tick_params(colors=TEXT_COLOR, which="both")
    ax.xaxis.label.set_color(TEXT_COLOR)
    ax.yaxis.label.set_color(TEXT_COLOR)
    ax.title.set_color(GOLD)
    ax.title.set_fontweight("bold")
    ax.title.set_fontsize(14)
    for spine in ax.spines.values():
        spine.set_color(GRID_COLOR)
    ax.grid(True, color=GRID_COLOR, alpha=0.3, linestyle="--")


# ── 1. Pie Chart ──────────────────────────────────────────────────────────────
def pie_chart(df):
    """Distribution of wines by top 10 countries."""
    data = df["country"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor(CARD_BG)
    ax.set_facecolor(CARD_BG)

    wedges, texts, autotexts = ax.pie(
        data.values,
        labels=data.index,
        autopct="%1.1f%%",
        colors=PALETTE[:len(data)],
        startangle=140,
        pctdistance=0.82,
        wedgeprops=dict(edgecolor=CARD_BG, linewidth=1.5),
    )
    for t in texts:
        t.set_color(TEXT_COLOR)
        t.set_fontsize(9)
    for t in autotexts:
        t.set_color(DARK_BG)
        t.set_fontsize(8)
        t.set_fontweight("bold")

    ax.set_title("Wine Distribution by Top 10 Countries", color=GOLD, fontsize=14, fontweight="bold", pad=15)
    plt.tight_layout()
    return fig


# ── 2. Histogram ──────────────────────────────────────────────────────────────
def histogram(df):
    """Frequency distribution of points (ratings)."""
    fig, ax = plt.subplots(figsize=(8, 5))
    _apply_dark_style(ax, fig)

    ax.hist(
        df["points"].dropna(), bins=20, color=GOLD, edgecolor=CARD_BG,
        alpha=0.9, linewidth=1.2,
    )
    ax.set_xlabel("Points (Rating)", fontsize=11)
    ax.set_ylabel("Frequency", fontsize=11)
    ax.set_title("Distribution of Wine Ratings")
    plt.tight_layout()
    return fig


# ── 3. Line Chart ─────────────────────────────────────────────────────────────
def line_chart(df):
    """Average price trend across point ranges."""
    fig, ax = plt.subplots(figsize=(8, 5))
    _apply_dark_style(ax, fig)

    temp = df.dropna(subset=["points", "price"])
    grouped = temp.groupby("points")["price"].mean().reset_index()
    grouped = grouped.sort_values("points")

    ax.plot(grouped["points"], grouped["price"], color=GOLD, linewidth=2.5, marker="o", markersize=4, markerfacecolor=TEAL)
    ax.fill_between(grouped["points"], grouped["price"], alpha=0.15, color=GOLD)
    ax.set_xlabel("Points (Rating)", fontsize=11)
    ax.set_ylabel("Average Price ($)", fontsize=11)
    ax.set_title("Average Price by Rating Score")
    plt.tight_layout()
    return fig


# ── 4. Bar Chart ──────────────────────────────────────────────────────────────
def bar_chart(df):
    """Top 15 wine varieties by review count."""
    fig, ax = plt.subplots(figsize=(8, 6))
    _apply_dark_style(ax, fig)

    data = df["variety"].value_counts().head(15)
    bars = ax.barh(data.index[::-1], data.values[::-1], color=PALETTE[:len(data)], edgecolor=CARD_BG, linewidth=0.8)

    for bar in bars:
        width = bar.get_width()
        ax.text(width + max(data.values)*0.01, bar.get_y() + bar.get_height()/2,
                f"{int(width):,}", va="center", color=TEXT_COLOR, fontsize=8)

    ax.set_xlabel("Number of Reviews", fontsize=11)
    ax.set_ylabel("")
    ax.set_title("Top 15 Wine Varieties by Review Count")
    plt.tight_layout()
    return fig


# ── 5. Scatter Plot ───────────────────────────────────────────────────────────
def scatter_plot(df):
    """Price vs Points relationship (sampled)."""
    fig, ax = plt.subplots(figsize=(8, 5))
    _apply_dark_style(ax, fig)

    temp = df.dropna(subset=["points", "price"])
    if len(temp) > 5000:
        temp = temp.sample(5000, random_state=42)

    ax.scatter(temp["points"], temp["price"], c=GOLD, alpha=0.35, s=12, edgecolors="none")
    # Trend line
    z = np.polyfit(temp["points"], temp["price"], 2)
    p = np.poly1d(z)
    x_line = np.linspace(temp["points"].min(), temp["points"].max(), 100)
    ax.plot(x_line, p(x_line), color=TEAL, linewidth=2.5, linestyle="--", label="Trend")

    ax.set_xlabel("Points (Rating)", fontsize=11)
    ax.set_ylabel("Price ($)", fontsize=11)
    ax.set_title("Price vs. Rating Score")
    ax.legend(facecolor=CARD_BG, edgecolor=GOLD, labelcolor=TEXT_COLOR)
    plt.tight_layout()
    return fig


# ── 6. Box Plot ───────────────────────────────────────────────────────────────
def box_plot(df):
    """Price distribution across top 10 countries."""
    fig, ax = plt.subplots(figsize=(8, 6))
    _apply_dark_style(ax, fig)

    top_countries = df["country"].value_counts().head(10).index.tolist()
    temp = df[df["country"].isin(top_countries)].dropna(subset=["price"])

    # Cap extreme outliers for readability
    cap = temp["price"].quantile(0.95)
    temp = temp[temp["price"] <= cap]

    sns.boxplot(
        data=temp, x="country", y="price", order=top_countries,
        palette=PALETTE[:len(top_countries)], ax=ax,
        flierprops=dict(marker="o", markerfacecolor=GOLD, markersize=3, alpha=0.4),
        boxprops=dict(edgecolor=TEXT_COLOR, linewidth=0.8),
        medianprops=dict(color=GOLD, linewidth=2),
        whiskerprops=dict(color=TEXT_COLOR),
        capprops=dict(color=TEXT_COLOR),
    )
    ax.set_xlabel("Country", fontsize=11)
    ax.set_ylabel("Price ($)", fontsize=11)
    ax.set_title("Price Distribution by Top 10 Countries")
    plt.xticks(rotation=35, ha="right", fontsize=9)
    plt.tight_layout()
    return fig


# ── 7. Heatmap ────────────────────────────────────────────────────────────────
def heatmap(df):
    """Correlation & aggregated metrics heatmap."""
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor(CARD_BG)
    ax.set_facecolor(CARD_BG)

    top_countries = df["country"].value_counts().head(8).index.tolist()
    temp = df[df["country"].isin(top_countries)].dropna(subset=["points", "price"])

    pivot = temp.pivot_table(values="points", index="country", columns=pd.cut(temp["price"], bins=5), aggfunc="mean")
    pivot.columns = [f"${int(c.left)}-{int(c.right)}" for c in pivot.columns]

    sns.heatmap(
        pivot, annot=True, fmt=".1f", cmap="YlOrBr", ax=ax,
        linewidths=0.8, linecolor=CARD_BG,
        annot_kws={"fontsize": 9, "color": DARK_BG},
        cbar_kws={"label": "Avg Points"},
    )
    ax.set_title("Avg Points by Country & Price Range", color=GOLD, fontsize=14, fontweight="bold")
    ax.tick_params(colors=TEXT_COLOR)
    ax.xaxis.label.set_color(TEXT_COLOR)
    ax.yaxis.label.set_color(TEXT_COLOR)
    ax.set_xlabel("Price Range", fontsize=11, color=TEXT_COLOR)
    ax.set_ylabel("Country", fontsize=11, color=TEXT_COLOR)
    plt.xticks(rotation=30, ha="right", fontsize=9)
    plt.yticks(fontsize=9)

    cbar = ax.collections[0].colorbar
    cbar.ax.yaxis.set_tick_params(color=TEXT_COLOR)
    cbar.ax.yaxis.label.set_color(TEXT_COLOR)
    plt.setp(plt.getp(cbar.ax.axes, "yticklabels"), color=TEXT_COLOR)

    plt.tight_layout()
    return fig


# ── 8. Area Chart ─────────────────────────────────────────────────────────────
def area_chart(df):
    """Cumulative review count across point score ranges."""
    fig, ax = plt.subplots(figsize=(8, 5))
    _apply_dark_style(ax, fig)

    temp = df["points"].dropna()
    counts = temp.value_counts().sort_index()
    cumulative = counts.cumsum()

    ax.fill_between(cumulative.index, cumulative.values, alpha=0.4, color=GOLD)
    ax.plot(cumulative.index, cumulative.values, color=GOLD, linewidth=2)
    ax.set_xlabel("Points (Rating)", fontsize=11)
    ax.set_ylabel("Cumulative Reviews", fontsize=11)
    ax.set_title("Cumulative Reviews Across Rating Scores")
    plt.tight_layout()
    return fig


# ── 9. Count Plot ─────────────────────────────────────────────────────────────
def count_plot(df):
    """Frequency of wines by province (top 15)."""
    fig, ax = plt.subplots(figsize=(8, 6))
    _apply_dark_style(ax, fig)

    top_provinces = df["province"].value_counts().head(15).index.tolist()
    temp = df[df["province"].isin(top_provinces)]

    sns.countplot(
        data=temp, y="province", order=top_provinces,
        palette=PALETTE[:len(top_provinces)], ax=ax,
        edgecolor=CARD_BG, linewidth=0.8,
    )
    ax.set_xlabel("Number of Reviews", fontsize=11)
    ax.set_ylabel("")
    ax.set_title("Top 15 Provinces by Review Count")
    plt.tight_layout()
    return fig


# ── 10. Violin Plot ──────────────────────────────────────────────────────────
def violin_plot(df):
    """Points distribution across top 8 varieties."""
    fig, ax = plt.subplots(figsize=(8, 6))
    _apply_dark_style(ax, fig)

    top_vars = df["variety"].value_counts().head(8).index.tolist()
    temp = df[df["variety"].isin(top_vars)]

    sns.violinplot(
        data=temp, x="variety", y="points", order=top_vars,
        palette=PALETTE[:len(top_vars)], ax=ax,
        inner="box", linewidth=0.8, saturation=0.85,
    )
    ax.set_xlabel("Variety", fontsize=11)
    ax.set_ylabel("Points (Rating)", fontsize=11)
    ax.set_title("Rating Distribution by Top 8 Varieties")
    plt.xticks(rotation=35, ha="right", fontsize=9)
    plt.tight_layout()
    return fig
