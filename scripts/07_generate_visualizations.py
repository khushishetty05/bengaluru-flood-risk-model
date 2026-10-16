import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import geopandas as gpd

# Set styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

# Directories
processed_dir = "data/processed"
output_dir = "reports/figures"
os.makedirs(output_dir, exist_ok=True)

final_csv = os.path.join(processed_dir, "final_flood_risk_40_wards.csv")
final_geojson = os.path.join(processed_dir, "final_flood_risk_40_wards.geojson")

df = pd.read_csv(final_csv)
gdf = gpd.read_file(final_geojson)

print(f"Loaded {len(df)} ward records for visualization.")

# -------------------------------------------------------------
# 1. Top 15 Wards by Flood Risk Score (Horizontal Bar Chart)
# -------------------------------------------------------------
plt.figure(figsize=(10, 6))
top15 = df.sort_values(by="flood_risk_score", ascending=True).tail(15)

category_colors = {
    "Critical": "#d73027",
    "High": "#fc8d59",
    "Moderate": "#fee08b",
    "Low": "#91bfdb"
}
colors = [category_colors.get(cat, "#4575b4") for cat in top15["risk_category"]]

bars = plt.barh(top15["ward_name"], top15["flood_risk_score"], color=colors, edgecolor="#444444", height=0.65)
plt.xlabel("Flood Risk Score (Composite: Hazard × Vulnerability)", fontsize=11, fontweight="bold")
plt.title("Top 15 Bengaluru Study Wards by Flood Risk Index", fontsize=14, fontweight="bold", pad=12)

# Value annotations
for bar in bars:
    w = bar.get_width()
    plt.text(w + 0.003, bar.get_y() + bar.get_height()/2, f"{w:.3f}", va="center", fontsize=9, fontweight="bold")

plt.xlim(0, max(top15["flood_risk_score"]) * 1.15)
plt.tight_layout()
p1 = os.path.join(output_dir, "01_top_risk_wards.png")
plt.savefig(p1, dpi=300)
plt.close()
print(f"Saved: {p1}")

# -------------------------------------------------------------
# 2. Hazard vs Vulnerability Matrix (Scatter Plot)
# -------------------------------------------------------------
plt.figure(figsize=(9, 7))
scatter = plt.scatter(
    df["hazard_score"],
    df["vulnerability_score"],
    c=df["flood_risk_score"],
    cmap="YlOrRd",
    s=df["population"] / 250,
    alpha=0.85,
    edgecolors="#333333",
    linewidth=1.2
)
cbar = plt.colorbar(scatter)
cbar.set_label("Flood Risk Score", fontsize=11, fontweight="bold")

plt.axvline(x=df["hazard_score"].median(), color="grey", linestyle="--", alpha=0.6, label="Median Hazard")
plt.axhline(y=df["vulnerability_score"].median(), color="grey", linestyle=":", alpha=0.6, label="Median Vulnerability")

# Annotate top 5 highest risk wards
top5 = df.sort_values(by="flood_risk_score", ascending=False).head(5)
for _, r in top5.iterrows():
    plt.annotate(
        r["ward_name"],
        (r["hazard_score"], r["vulnerability_score"]),
        textcoords="offset points",
        xytext=(8, 5),
        fontsize=9,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#999999", alpha=0.8)
    )

plt.xlabel("Hazard Score (Topography & Drainage Concentration)", fontsize=11, fontweight="bold")
plt.ylabel("Vulnerability Score (Population & Informal Settlements)", fontsize=11, fontweight="bold")
plt.title("Hazard vs. Vulnerability Matrix (40 Bengaluru Wards)", fontsize=13, fontweight="bold", pad=12)
plt.legend(loc="lower left", frameon=True)
plt.tight_layout()
p2 = os.path.join(output_dir, "02_hazard_vs_vulnerability_matrix.png")
plt.savefig(p2, dpi=300)
plt.close()
print(f"Saved: {p2}")

# -------------------------------------------------------------
# 3. Topography vs Hazard Score (Inverse Elevation Relation)
# -------------------------------------------------------------
plt.figure(figsize=(9, 6))
sns.regplot(
    data=df,
    x="elevation_mean_m",
    y="hazard_score",
    color="#1f78b4",
    scatter_kws={"s": 60, "alpha": 0.8, "edgecolor": "#111111"},
    line_kws={"color": "#e31a1c", "linewidth": 2}
)
plt.xlabel("Mean Elevation (meters above sea level)", fontsize=11, fontweight="bold")
plt.ylabel("Computed Hazard Score", fontsize=11, fontweight="bold")
plt.title("Topography vs. Flood Hazard: Elevation Inversion Trend", fontsize=13, fontweight="bold", pad=12)
plt.tight_layout()
p3 = os.path.join(output_dir, "03_elevation_vs_hazard.png")
plt.savefig(p3, dpi=300)
plt.close()
print(f"Saved: {p3}")

# -------------------------------------------------------------
# 4. Drainage Density by Ward (Top 15)
# -------------------------------------------------------------
plt.figure(figsize=(10, 6))
top_drain = df.sort_values(by="drainage_density_km_per_sqkm", ascending=True).tail(15)
bars = plt.barh(top_drain["ward_name"], top_drain["drainage_density_km_per_sqkm"], color="#3182bd", edgecolor="#222222", height=0.65)

for bar in bars:
    w = bar.get_width()
    plt.text(w + 0.05, bar.get_y() + bar.get_height()/2, f"{w:.2f}", va="center", fontsize=9, fontweight="bold")

plt.xlabel("Drainage Density (km / sq km)", fontsize=11, fontweight="bold")
plt.title("Top 15 Wards by Natural Drainage Network Density", fontsize=13, fontweight="bold", pad=12)
plt.xlim(0, max(top_drain["drainage_density_km_per_sqkm"]) * 1.15)
plt.tight_layout()
p4 = os.path.join(output_dir, "04_drainage_density_ranking.png")
plt.savefig(p4, dpi=300)
plt.close()
print(f"Saved: {p4}")

# -------------------------------------------------------------
# 5. Spatial Choropleth Map of Bengaluru 40 Wards
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(
    column="flood_risk_score",
    cmap="YlOrRd",
    legend=True,
    edgecolor="#222222",
    linewidth=0.7,
    ax=ax,
    legend_kwds={
        "label": "Flood Risk Score",
        "orientation": "horizontal",
        "shrink": 0.65,
        "pad": 0.03
    }
)
ax.set_title("Geospatial Flood Risk Distribution across 40 Bengaluru Wards", fontsize=14, fontweight="bold", pad=14)
ax.set_axis_off()
plt.tight_layout()
p5 = os.path.join(output_dir, "05_spatial_flood_risk_map.png")
plt.savefig(p5, dpi=300)
plt.close()
print(f"Saved: {p5}")

# -------------------------------------------------------------
# 6. Combined 4-Panel Executive Summary
# -------------------------------------------------------------
fig, axs = plt.subplots(2, 2, figsize=(16, 13))

# Panel A: Top 10 Risk Wards
top10 = df.sort_values(by="flood_risk_score", ascending=True).tail(10)
axs[0, 0].barh(top10["ward_name"], top10["flood_risk_score"], color="#e6550d", edgecolor="#333333", height=0.65)
axs[0, 0].set_title("A. Top 10 High Flood Risk Wards", fontsize=12, fontweight="bold")
axs[0, 0].set_xlabel("Flood Risk Score", fontsize=10)

# Panel B: Hazard vs Vulnerability
sc = axs[0, 1].scatter(df["hazard_score"], df["vulnerability_score"], c=df["flood_risk_score"], cmap="YlOrRd", s=80, edgecolors="#333333")
plt.colorbar(sc, ax=axs[0, 1], label="Risk Score")
axs[0, 1].set_title("B. Hazard vs Vulnerability Mapping", fontsize=12, fontweight="bold")
axs[0, 1].set_xlabel("Hazard Score", fontsize=10)
axs[0, 1].set_ylabel("Vulnerability Score", fontsize=10)

# Panel C: Elevation Trend
sns.regplot(data=df, x="elevation_mean_m", y="hazard_score", ax=axs[1, 0], color="#2b8cbe", scatter_kws={"s": 45, "alpha": 0.8}, line_kws={"color": "#de2d26"})
axs[1, 0].set_title("C. Mean Elevation (m) vs. Hazard Score", fontsize=12, fontweight="bold")
axs[1, 0].set_xlabel("Mean Elevation (m)", fontsize=10)
axs[1, 0].set_ylabel("Hazard Score", fontsize=10)

# Panel D: Risk Category Distribution
cat_counts = df["risk_category"].value_counts()
axs[1, 1].pie(cat_counts, labels=cat_counts.index, autopct="%1.1f%%", colors=["#fc8d59", "#fee08b", "#91bfdb"], startangle=140, wedgeprops={"edgecolor": "white", "linewidth": 2})
axs[1, 1].set_title("D. Ward Distribution across Risk Categories", fontsize=12, fontweight="bold")

plt.suptitle("Bengaluru Urban Flood Risk Assessment Dashboard (40 Study Wards)", fontsize=16, fontweight="bold", y=0.98)
plt.tight_layout()
p6 = os.path.join(output_dir, "06_flood_risk_summary_dashboard.png")
plt.savefig(p6, dpi=300)
plt.close()
print(f"Saved: {p6}")

print("\nAll 6 visualization figures successfully generated!")
