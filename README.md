```markdown
# Bengaluru Urban Flood Risk Assessment (40 Wards Prototype)

A spatial multi-criteria decision analysis (MCDA) pipeline and interactive web prototype designed to evaluate ward-level flood vulnerability across 40 selected municipal wards in Bengaluru.

---

## 1. Theoretical Framework

Flood risk is evaluated using the standard disaster risk equation:

$$\text{Flood Risk} = \text{Hazard} \times \text{Vulnerability}$$

* **Hazard (Physical Susceptibility):** Combines terrain elevation from ISRO CartoDEM and stormwater drainage density from OpenStreetMap waterways (Raja Kaluves).
* **Vulnerability (Socioeconomic Exposure):** Baseline population density and informal settlement counts derived from census enumeration and municipal slum listings.

All factors are normalized using min-max scaling ($0.0 - 1.0$), with elevation inverted to account for natural water accumulation in low-lying depressions.

---

## 2. Project Architecture

```text
bengaluru_flood_project/
├── data/
│   ├── raw/                 # Ignored from version control (DEM rasters, OSM shapefiles)
│   └── processed/           # Processed layers, intermediate metrics, final GeoJSON
├── scripts/
│   ├── 01_inspect_wards.py           # KML attribute schema validation
│   ├── 02_extract_40_wards.py        # Boundary extraction & EPSG:4326 reprojection
│   ├── 03_process_dem.py             # Raster mosaic & DEM zonal statistics
│   ├── 04_process_drainage.py        # UTM-projected drainage density calculation
│   ├── 05_process_vulnerability.py   # Demographic exposure processing
│   └── 06_compute_risk_index.py      # Normalization and composite risk calculation
├── app/
│   ├── backend/             # FastAPI REST service serving spatial endpoints
│   └── frontend/            # Interactive Leaflet.js analytical dashboard
├── .gitignore               # Excludes large binaries (.tif, .zip, .venv)
└── README.md

```

---

## 3. Data Processing Pipeline

Each script executes a modular stage of the spatial assessment workflow:

1. **`01_inspect_wards.py`**: Reads the raw BBMP 2022 master ward boundary file (`.kml`) to inspect attribute field schemas and identify the naming headers for ward identification.
2. **`02_extract_40_wards.py`**: Filters the master 243-ward dataset down to the 40 target study wards, standardizes coordinate references to `EPSG:4326` (WGS84), and writes `data/processed/wards_40_clipped.geojson`.
3. **`03_process_dem.py`**: Mosaics ISRO Bhuvan CartoDEM 30-meter elevation raster tiles (`cdnd43r.tif` and `cdnd43x.tif`), overlays the 40 study polygons, and performs zonal statistics to extract mean, minimum, and maximum ground elevation in `hazard_terrain_metrics.csv`.
4. **`04_process_drainage.py`**: Loads OpenStreetMap waterways (`gis_osm_waterways_free_1.shp`), projects vectors into UTM Zone 43N (`EPSG:32643`) for metric calculations, clips drains per ward, and calculates total drain length ($km$) and drainage density ($km/km^2$) in `hazard_drainage_metrics.csv`.
5. **`05_process_vulnerability.py`**: Integrates demographic metrics (Census population and informal settlement counts) across the 40 wards into `vulnerability_metrics.csv`.
6. **`06_compute_risk_index.py`**: Applies min-max scaling ($0.0 - 1.0$), inverts ground elevation, computes composite Hazard and Vulnerability scores, assigns final flood risk tiers (Low, Moderate, High, Critical), and writes the consolidated output to `final_flood_risk_40_wards.csv` and `final_flood_risk_40_wards.geojson`.

---

## 4. Environment Setup & Dependencies

### Prerequisites

* Python 3.10+
* Virtual environment (`venv`)

### Installation

```bash
# Clone the repository
git clone [https://github.com/YOUR_USERNAME/REPO_NAME.git](https://github.com/YOUR_USERNAME/REPO_NAME.git)
cd REPO_NAME

# Create and activate virtual environment
python -m venv .venv

# Activate on Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Activate on Linux / macOS:
source .venv/bin/activate

# Install required GIS and Web libraries
pip install geopandas fiona shapely rasterio rasterstats pandas fastapi uvicorn

```

---

## 5. Execution Workflow

### Step 1: Run the Data Pipeline

Run each processing script in numerical order:

```bash
python scripts/01_inspect_wards.py
python scripts/02_extract_40_wards.py
python scripts/03_process_dem.py
python scripts/04_process_drainage.py
python scripts/05_process_vulnerability.py
python scripts/06_compute_risk_index.py

```

### Step 2: Start the FastAPI Backend Service

Launch the local REST API server:

```bash
uvicorn app.backend.main:app --reload --port 8000

```

Available API Endpoints:

* `GET http://127.0.0.1:8000/api/health` - Health status and GeoJSON availability check
* `GET http://127.0.0.1:8000/api/wards` - Returns the complete multi-attribute GeoJSON payload
* `GET http://127.0.0.1:8000/api/ward/{ward_name}` - Returns calculated risk metrics for a single ward

### Step 3: Launch the Interactive Dashboard

1. Navigate to `app/frontend/index.html`.
2. Open the file in any modern web browser or serve it via VS Code Live Server.
3. The dashboard connects to the local API endpoint (`http://127.0.0.1:8000/api/wards`), renders color-coded risk boundaries across the 40 wards, and updates the telemetry sidebar on polygon click.

---

## 6. Output Summary

| Layer Name | Output File | Description |
| --- | --- | --- |
| **Study Boundaries** | `data/processed/wards_40_clipped.geojson` | Standardized study ward boundaries (`EPSG:4326`) |
| **Terrain Metrics** | `data/processed/hazard_terrain_metrics.csv` | Mean, min, and max ground elevation per ward ($m$) |
| **Drainage Metrics** | `data/processed/hazard_drainage_metrics.csv` | Total drain length ($km$) and drainage density ($km/km^2$) |
| **Vulnerability Metrics** | `data/processed/vulnerability_metrics.csv` | Population and slum counts per ward |
| **Composite Risk (Tabular)** | `data/processed/final_flood_risk_40_wards.csv` | Normalized indicators, composite indices, and assigned risk tiers |
| **Composite Risk (Spatial)** | `data/processed/final_flood_risk_40_wards.geojson` | Complete polygon vector dataset ready for web rendering |

```

```
