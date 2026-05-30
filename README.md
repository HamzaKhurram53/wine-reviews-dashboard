# 🍷 Wine Reviews Dashboard

A professional data visualization dashboard analyzing Wine Enthusiast reviews. Built for the **Exploratory Data Analysis** course.

## Dataset

The dashboard merges two Wine Enthusiast datasets:
- `winemag-data_first150k.csv` — 150,930 reviews (11 features)
- `winemag-data-130k-v2.csv` — 129,971 reviews (14 features)

Combined dataset: ~280,000 reviews covering country, points, price, variety, winery, province, region, taster, and description.

## Features

### 10 Chart Types
1. **Pie Chart** — Wine distribution by top 10 countries
2. **Histogram** — Frequency distribution of ratings
3. **Line Chart** — Average price trend across rating scores
4. **Bar Chart** — Top 15 wine varieties by review count
5. **Scatter Plot** — Price vs. rating relationship
6. **Box Plot** — Price distribution by country
7. **Heatmap** — Average points by country & price range
8. **Area Chart** — Cumulative reviews across rating scores
9. **Count Plot** — Top 15 provinces by review count
10. **Violin Plot** — Rating distribution by top 8 varieties

### 6 Interactive Filters
- **Country** — Multi-select dropdown
- **Variety** — Multi-select dropdown
- **Points Range** — Numerical slider (min–max)
- **Price Range** — Numerical slider (min–max)
- **Search** — Text filter on descriptions
- **Reset** — Clear all filters

All filters are connected to every chart — updating a filter refreshes all visualizations simultaneously.

### KPI Summary Cards
Total Reviews, Countries, Avg Points, Avg Price, Highest Rated, Most Expensive

## Key Insights

- **US dominates** the dataset with the largest share of reviews
- **Higher-rated wines** tend to have exponentially higher prices
- **Pinot Noir, Chardonnay, and Cabernet Sauvignon** are the most reviewed varieties
- **California** leads as the most represented province
- Rating distributions vary significantly by variety — some have tighter clusters than others

## Installation

```bash
pip install -r requirements.txt
```

## Running the Dashboard

```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`.

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.x | Core language |
| Pandas | Data loading, cleaning, filtering |
| NumPy | Numerical operations |
| Matplotlib | Chart creation |
| Seaborn | Statistical visualizations |
| Streamlit | Interactive dashboard interface |

## Project Structure

```
dashboard_project/
├── data/
│   ├── winemag-data_first150k.csv
│   └── winemag-data-130k-v2.csv
├── notebooks/
│   └── analysis.ipynb
├── app.py              # Main dashboard
├── charts.py           # Visualization functions
├── filters.py          # Data loading & filter logic
├── requirements.txt    # Dependencies
└── README.md           # This file
```

## Course Info

- **Course:** Exploratory Data Analysis
- **Instructor:** Ali Hassan Sherazi
- **Submission Date:** June 5, 2026
