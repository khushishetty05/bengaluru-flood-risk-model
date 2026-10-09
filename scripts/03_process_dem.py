import os
import glob
import numpy as np
import rasterio
from rasterio.merge import merge
import geopandas as gpd
from rasterstats import zonal_stats
import pandas as pd

# Paths
raw_hazard_dir = "data/raw/02_Hazard_Data/cartodem_extracted"
processed_dir = "data/processed"
wards_geojson = os.path.join(processed_dir, "wards_40_clipped.geojson")
merged_dem_path = os.path.join(processed_dir, "bengaluru_dem_merged.tif")
output_csv = os.path.join(processed_dir, "hazard_terrain_metrics.csv")

# 1. Identify raw DEM TIFF files (excluding SRTM auxiliary rasters)
tif_files = glob.glob(os.path.join(raw_hazard_dir, "**", "*.tif"), recursive=True)
dem_tiles = [f for f in tif_files if "srtm" not in os.path.basename(f).lower()]

print(f"Found {len(dem_tiles)} CartoDEM tiles to merge:")
for tile in dem_tiles:
    print(f" - {os.path.basename(tile)}")

# 2. Merge tiles into a single seamless raster
print("\nStep 1/3: Merging elevation tiles...")
src_files_to_mosaic = [rasterio.open(fp) for fp in dem_tiles]
mosaic, out_trans = merge(src_files_to_mosaic)

out_meta = src_files_to_mosaic[0].meta.copy()
out_meta.update({
    "driver": "GTiff",
    "height": mosaic.shape[1],
    "width": mosaic.shape[2],
    "transform": out_trans
})

for src in src_files_to_mosaic:
    src.close()

with rasterio.open(merged_dem_path, "w", **out_meta) as dest:
    dest.write(mosaic)
print(f"Merged DEM saved to: {merged_dem_path}")

# 3. Read 40-ward polygons
print("\nStep 2/3: Loading 40-ward boundaries...")
gdf = gpd.read_file(wards_geojson)

# Verify CRS match with DEM
with rasterio.open(merged_dem_path) as dem_src:
    dem_crs = dem_src.crs
    dem_nodata = dem_src.nodata

if gdf.crs != dem_crs:
    gdf = gdf.to_crs(dem_crs)

# 4. Extract Elevation Zonal Statistics per ward
print("Step 3/3: Calculating mean elevation for each ward...")
elevation_stats = zonal_stats(
    gdf,
    merged_dem_path,
    stats=["mean", "min", "max"],
    nodata=dem_nodata
)

elev_df = pd.DataFrame(elevation_stats).rename(columns={
    "mean": "elevation_mean_m",
    "min": "elevation_min_m",
    "max": "elevation_max_m"
})

# Identify ward name column
name_col = None
for col in ["WardName", "WARD_NAME", "Name", "name"]:
    if col in gdf.columns:
        name_col = col
        break
if not name_col:
    name_col = gdf.columns[0]

results_df = pd.DataFrame({
    "ward_name": gdf[name_col],
    "elevation_mean_m": elev_df["elevation_mean_m"].round(2),
    "elevation_min_m": elev_df["elevation_min_m"].round(2),
    "elevation_max_m": elev_df["elevation_max_m"].round(2)
})

# Save output
results_df.to_csv(output_csv, index=False)
print(f"\nCompleted! Saved terrain metrics to: {output_csv}")
print("\nSample Output (First 5 Wards):")
print(results_df.head())