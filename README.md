# Bengaluru Urban Flood Risk Assessment (40 Wards Prototype)

A spatial **Multi-Criteria Decision Analysis (MCDA)** pipeline designed to assess ward-level flood risk across 40 selected municipal wards in Bengaluru, Karnataka, India.

The project combines terrain characteristics, drainage infrastructure, and socioeconomic vulnerability indicators to develop a preliminary flood risk assessment. The current focus is on completing the data processing pipeline, with an interactive dashboard planned as a future phase.

---

## 1. Project Overview

Urban flooding is influenced by several factors, including low-lying terrain, drainage infrastructure, population density, and informal settlements.

This project aims to evaluate these factors at the ward level and generate a composite flood risk index for the 40 selected study wards in Bengaluru.

### Theoretical Framework

The assessment follows the conceptual relationship:

**Flood Risk = Hazard × Vulnerability**

- **Hazard:** Represents physical susceptibility to flooding, using terrain elevation and drainage-related indicators.
- **Vulnerability:** Represents socioeconomic exposure, using population density and informal settlement counts.

The input indicators are normalized using Min-Max Scaling to a range of 0 to 1. Elevation is inversely normalized because lower-lying areas may be more susceptible to water accumulation.

The resulting hazard and vulnerability indicators are combined to derive composite flood risk scores and preliminary risk categories.

> Note: The risk index is a prototype analytical model. Its accuracy depends on data quality, indicator selection, weighting assumptions, and validation against observed flood events.

---

## 2. Project Architecture

The repository is organized into data directories and modular Python scripts.

```text
bengaluru_flood_project/
│
├── data/
│   ├── raw/                       # Raw DEM, OSM and source datasets
│   └── processed/                 # Processed spatial layers and metrics
│
├── scripts/
│   ├── 01_inspect_wards.py
│   ├── 02_extract_40_wards.py
│   ├── 03_process_dem.py
│   ├── 04_process_drainage.py
│   ├── 05_process_vulnerability.py
│   └── 06_compute_risk_index.py
│
├── .gitignore
└── README.md
```

**Note:** This structure documents the intended organization of the project. Individual output files are generated when the corresponding processing scripts run successfully.

---

## 3. Data Processing Pipeline

The pipeline consists of six modular stages executed sequentially.

| Stage | Script | Purpose |
|---|---|---|
| 1 | `01_inspect_wards.py` | Inspects the BBMP ward boundary KML file and identifies relevant attribute fields. |
| 2 | `02_extract_40_wards.py` | Selects the 40 study wards, standardizes coordinate references to EPSG:4326, and generates the study boundary GeoJSON. |
| 3 | `03_process_dem.py` | Processes ISRO Bhuvan CartoDEM elevation tiles and calculates zonal elevation statistics for each ward. |
| 4 | `04_process_drainage.py` | Processes OpenStreetMap waterways, calculates total drainage length, and derives drainage density for each ward. |
| 5 | `05_process_vulnerability.py` | Integrates demographic and informal settlement indicators to estimate socioeconomic vulnerability. |
| 6 | `06_compute_risk_index.py` | Normalizes indicators, computes composite risk scores, assigns risk categories, and generates consolidated outputs. |

### 3.1 Terrain Analysis

Elevation data from ISRO Bhuvan CartoDEM is used to derive terrain-related indicators.

Planned metrics include:

- Mean elevation per ward
- Minimum elevation per ward
- Maximum elevation per ward

Lower elevations are treated as a potential indicator of greater flood susceptibility.

### 3.2 Drainage Analysis

OpenStreetMap waterway data is used to estimate drainage availability across the study wards.

The analysis calculates:

- Total mapped drainage length in kilometres
- Drainage density in kilometres per square kilometre

Drainage density is used as a proxy indicator and does not, by itself, measure the actual capacity or condition of stormwater drains.

### 3.3 Vulnerability Analysis

Socioeconomic indicators are used to estimate the exposure of populations to potential flooding.

The planned indicators include:

- Population density
- Informal settlement counts

The consistency and spatial alignment of the underlying census and municipal datasets are important for reliable ward-level comparisons.

### 3.4 Composite Risk Assessment

The final stage applies Min-Max Scaling to the selected indicators and calculates composite hazard, vulnerability, and flood risk scores.

The resulting scores are used to classify wards into the following preliminary categories:

- Low
- Moderate
- High
- Critical

The final classification depends on the scoring and threshold rules implemented in the risk calculation script.

---

## 4. Technology Stack

- **Programming Language:** Python 3.10+
- **Geospatial Processing:** GeoPandas, Fiona, Shapely
- **Raster Processing:** Rasterio, Rasterstats
- **Data Analysis:** Pandas
- **Geospatial Data Sources:** ISRO Bhuvan CartoDEM, OpenStreetMap waterways
- **Planned Backend:** FastAPI
- **Planned Frontend:** React and Leaflet

---

## 5. Setup and Installation

### Prerequisites

- Python 3.10 or later
- Git
- Access to the required source datasets
- A terminal or command prompt

### Step 1: Clone the Repository

Replace `YOUR_USERNAME` and `REPO_NAME` with the actual GitHub username and repository name.

```bash
git clone https://github.com/YOUR_USERNAME/REPO_NAME.git
cd REPO_NAME
```

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment.

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
python -m pip install --upgrade pip
pip install geopandas fiona shapely rasterio rasterstats pandas
```

If the project uses additional libraries, install those dependencies as well.

---

## 6. Running the Data Pipeline

Run the scripts in the following order from the project root directory:

```bash
python scripts/01_inspect_wards.py
python scripts/02_extract_40_wards.py
python scripts/03_process_dem.py
python scripts/04_process_drainage.py
python scripts/05_process_vulnerability.py
python scripts/06_compute_risk_index.py
```

Each stage may depend on files produced by earlier stages. Ensure that the required input datasets are available in the expected locations before execution.

**Important:** The commands above describe the intended execution sequence. Successful completion and the generation of each output should be verified locally.

---

## 7. Expected Outputs

The following table describes the intended output files of the pipeline.

| Output File | Description |
|---|---|
| `data/processed/wards_40_clipped.geojson` | Standardized boundaries for the 40 selected study wards. |
| `data/processed/hazard_terrain_metrics.csv` | Mean, minimum, and maximum elevation metrics per ward. |
| `data/processed/hazard_drainage_metrics.csv` | Total mapped drainage length and drainage density per ward. |
| `data/processed/vulnerability_metrics.csv` | Population and informal settlement indicators per ward. |
| `data/processed/final_flood_risk_40_wards.csv` | Tabular dataset containing normalized indicators, composite scores, and risk categories. |
| `data/processed/final_flood_risk_40_wards.geojson` | Ward polygon dataset enriched with the final flood risk attributes. |

These files are generated by the processing scripts and should not be assumed to exist until the relevant stages have completed successfully.

---

## 8. Data Sources

The assessment is designed to use the following data sources:

- **BBMP:** Ward boundary data for identifying the study area.
- **ISRO Bhuvan:** CartoDEM elevation data for terrain analysis.
- **OpenStreetMap:** Waterway data for estimating mapped drainage density.
- **Census and municipal records:** Population and informal settlement indicators for vulnerability analysis.

The exact dataset versions, download links, reference years, and licensing information should be documented as the source files are finalized.

---

## 9. Current Status

The project is structured around a modular geospatial processing workflow for 40 selected wards in Bengaluru.

The processing scripts cover ward selection, terrain analysis, drainage analysis, vulnerability assessment, and composite risk calculation.

The completion status of individual stages and the availability of their outputs should be verified against the actual repository and execution results.

### Planned Next Steps

1. **Validate the data pipeline:** Confirm that all scripts execute successfully and generate the expected outputs.
2. **Validate the risk model:** Review indicator normalization, weighting assumptions, classification thresholds, and available flood-event records.
3. **Develop an API layer:** Build a FastAPI backend to expose processed ward metrics through REST endpoints.
4. **Build an interactive dashboard:** Develop a React and Leaflet interface to visualize ward-level risk categories and associated indicators.
5. **Improve documentation:** Record dataset sources, processing assumptions, limitations, and reproducibility instructions.

---

## 10. Limitations

- The assessment is a prototype and should not be treated as an official flood forecast or emergency warning system.
- Drainage density does not directly measure drainage capacity, blockages, or infrastructure condition.
- Population and informal settlement datasets may differ in reference year, coverage, and spatial accuracy.
- Composite risk scores depend on the indicators, normalization methods, weights, and classification thresholds selected.
- The model requires further validation against observed flood events before its results can support operational decisions.

---

