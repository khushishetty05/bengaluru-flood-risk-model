import fiona
import geopandas as gpd

# Enable KML driver
fiona.drvsupport.supported_drivers["KML"] = "rw"
fiona.drvsupport.supported_drivers["LIBKML"] = "rw"

kml_path = "data/raw/01_Ward_Boundaries/bbmp_ward_map_2022.kml"
output_path = "data/processed/wards_40_clipped.geojson"

print("Loading KML file...")
gdf = gpd.read_file(kml_path, driver="KML")

# Detect the exact column names for Ward Name and Ward No
name_col = None
no_col = None

for col in gdf.columns:
    col_lower = col.lower()
    if "ward" in col_lower and "name" in col_lower:
        name_col = col
    elif "ward" in col_lower and ("no" in col_lower or "num" in col_lower):
        no_col = col

# Fallback detection if headers differ
if not name_col:
    name_col = [c for c in gdf.columns if gdf[c].astype(str).str.contains("Ward|Layout|Town", regex=True).any()][0]

print(f"Using Ward Name column: {name_col}")
print(f"Total wards in raw dataset: {len(gdf)}")

# Define target selection (First 40 wards or a custom list of ward numbers/names)
# By default, extracting the first 40 wards:
gdf_40 = gdf.iloc[:40].copy()

# Ensure standard WGS84 CRS (EPSG:4326) for Web Mapping (Leaflet)
if gdf_40.crs is None:
    gdf_40.set_crs(epsg=4326, inplace=True)
else:
    gdf_40 = gdf_40.to_crs(epsg=4326)

# Save to processed GeoJSON
gdf_40.to_file(output_path, driver="GeoJSON")
print(f"\nSuccessfully extracted {len(gdf_40)} wards!")
print(f"Saved to: {output_path}")