import subprocess
import sys
import os

scripts = [
    ("STAGE 1: Inspect Ward Boundaries", "scripts/01_inspect_wards.py"),
    ("STAGE 2: Extract 40 Study Wards", "scripts/02_extract_40_wards.py"),
    ("STAGE 3: Process CartoDEM Elevation", "scripts/03_process_dem.py"),
    ("STAGE 4: Process Drainage Network", "scripts/04_process_drainage.py"),
    ("STAGE 5: Process Vulnerability (Census & Slums)", "scripts/05_process_vulnerability.py"),
    ("STAGE 6: Compute Composite Flood Risk Index", "scripts/06_compute_risk_index.py"),
    ("STAGE 7: Generate Diagnostic Visualizations", "scripts/07_generate_visualizations.py"),
    ("STAGE 8: Generate Comprehensive PDF Report", "scripts/08_generate_pdf_report.py"),
]

python_exe = sys.executable

print("\n" + "="*70)
print("  BENGALURU URBAN FLOOD RISK MODEL — MASTER EXECUTION PIPELINE")
print("="*70 + "\n")

for title, script_path in scripts:
    print("\n" + "-"*70)
    print(f"▶ {title}")
    print(f"  Command: python {script_path}")
    print("-"*70)
    
    result = subprocess.run([python_exe, script_path])
    if result.returncode != 0:
        print(f"\n❌ Error running {script_path}. Halting pipeline.")
        sys.exit(result.returncode)

print("\n" + "="*70)
print("✅ ALL PIPELINE STAGES COMPLETED SUCCESSFULLY!")
print("   - Processed Data: data/processed/")
print("   - Generated Figures: reports/figures/")
print("   - Full PDF Report: reports/Bengaluru_Flood_Risk_Assessment_Report.pdf")
print("="*70 + "\n")
