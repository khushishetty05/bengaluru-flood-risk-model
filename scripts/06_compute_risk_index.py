import os
import pandas as pd
import geopandas as gpd

processed_dir = "data/processed"
terrain_csv = os.path.join(processed_dir, "hazard_terrain_metrics.csv")
drainage_csv = os.path.join(processed_dir, "hazard_drainage_metrics.csv")
vuln_csv = os.path.join(processed_dir, "vulnerability_metrics.csv")
wards_geojson = os.path.join(processed_dir, "wards_40_clipped.geojson")

final_csv = os.path.join(processed_dir, "final_flood_risk_40_wards.csv")
final_geojson = os.path.join(processed_dir, "final_flood_risk_40_wards.geojson")

# 1. Load intermediate datasets
df_terrain = pd.read_csv(terrain_csv)
df_drain = pd.read_csv(drainage_csv)
df_vuln = pd.read_csv(vuln_csv)

# Merge into a single master dataframe
df = df_terrain.merge(df_drain, on="ward_name", how="left")
df = df.merge(df_vuln, on="ward_name", how="left")

# 2. Normalization helper (0.0 to 1.0 scale)
def min_max_norm(series, invert=False):
    min_v, max_v = series.min(), series.max()
    if min_v == max_v:
        return series.apply(lambda x: 0.5)
    norm = (series - min_v) / (max_v - min_v)
    return 1.0 - norm if invert else norm

# Elevation: LOWER elevation means HIGHER hazard (inverted)
df["norm_elevation"] = min_max_norm(df["elevation_mean_m"], invert=True)

# Drainage density: HIGHER density along main channels = higher flow accumulation
df["norm_drainage"] = min_max_norm(df["drainage_density_km_per_sqkm"])

# Population: Higher population = Higher vulnerability
df["norm_pop"] = min_max_norm(df["population"])

# Slums: Higher slum count = Higher sensitivity/vulnerability
df["norm_slums"] = min_max_norm(df["slum_count"])

# 3. Composite Calculation
# Hazard Score (60% low elevation tendency, 40% drainage concentration)
df["hazard_score"] = (0.6 * df["norm_elevation"] + 0.4 * df["norm_drainage"]).round(3)

# Vulnerability Score (50% population density proxy, 50% informal settlement density)
df["vulnerability_score"] = (0.5 * df["norm_pop"] + 0.5 * df["norm_slums"]).round(3)

# Final Risk Index = Hazard x Vulnerability (scaled 0 to 1)
df["flood_risk_score"] = (df["hazard_score"] * df["vulnerability_score"]).round(3)

# Categorize into Risk Tiers
def categorize(score):
    if score >= 0.45:
        return "Critical"
    elif score >= 0.30:
        return "High"
    elif score >= 0.15:
        return "Moderate"
    else:
        return "Low"

df["risk_category"] = df["flood_risk_score"].apply(categorize)

# 4. Save Final CSV
df.to_csv(final_csv, index=False)
print(f"Final tabular metrics saved to: {final_csv}")

# 5. Bake scores into GeoJSON for frontend/Leaflet dashboard
wards_gdf = gpd.read_file(wards_geojson)
name_col = "WardName" if "WardName" in wards_gdf.columns else wards_gdf.columns[0]
merged_gdf = wards_gdf.merge(df, left_on=name_col, right_on="ward_name", how="left")

merged_gdf.to_file(final_geojson, driver="GeoJSON")
print(f"Final GeoJSON saved to: {final_geojson}")

print("\n--- TOP 5 HIGHEST FLOOD RISK WARDS ---")
top_5 = df.sort_values(by="flood_risk_score", ascending=False).head(5)
print(top_5[["ward_name", "hazard_score", "vulnerability_score", "flood_risk_score", "risk_category"]])