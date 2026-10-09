import os
import glob
import geopandas as gpd
import pandas as pd

processed_dir = "data/processed"
raw_hazard_dir = "data/raw/02_Hazard_Data"
wards_geojson = os.path.join(processed_dir, "wards_40_clipped.geojson")
output_csv = os.path.join(processed_dir, "hazard_drainage_metrics.csv")

# 1. Find waterways shapefile
waterway_matches = glob.glob(
    os.path.join(raw_hazard_dir, "**", "*waterways*.shp"),
    recursive=True
)

if not waterway_matches:
    raise FileNotFoundError("Could not find *waterways*.shp in data/raw/02_Hazard_Data/")

waterway_shp = waterway_matches[0]
print(f"Step 1: Using waterways file -> {waterway_shp}")

# 2. Load layers
wards = gpd.read_file(wards_geojson)
waterways = gpd.read_file(waterway_shp)

name_col = None
for col in ["WardName", "WARD_NAME", "Name", "name"]:
    if col in wards.columns:
        name_col = col
        break
if not name_col:
    name_col = wards.columns[0]

# 3. Project to metric system (UTM Zone 43N: EPSG 32643) for kilometer calculation
print("Step 2: Projecting layers to UTM 43N (meters/km)...")
wards_utm = wards.to_crs(epsg=32643)
waterways_utm = waterways.to_crs(epsg=32643)

wards_utm["area_sqkm"] = wards_utm.geometry.area / 1e6

# 4. Clip waterways per ward and sum length
print("Step 3: Calculating total drain length per ward...")
clipped = gpd.overlay(waterways_utm, wards_utm, how="intersection")
clipped["drain_len_km"] = clipped.geometry.length / 1000.0

drain_agg = clipped.groupby(name_col)["drain_len_km"].sum().reset_index()

# 5. Merge with all 40 wards
result_df = pd.DataFrame({
    "ward_name": wards_utm[name_col],
    "area_sqkm": wards_utm["area_sqkm"].round(2)
}).merge(drain_agg.rename(columns={name_col: "ward_name"}), on="ward_name", how="left")

result_df["drain_length_km"] = result_df["drain_len_km"].fillna(0.0).round(2)
result_df["drainage_density_km_per_sqkm"] = (
    result_df["drain_length_km"] / result_df["area_sqkm"]
).round(2)
result_df = result_df.drop(columns=["drain_len_km"])

result_df.to_csv(output_csv, index=False)
print(f"\nSaved drainage metrics to: {output_csv}")
print(result_df.head())