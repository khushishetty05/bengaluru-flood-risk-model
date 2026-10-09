import fiona
import geopandas as gpd

kml_path = "data/raw/01_Ward_Boundaries/bbmp_ward_map_2022.kml"

# Enable KML driver support
fiona.drvsupport.supported_drivers["KML"] = "rw"
fiona.drvsupport.supported_drivers["LIBKML"] = "rw"

layers = fiona.listlayers(kml_path)
print(f"Layers found: {layers}")

gdf = gpd.read_file(kml_path, driver="KML")

print("\n--- Dataset Summary ---")
print(f"Total polygons/wards found: {len(gdf)}")
print("\n--- Column / Attribute Names ---")
print(gdf.columns.tolist())

print("\n--- First 5 Rows (Attributes) ---")
print(gdf.drop(columns="geometry").head())