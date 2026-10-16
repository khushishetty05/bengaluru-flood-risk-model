import os
import pandas as pd
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#666666"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(40, 805, "Bengaluru Urban Flood Risk Assessment (40 Study Wards) — Technical Report")
            self.setStrokeColor(colors.HexColor("#dddddd"))
            self.setLineWidth(0.5)
            self.line(40, 800, 555, 800)
            
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(555, 30, page_text)
        self.drawString(40, 30, "CONFIDENTIAL & PROPRIETARY — FOR TEAM INTERNAL REFERENCE")
        self.setStrokeColor(colors.HexColor("#dddddd"))
        self.setLineWidth(0.5)
        self.line(40, 42, 555, 42)
        self.restoreState()

def build_pdf():
    pdf_path = "reports/Bengaluru_Flood_Risk_Assessment_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#1a365d')
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#4a5568')
    )
    
    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#718096')
    )

    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#1a365d'),
        spaceAfter=8,
        spaceBefore=14,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#2b6cb0'),
        spaceAfter=6,
        spaceBefore=10,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#2d3748'),
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#2d3748'),
        leftIndent=15,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#2c5282')
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#4a5568'),
        alignment=1, # Center
        spaceAfter=10
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#2d3748')
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    story = []

    # -------------------------------------------------------------
    # COVER / HEADER
    # -------------------------------------------------------------
    story.append(Paragraph("Bengaluru Urban Flood Risk Assessment", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("A Multi-Criteria Geospatial & Demographic Risk Model across 40 Study Wards", subtitle_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Author/Team:</b> Flood Modeling & Spatial Analytics Group &nbsp;|&nbsp; <b>Date:</b> October 2026 &nbsp;|&nbsp; <b>Status:</b> Baseline Model Completed", meta_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#2b6cb0'), spaceAfter=14))

    # Executive Callout
    callout_data = [[
        Paragraph(
            "<b>EXECUTIVE SUMMARY:</b> This document provides a comprehensive technical overview of the "
            "end-to-end data extraction, spatial engineering, socioeconomic harmonization, and flood risk computation "
            "for 40 representative BBMP wards in Bengaluru. Using satellite terrain elevation (CartoDEM), OpenStreetMap "
            "drainage corridors, and BBMP 2011 Census/Slum datasets, we formulated a composite MCDA model "
            "(<i>Risk = Hazard × Vulnerability</i>) to identify hotspots vulnerable to severe urban flooding.",
            callout_style
        )
    ]]
    callout_table = Table(callout_data, colWidths=[515])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ebf8ff')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#bee3f8')),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 14))

    # Embed Executive Dashboard Figure
    p_dash = "reports/figures/06_flood_risk_summary_dashboard.png"
    if os.path.exists(p_dash):
        img_dash = Image(p_dash, width=515, height=360)
        story.append(img_dash)
        story.append(Paragraph("Figure 1: Executive 4-Panel Summary Dashboard (Risk Ranking, Hazard-Vulnerability Matrix, Elevation Inversion, Category Distribution)", caption_style))

    story.append(PageBreak())

    # -------------------------------------------------------------
    # SECTION 1: DATA SOURCES & EXTRACTION
    # -------------------------------------------------------------
    story.append(Paragraph("1. Data Sources & Ingestion Pipeline", h1_style))
    story.append(Paragraph(
        "The project integrates multi-spectral rasters, vector hydrologic networks, and census demographic data "
        "to establish a multi-criteria baseline. The raw data ingestion is structured as follows:",
        body_style
    ))

    data_summary = [
        [Paragraph("Domain", table_header), Paragraph("Data Source", table_header), Paragraph("Format / Location", table_header), Paragraph("Spatial / Attribute Extent", table_header)],
        [
            Paragraph("<b>Administrative Boundaries</b>", table_cell),
            Paragraph("BBMP Ward Boundary KML/Shapefile", table_cell),
            Paragraph("<code>data/raw/01_Ward_Boundaries/</code>", table_cell),
            Paragraph("198 BBMP wards filtered down to 40 representative study wards in north & central Bengaluru.", table_cell)
        ],
        [
            Paragraph("<b>Terrain Topography</b>", table_cell),
            Paragraph("ISRO Bhuvan CartoDEM (30m Resolution)", table_cell),
            Paragraph("GeoTIFF rasters (tiles <code>cdnd43r</code>, <code>cdnd43x</code>)", table_cell),
            Paragraph("High-accuracy elevation surface (750m – 895m range) providing bare-earth digital elevation.", table_cell)
        ],
        [
            Paragraph("<b>Drainage Network</b>", table_cell),
            Paragraph("OpenStreetMap Waterways Layer", table_cell),
            Paragraph("Shapefile (<code>gis_osm_waterways_free_1.shp</code>)", table_cell),
            Paragraph("Primary rajakaluve storm drains, secondary nalas, and natural streams across Bengaluru Urban.", table_cell)
        ],
        [
            Paragraph("<b>Demographics & Slums</b>", table_cell),
            Paragraph("BBMP 2011 Census & Urban Slums Registry", table_cell),
            Paragraph("CSVs in <code>data/raw/03_Vulnerability_Data/</code>", table_cell),
            Paragraph("Ward-level total populations, gender ratios, SC/ST counts, and municipal slum listings with basic amenities.", table_cell)
        ],
    ]
    t_data = Table(data_summary, colWidths=[100, 115, 130, 170])
    t_data.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a365d')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f7fafc')]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_data)
    story.append(Spacer(1, 14))

    # -------------------------------------------------------------
    # SECTION 2: DATA PROCESSING & BUG RESOLUTION
    # -------------------------------------------------------------
    story.append(Paragraph("2. Data Processing Workflow & Pipeline Fixes", h1_style))
    story.append(Paragraph(
        "Data preparation required five sequential processing stages to align spatial resolutions and attribute schemas:",
        body_style
    ))

    story.append(Paragraph("<b>Stage 1 & 2: Boundary Extraction (<code>01_inspect_wards.py</code>, <code>02_extract_40_wards.py</code>)</b>", h2_style))
    story.append(Paragraph("The municipal boundaries were reprojected to EPSG:4326. A subset of 40 wards spanning low-lying valleys, high-density commercial centers, and northern catchment corridors was extracted into <code>data/processed/wards_40_clipped.geojson</code>.", bullet_style))

    story.append(Paragraph("<b>Stage 3: DEM Mosaic & Zonal Statistics (<code>03_process_dem.py</code>)</b>", h2_style))
    story.append(Paragraph("CartoDEM tiles were merged using <code>rasterio.merge</code> into <code>bengaluru_dem_merged.tif</code>. Zonal statistics were computed across each ward polygon to extract minimum, mean, and maximum surface elevation in meters.", bullet_style))

    story.append(Paragraph("<b>Stage 4: Drainage Spatial Intersection (<code>04_process_drainage.py</code>)</b>", h2_style))
    story.append(Paragraph("OSM waterway vectors were spatially clipped against each ward boundary. Total stream length in kilometers was aggregated and divided by ward area (sq km) to derive <i>drainage density</i> (km/sq km).", bullet_style))

    story.append(Paragraph("<b>Stage 5: Vulnerability Integration & Crucial Data Fix (<code>05_process_vulnerability.py</code>)</b>", h2_style))
    
    vuln_box = [[
        Paragraph(
            "<b>IMPORTANT PIPELINE FIX IMPLEMENTED:</b><br/>"
            "During pipeline verification, we discovered that <code>05_process_vulnerability.py</code> previously searched for "
            "<code>'Bengaluru Census 2011.csv'</code> and <code>'Bengaluru Urban Slums.csv'</code>, whereas the actual raw files were named "
            "<code>'Bengaluru Ward-wise Census Data - 2011.csv'</code> and <code>'Bengaluru List of Slums with Amenities - 2011.csv'</code>.<br/>"
            "Because of this mismatch, the script had triggered fallback default values assigning <b>flat 35,000 population and 0 slums</b> to every ward, "
            "making vulnerability identically 0.5.<br/><br/>"
            "<b>Resolution:</b> We corrected the file paths, updated the attribute matching logic to specifically target <code>'Ward Name'</code> "
            "(instead of picking <code>'Ward Num'</code>), added alias resolution for BBMP spelling variants (e.g., <i>Atturu Layout</i> $\\rightarrow$ <i>Atturu</i>, "
            "<i>Peenya</i> $\\rightarrow$ <i>Peenya Industrial Area</i>, <i>Ulsoor</i> $\\rightarrow$ <i>Halsoor</i>), and mapped slums by ward pattern. "
            "The vulnerability metrics now accurately reflect authentic census and field settlement figures.",
            callout_style
        )
    ]]
    t_vuln = Table(vuln_box, colWidths=[515])
    t_vuln.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fffaf0')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#feebc8')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_vuln)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Stage 6: Multi-Criteria Composite Risk Calculation (<code>06_compute_risk_index.py</code>)</b>", h2_style))
    story.append(Paragraph(
        "All metrics were normalized to a [0.0, 1.0] scale using Min-Max Normalization. Elevation was inverted (1 - norm) "
        "such that lower-lying terrain receives higher hazard weighting.<br/>"
        "• <b>Hazard Score:</b> 0.6 × (Norm Inverted Elevation) + 0.4 × (Norm Drainage Density)<br/>"
        "• <b>Vulnerability Score:</b> 0.5 × (Norm Population) + 0.5 × (Norm Slum Count)<br/>"
        "• <b>Final Composite Flood Risk Index:</b> Hazard Score × Vulnerability Score<br/>"
        "• <b>Risk Categorization:</b> Critical (≥ 0.45), High (0.30 – 0.45), Moderate (0.15 – 0.30), Low (< 0.15).",
        body_style
    ))

    story.append(PageBreak())

    # -------------------------------------------------------------
    # SECTION 3: TABULAR RESULTS
    # -------------------------------------------------------------
    story.append(Paragraph("3. Observed Outputs & Top Risk Wards", h1_style))
    story.append(Paragraph(
        "Following the re-execution of the pipeline with authentic demographic numbers, the model produced the following "
        "quantitative risk index for the highest-risk study wards:",
        body_style
    ))

    # Load top wards from CSV
    csv_file = "data/processed/final_flood_risk_40_wards.csv"
    if os.path.exists(csv_file):
        df_risk = pd.read_csv(csv_file)
        top_wards = df_risk.sort_values(by="flood_risk_score", ascending=False).head(12)
        
        table_rows = [
            [
                Paragraph("Ward Name", table_header),
                Paragraph("Mean Elev (m)", table_header),
                Paragraph("Drain Density", table_header),
                Paragraph("Population", table_header),
                Paragraph("Slums", table_header),
                Paragraph("Hazard", table_header),
                Paragraph("Vuln", table_header),
                Paragraph("Risk Score", table_header),
                Paragraph("Category", table_header),
            ]
        ]
        
        for _, r in top_wards.iterrows():
            table_rows.append([
                Paragraph(f"<b>{r['ward_name']}</b>", table_cell),
                Paragraph(f"{r['elevation_mean_m']:.1f}", table_cell),
                Paragraph(f"{r['drainage_density_km_per_sqkm']:.2f}", table_cell),
                Paragraph(f"{int(r['population']):,}", table_cell),
                Paragraph(f"{int(r['slum_count'])}", table_cell),
                Paragraph(f"{r['hazard_score']:.3f}", table_cell),
                Paragraph(f"{r['vulnerability_score']:.3f}", table_cell),
                Paragraph(f"<b>{r['flood_risk_score']:.3f}</b>", table_cell),
                Paragraph(f"<font color='{'#c53030' if r['risk_category']=='High' else '#d69e2e' if r['risk_category']=='Moderate' else '#3182ce'}'><b>{r['risk_category']}</b></font>", table_cell),
            ])
            
        t_risk = Table(table_rows, colWidths=[105, 50, 50, 50, 35, 45, 45, 55, 50])
        t_risk.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a365d')),
            ('PADDING', (0,0), (-1,-1), 4),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f7fafc')]),
            ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ]))
        story.append(t_risk)
        story.append(Spacer(1, 12))

    # Analytical findings
    story.append(Paragraph("Key Analytical Observations:", h2_style))
    story.append(Paragraph("• <b>Shettihalli & Someshwara Ward:</b> Rank highest in composite flood risk (0.211 and 0.209) due to a combination of low-lying terrain elevations (~811m) and substantial informal settlement concentrations.", bullet_style))
    story.append(Paragraph("• <b>Hegganahalli:</b> Exhibits severe vulnerability driven by a dense resident population exceeding 47,000 and moderate drainage channel concentration.", bullet_style))
    story.append(Paragraph("• <b>Topographic Protection in Malleswaram:</b> Wards located on higher ridges (e.g. Aramane Nagara at 851.1m and Malleswaram at 850.8m) receive minimal physical hazard scores (< 0.05), positioning them firmly in the Low risk tier.", bullet_style))

    story.append(PageBreak())

    # -------------------------------------------------------------
    # SECTION 4: VISUAL GRAPH GALLERY
    # -------------------------------------------------------------
    story.append(Paragraph("4. Diagnostic Visualizations & Spatial Maps", h1_style))
    story.append(Paragraph(
        "Six automated analytical charts were generated using Matplotlib, Seaborn, and GeoPandas to illustrate "
        "the relationships between physical topography, drainage density, and computed flood risk:",
        body_style
    ))

    # Figure 2: Top 15 Wards
    p_top15 = "reports/figures/01_top_risk_wards.png"
    if os.path.exists(p_top15):
        img_top15 = Image(p_top15, width=490, height=270)
        story.append(img_top15)
        story.append(Paragraph("Figure 2: Top 15 Study Wards Ranked by Multi-Criteria Composite Flood Risk Score", caption_style))
        story.append(Spacer(1, 10))

    # Figure 3: Spatial Map
    p_map = "reports/figures/05_spatial_flood_risk_map.png"
    if os.path.exists(p_map):
        img_map = Image(p_map, width=420, height=380)
        story.append(img_map)
        story.append(Paragraph("Figure 3: Geospatial Choropleth Risk Distribution Across 40 Bengaluru Wards", caption_style))

    story.append(PageBreak())

    # Figure 4 & 5: Matrix and Elevation Trend
    p_mat = "reports/figures/02_hazard_vs_vulnerability_matrix.png"
    if os.path.exists(p_mat):
        img_mat = Image(p_mat, width=450, height=310)
        story.append(img_mat)
        story.append(Paragraph("Figure 4: Hazard vs. Vulnerability 4-Quadrant Matrix (Bubble size represents ward population)", caption_style))
        story.append(Spacer(1, 12))

    p_elev = "reports/figures/03_elevation_vs_hazard.png"
    if os.path.exists(p_elev):
        img_elev = Image(p_elev, width=450, height=280)
        story.append(img_elev)
        story.append(Paragraph("Figure 5: Empirical Regression Demonstrating Inversion of Elevation vs. Computed Flood Hazard", caption_style))

    story.append(PageBreak())

    # Figure 6: Drainage Density
    p_drain = "reports/figures/04_drainage_density_ranking.png"
    if os.path.exists(p_drain):
        img_drain = Image(p_drain, width=480, height=270)
        story.append(img_drain)
        story.append(Paragraph("Figure 6: Top 15 Wards by Natural & Stormwater Drainage Corridor Density (km/sq km)", caption_style))
        story.append(Spacer(1, 12))

    # -------------------------------------------------------------
    # SECTION 5: TEAM REPRODUCIBILITY GUIDE
    # -------------------------------------------------------------
    story.append(Paragraph("5. Execution Guide for Team Members", h1_style))
    story.append(Paragraph(
        "Team members can reproduce all results, recompute the risk scores, and regenerate all figures "
        "by executing the following workflow in terminal:",
        body_style
    ))

    code_block = [
        [Paragraph(
            "<b># 1. Activate Environment:</b><br/>"
            "<code>.\\.venv\\Scripts\\Activate.ps1</code> (Windows) or <code>source .venv/bin/activate</code> (Linux/Mac)<br/><br/>"
            "<b># 2. Run Demographic Processing & Risk Computation:</b><br/>"
            "<code>python scripts/05_process_vulnerability.py</code><br/>"
            "<code>python scripts/06_compute_risk_index.py</code><br/><br/>"
            "<b># 3. Generate Diagnostic Visualizations & Figures:</b><br/>"
            "<code>python scripts/07_generate_visualizations.py</code><br/><br/>"
            "<b># 4. Generate this Comprehensive PDF Report:</b><br/>"
            "<code>python scripts/08_generate_pdf_report.py</code>",
            callout_style
        )]
    ]
    t_code = Table(code_block, colWidths=[515])
    t_code.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f7fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e0')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_code)
    story.append(Spacer(1, 14))

    story.append(Paragraph("<b>Planned Next Steps:</b>", h2_style))
    story.append(Paragraph("1. <b>FastAPI Backend:</b> Expose <code>final_flood_risk_40_wards.geojson</code> via REST endpoints for real-time ward querying.", bullet_style))
    story.append(Paragraph("2. <b>React / Leaflet Interactive Dashboard:</b> Deploy an interactive web application allowing users to adjust MCDA weights dynamically.", bullet_style))
    story.append(Paragraph("3. <b>Empirical Rainfall Calibration:</b> Ingest IMD extreme precipitation event data to validate flood vulnerability against observed inundation points.", bullet_style))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"\nPDF Report successfully compiled at: {pdf_path}")

if __name__ == "__main__":
    build_pdf()
