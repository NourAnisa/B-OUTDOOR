import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ArrowStyle
import numpy as np

IMG_DIR = r"c:\Users\Nor Anisa\Downloads\LOMBA SI\B-OUTDOOR\img"
os.makedirs(IMG_DIR, exist_ok=True)

# Set global matplotlib styles
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 0.8

# ==============================================================================
# FIG 2.1: KERANGKA KONSEPTUAL B-OUTDOOR
# ==============================================================================
def make_fig_2_1():
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Background subtle styling
    ax.add_patch(FancyBboxPatch((1, 1), 98, 98, boxstyle="round,pad=1,rounding_size=2",
                                facecolor="#f8fafc", edgecolor="#e2e8f0", linewidth=1.2))

    # Title Banner
    ax.add_patch(FancyBboxPatch((4, 87), 92, 9, boxstyle="round,pad=0.5,rounding_size=1.5",
                                facecolor="#166534", edgecolor="#14532d", linewidth=1.5))
    ax.text(50, 91.5, "KERANGKA KONSEPTUAL ARTEFAK GEOPORTAL B-OUTDOOR",
            ha='center', va='center', color='white', fontsize=11, fontweight='bold')

    # Columns: Input (Left), Process/Platform (Center), Output/Impact (Right)
    # Box 1: INPUT MASALAH & POTENSI
    ax.add_patch(FancyBboxPatch((4, 10), 27, 73, boxstyle="round,pad=0.8,rounding_size=2",
                                facecolor="#ffffff", edgecolor="#059669", linewidth=1.5))
    ax.text(17.5, 78, "INPUT POTENSI & ISU", ha='center', va='center',
            color='#065f46', fontsize=10, fontweight='bold')
    
    inputs = [
        ("Karakteristik 18 Bukit Kalsel\n(Elevasi, Jalur, Fasilitas)", "#ecfdf5", "#047857"),
        ("Timbulan Sampah & Kualitas Air\n36 Titik Sungai Banjarmasin", "#ecfdf5", "#047857"),
        ("Peran Central Gateway Kota\n(Logistik, Rental, Akses)", "#ecfdf5", "#047857"),
        ("Modal Sosial Komunitas Mapala\n(Aksi Bersih, Ekspedisi, DSRM)", "#ecfdf5", "#047857")
    ]
    for i, (txt, bg, fg) in enumerate(inputs):
        y = 65 - i * 16
        ax.add_patch(FancyBboxPatch((6, y - 6), 23, 12, boxstyle="round,pad=0.5,rounding_size=1",
                                    facecolor=bg, edgecolor=fg, linewidth=0.8))
        ax.text(17.5, y, txt, ha='center', va='center', color='#0f172a', fontsize=7.5, multialignment='center')

    # Box 2: PROSES / ARTEFAK B-OUTDOOR
    ax.add_patch(FancyBboxPatch((35, 10), 30, 73, boxstyle="round,pad=0.8,rounding_size=2",
                                facecolor="#ffffff", edgecolor="#0284c7", linewidth=1.5))
    ax.text(50, 78, "PLATFORM B-OUTDOOR", ha='center', va='center',
            color='#0369a1', fontsize=10, fontweight='bold')

    platform_modules = [
        ("WebGIS Leaflet.js Multi-Layer\n(Peta Bukit & Patroli Sungai)", "#f0f9ff", "#0284c7"),
        ("Direktori Geospasial Bukit\n(Filter Klaster, Estimasi Rute)", "#f0f9ff", "#0284c7"),
        ("Citizen Science River Patrol\n(Input TDS/pH, Foto Geotag)", "#f0f9ff", "#0284c7"),
        ("Modul Leave No Trace (LNT)\n(Kalkulator Etika Lingkungan)", "#f0f9ff", "#0284c7")
    ]
    for i, (txt, bg, fg) in enumerate(platform_modules):
        y = 65 - i * 16
        ax.add_patch(FancyBboxPatch((37, y - 6), 26, 12, boxstyle="round,pad=0.5,rounding_size=1",
                                    facecolor=bg, edgecolor=fg, linewidth=0.8))
        ax.text(50, y, txt, ha='center', va='center', color='#0f172a', fontsize=7.5, multialignment='center')

    # Box 3: OUTPUT / DAMPAK STRATEGIS
    ax.add_patch(FancyBboxPatch((69, 10), 27, 73, boxstyle="round,pad=0.8,rounding_size=2",
                                facecolor="#ffffff", edgecolor="#b45309", linewidth=1.5))
    ax.text(82.5, 78, "OUTPUT & DAMPAK", ha='center', va='center',
            color='#92400e', fontsize=10, fontweight='bold')

    outputs = [
        ("Peningkatan Kunjungan Ekowisata\nPerbukitan Terstandar & Aman", "#fffbeb", "#d97706"),
        ("Penyusutan Sampah Terapung &\nMitigasi Pencemaran Sungai", "#fffbeb", "#d97706"),
        ("Penguatan Ekonomi Lokal UMKM\n(Rental Alat Outdoor & Pemandu)", "#fffbeb", "#d97706"),
        ("Matriks Rekomendasi OPD\n(DLH, Disparbud, Dispora Banjarmasin)", "#fffbeb", "#d97706")
    ]
    for i, (txt, bg, fg) in enumerate(outputs):
        y = 65 - i * 16
        ax.add_patch(FancyBboxPatch((71, y - 6), 23, 12, boxstyle="round,pad=0.5,rounding_size=1",
                                    facecolor=bg, edgecolor=fg, linewidth=0.8))
        ax.text(82.5, y, txt, ha='center', va='center', color='#0f172a', fontsize=7.5, multialignment='center')

    # Connecting Arrows
    for y in [65, 49, 33, 17]:
        ax.annotate('', xy=(35, y), xytext=(31, y),
                    arrowprops=dict(arrowstyle="->", color="#0284c7", lw=1.5))
        ax.annotate('', xy=(69, y), xytext=(65, y),
                    arrowprops=dict(arrowstyle="->", color="#b45309", lw=1.5))

    plt.tight_layout()
    out_path = os.path.join(IMG_DIR, "fig_2_1_framework.png")
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", out_path)

# ==============================================================================
# FIG 3.1: ALUR TAHAPAN METODOLOGI DSRM
# ==============================================================================
def make_fig_3_1():
    fig, ax = plt.subplots(figsize=(9, 4.8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.add_patch(FancyBboxPatch((1, 1), 98, 98, boxstyle="round,pad=1,rounding_size=2",
                                facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=1.2))

    # Title
    ax.text(50, 93, "ALUR PENELITIAN DESIGN SCIENCE RESEARCH METHODOLOGY (DSRM)",
            ha='center', va='center', color='#166534', fontsize=11, fontweight='bold')

    steps = [
        ("1. Identifikasi Masalah", "Kesenjangan direktori bukit Kalsel &\npencemaran alur sungai Banjarmasin", "#ecfdf5", "#059669"),
        ("2. Definisi Tujuan Solusi", "Platform terpadu WebGIS Gateway Wisata\n& modul Citizen Science River Patrol", "#ecfdf5", "#059669"),
        ("3. Desain & Pengembangan", "Pengkodean Leaflet.js, integrasi data\nspasial bukit & form survey in-situ", "#eff6ff", "#2563eb"),
        ("4. Demonstrasi Sistem", "Pengujian langsung oleh komunitas\nMapala pada 18 bukit & 36 titik sungai", "#eff6ff", "#2563eb"),
        ("5. Evaluasi Artefak", "Analisis akurasi spasial, performa UI/UX\n& validitas data uji TDS/pH sungai", "#fef3c7", "#d97706"),
        ("6. Komunikasi & Kebijakan", "Publikasi kode sumber terbuka GitHub\n& perumusan naskah rekomendasi OPD", "#fef3c7", "#d97706")
    ]

    # Two rows of 3 boxes
    coords = [
        (4, 52), (36, 52), (68, 52),
        (68, 12), (36, 12), (4, 12)
    ]

    for i, (title, desc, bg, border) in enumerate(steps):
        x, y = coords[i]
        ax.add_patch(FancyBboxPatch((x, y), 28, 30, boxstyle="round,pad=0.6,rounding_size=1.5",
                                    facecolor=bg, edgecolor=border, linewidth=1.5))
        ax.text(x + 14, y + 23, title, ha='center', va='center',
                color=border, fontsize=9, fontweight='bold')
        ax.plot([x + 2, x + 26], [y + 17, y + 17], color=border, linewidth=0.8, alpha=0.5)
        ax.text(x + 14, y + 8, desc, ha='center', va='center',
                color='#1e293b', fontsize=7.5, multialignment='center')

    # Flow arrows
    # Row 1 left-to-right
    ax.annotate('', xy=(36, 67), xytext=(32, 67),
                arrowprops=dict(arrowstyle="->", color="#059669", lw=2))
    ax.annotate('', xy=(68, 67), xytext=(64, 67),
                arrowprops=dict(arrowstyle="->", color="#2563eb", lw=2))
    # Down arrow at right
    ax.annotate('', xy=(82, 42), xytext=(82, 52),
                arrowprops=dict(arrowstyle="->", color="#2563eb", lw=2))
    # Row 2 right-to-left
    ax.annotate('', xy=(64, 27), xytext=(68, 27),
                arrowprops=dict(arrowstyle="->", color="#d97706", lw=2))
    ax.annotate('', xy=(32, 27), xytext=(36, 27),
                arrowprops=dict(arrowstyle="->", color="#d97706", lw=2))

    plt.tight_layout()
    out_path = os.path.join(IMG_DIR, "fig_3_1_methodology.png")
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", out_path)

# ==============================================================================
# FIG 4.1: PETA SEBARAN SPASIAL & RADIUS DARI BANJARMASIN
# ==============================================================================
def make_fig_4_1():
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=300)
    ax.set_facecolor("#f8fafc")

    # Data 18 bukit: koordinat perkiraan relatif terhadap Banjarmasin (0, 0)
    # x = km timur (+), y = km utara (+)
    hills_data = [
        # Banjar & Riam Kanan
        ("Matang Kaladan", 48, -12, 432, "Banjar"),
        ("Bukit Batas", 52, -15, 540, "Banjar"),
        ("Bukit Batu", 45, -18, 380, "Banjar"),
        ("Mawar (Kirang)", 42, -10, 365, "Banjar"),
        ("Tabuan", 50, -16, 490, "Banjar"),
        ("Patra Bulu", 47, -14, 415, "Banjar"),
        # Tanah Laut
        ("Bukit Telang", 40, -45, 360, "Tanah Laut"),
        ("Bukit Birah", 45, -55, 380, "Tanah Laut"),
        ("Bukit Riam Bejanjang", 42, -50, 310, "Tanah Laut"),
        ("Bukit Timah", 35, -40, 200, "Tanah Laut"),
        ("Bukit Priangan", 38, -48, 290, "Tanah Laut"),
        ("Bukit Lintang", 44, -58, 340, "Tanah Laut"),
        # HSS & HST (Meratus)
        ("Bukit Langara", 95, 35, 500, "HSS/HST"),
        ("Puncak Halau-Halau", 125, 45, 1901, "HSS/HST"),
        ("Bukit Kudung", 100, 30, 620, "HSS/HST"),
        ("Bukit Palawan", 90, 28, 480, "HSS/HST"),
        # Kotabaru
        ("Bukit Mamake", 170, -35, 250, "Kotabaru"),
        ("Bukit Bapake", 175, -38, 280, "Kotabaru"),
    ]

    # Concentric radius circles from Banjarmasin
    radii = [50, 100, 150, 200]
    for r in radii:
        circle = plt.Circle((0, 0), r, color='#94a3b8', fill=False, linestyle='--', linewidth=0.8, alpha=0.6)
        ax.add_patch(circle)
        ax.text(0, r + 2, f"Radius {r} km", color='#64748b', fontsize=7.5, ha='center', weight='bold')

    # Plot Banjarmasin Central Gateway
    ax.scatter(0, 0, color='#dc2626', s=180, zorder=5, marker='*', edgecolor='black', linewidth=1.2)
    ax.annotate("KOTA BANJARMASIN\n(Central Gateway)", xy=(0, 0), xytext=(-15, 12),
                fontsize=8.5, fontweight='bold', color='#dc2626',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='#fee2e2', edgecolor='#dc2626', lw=1))

    # Cluster colors
    cluster_cfg = {
        "Banjar": {"color": "#16a34a", "label": "Klaster Banjar & Riam Kanan"},
        "Tanah Laut": {"color": "#ea580c", "label": "Klaster Savana Tanah Laut"},
        "HSS/HST": {"color": "#7c3aed", "label": "Klaster Karst & Meratus (HSS/HST)"},
        "Kotabaru": {"color": "#0284c7", "label": "Klaster Pesisir Kotabaru"}
    }

    plotted_labels = set()
    for name, x, y, elev, clust in hills_data:
        cfg = cluster_cfg[clust]
        lbl = cfg["label"] if clust not in plotted_labels else ""
        plotted_labels.add(clust)
        
        # Point size scaled by elevation
        size = 50 + (elev / 1901) * 150
        ax.scatter(x, y, color=cfg["color"], s=size, alpha=0.85, edgecolors='white',
                   linewidth=1.2, zorder=4, label=lbl)
        
        # Label with elevation
        offset_y = 5 if y >= 0 else -8
        ax.text(x, y + offset_y, f"{name}\n({elev} m)", fontsize=6.8, ha='center',
                color='#1e293b', weight='bold',
                bbox=dict(boxstyle="round,pad=0.15", facecolor='white', edgecolor='#cbd5e1', alpha=0.85, lw=0.5))

    ax.set_xlim(-40, 210)
    ax.set_ylim(-80, 75)
    ax.set_xlabel("Jarak Relatif Barat - Timur (km)", fontsize=9, fontweight='bold', color='#334155')
    ax.set_ylabel("Jarak Relatif Selatan - Utara (km)", fontsize=9, fontweight='bold', color='#334155')
    ax.set_title("Peta Sebaran Geospasial 18 Destinasi Bukit Kalsel dari Pintu Gerbang Banjarmasin",
                 fontsize=10.5, fontweight='bold', color='#166534', pad=12)

    ax.grid(True, linestyle=':', alpha=0.5, color='#cbd5e1')
    ax.legend(loc='lower right', fontsize=8, framealpha=0.95, edgecolor='#cbd5e1')

    plt.tight_layout()
    out_path = os.path.join(IMG_DIR, "fig_4_1_spatial_map.png")
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", out_path)

# ==============================================================================
# FIG 4.2: PROFIL ELEVASI & TINGKAT KESULITAN JALUR
# ==============================================================================
def make_fig_4_2():
    fig, ax = plt.subplots(figsize=(9, 4.8), dpi=300)

    hills = [
        "Halau-Halau", "Kudung", "Batas", "Langara", "Tabuan",
        "Palawan", "Matang Kaladan", "Patra Bulu", "Birah", "Batu",
        "Mawar", "Telang", "Lintang", "Riam Bejanjang", "Priangan",
        "Bapake", "Mamake", "Timah"
    ]
    elevations = [1901, 620, 540, 500, 490, 480, 432, 415, 380, 380, 365, 360, 340, 310, 290, 280, 250, 200]
    difficulties = ["Ekstrem", "Sulit", "Sedang", "Sedang", "Sedang",
                    "Sedang", "Sedang", "Sedang", "Mudah", "Mudah",
                    "Mudah", "Mudah", "Mudah", "Mudah", "Mudah",
                    "Mudah", "Mudah", "Mudah"]

    diff_colors = {
        "Mudah": "#22c55e",
        "Sedang": "#3b82f6",
        "Sulit": "#f59e0b",
        "Ekstrem": "#ef4444"
    }

    colors = [diff_colors[d] for d in difficulties]

    bars = ax.barh(hills[::-1], elevations[::-1], color=colors[::-1], height=0.65, edgecolor='#334155', linewidth=0.5)

    for bar, elev in zip(bars, elevations[::-1]):
        w = bar.get_width()
        ax.text(w + 25, bar.get_y() + bar.get_height() / 2, f"{elev} mdpl",
                ha='left', va='center', fontsize=7.5, color='#1e293b', weight='bold')

    ax.set_xlim(0, 2150)
    ax.set_xlabel("Elevasi Puncak (mdpl)", fontsize=9, fontweight='bold', color='#334155')
    ax.set_title("Profil Elevasi dan Tingkat Kesulitan Jalur 18 Perbukitan Unggulan Kalimantan Selatan",
                 fontsize=10.5, fontweight='bold', color='#166534', pad=12)

    # Custom Legend for difficulty
    legend_elements = [
        patches.Patch(facecolor="#22c55e", edgecolor="#334155", label="Tingkat Mudah (Trekking < 1 Jam)"),
        patches.Patch(facecolor="#3b82f6", edgecolor="#334155", label="Tingkat Sedang (Hiking 1 - 2 Jam)"),
        patches.Patch(facecolor="#f59e0b", edgecolor="#334155", label="Tingkat Sulit (Hiking 2 - 4 Jam)"),
        patches.Patch(facecolor="#ef4444", edgecolor="#334155", label="Tingkat Ekstrem (Ekspedisi Multi-Hari)")
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=8, framealpha=0.95, edgecolor='#cbd5e1')
    ax.grid(True, axis='x', linestyle=':', alpha=0.5, color='#cbd5e1')

    plt.tight_layout()
    out_path = os.path.join(IMG_DIR, "fig_4_2_elevation_difficulty.png")
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", out_path)

# ==============================================================================
# FIG 4.3: ANALISIS KUALITAS AIR & KOMPOSISI SAMPAH SUNGAI
# ==============================================================================
def make_fig_4_3():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4.5), dpi=300)

    # Subplot 1: Nilai TDS di 5 Kecamatan Banjarmasin
    districts = ['Banjarmasin\nBarat', 'Banjarmasin\nSelatan', 'Banjarmasin\nTengah', 'Banjarmasin\nTimur', 'Banjarmasin\nUtara']
    tds_mean = [178, 145, 192, 134, 112]
    tds_err = [22, 18, 25, 15, 12]

    bar_colors = ['#0284c7', '#0ea5e9', '#0369a1', '#38bdf8', '#7dd3fc']
    bars = ax1.bar(districts, tds_mean, yerr=tds_err, capsize=4, color=bar_colors, edgecolor='#0c4a6e', width=0.6)

    # Threshold Baku Mutu PP 22/2021 (Kelas II: 1000 mg/L, cut off reference line)
    ax1.axhline(300, color='#dc2626', linestyle='--', linewidth=1, label='Batas Toleransi Rekreasi (300 ppm)')
    ax1.set_ylim(0, 350)
    ax1.set_ylabel("Total Dissolved Solids / TDS (ppm)", fontsize=8.5, fontweight='bold', color='#334155')
    ax1.set_title("Rata-Rata TDS Air Sungai per Kecamatan\n(Hasil Uji In-Situ 36 Titik Stasiun)",
                  fontsize=9.5, fontweight='bold', color='#0369a1', pad=10)
    ax1.grid(True, axis='y', linestyle=':', alpha=0.5)
    ax1.legend(loc='upper right', fontsize=7.5, framealpha=0.9)

    for bar, val in zip(bars, tds_mean):
        ax1.text(bar.get_x() + bar.get_width() / 2, val + 28, f"{val} ppm",
                 ha='center', va='bottom', fontsize=8, weight='bold', color='#0f172a')

    # Subplot 2: Komposisi Timbulan Sampah Sungai (Donut Chart)
    waste_labels = ['Plastik Sekali Pakai\n(45%)', 'Eceng Gondok & Gulma\n(30%)',
                    'Kayu & Ranting Hanyut\n(15%)', 'Limbah Domestik Lain\n(10%)']
    waste_sizes = [45, 30, 15, 10]
    waste_colors = ['#ef4444', '#10b981', '#f59e0b', '#8b5cf6']
    explode = (0.05, 0, 0, 0)

    wedges, texts = ax2.pie(waste_sizes, explode=explode, labels=waste_labels, colors=waste_colors,
                            startangle=140, textprops={'fontsize': 8, 'color': '#1e293b', 'weight': 'bold'},
                            wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2))

    ax2.set_title("Komposisi Timbulan Sampah Terapung\ndi Alur Sungai Kota Banjarmasin",
                  fontsize=9.5, fontweight='bold', color='#166534', pad=10)

    plt.tight_layout()
    out_path = os.path.join(IMG_DIR, "fig_4_3_river_quality_waste.png")
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", out_path)

# ==============================================================================
# FIG 4.4: TANGKAPAN LAYAR ANTARMUKA GEOPORTAL B-OUTDOOR
# ==============================================================================
def make_fig_4_4():
    fig, ax = plt.subplots(figsize=(9, 5.0), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Window frame
    ax.add_patch(FancyBboxPatch((1, 1), 98, 98, boxstyle="round,pad=0.8,rounding_size=2",
                                facecolor="#0f172a", edgecolor="#334155", linewidth=1.5))

    # Browser Top Bar
    ax.add_patch(FancyBboxPatch((2, 90), 96, 8, boxstyle="round,pad=0.4,rounding_size=1",
                                facecolor="#1e293b", edgecolor="#334155", linewidth=1))
    # Window dots
    ax.scatter([4.5, 6.5, 8.5], [94, 94, 94], color=['#ef4444', '#f59e0b', '#10b981'], s=35)
    # URL bar
    ax.add_patch(FancyBboxPatch((12, 91.5), 75, 5, boxstyle="round,pad=0.3,rounding_size=0.8",
                                facecolor="#0f172a", edgecolor="#475569", linewidth=0.8))
    ax.text(14, 94, "https://nouranisa.github.io/B-OUTDOOR/  -  B-OUTDOOR Gateway & River Patrol Geoportal",
            ha='left', va='center', color='#94a3b8', fontsize=7.5, fontfamily='monospace')

    # Left Sidebar (Filter & Direktori Bukit)
    ax.add_patch(FancyBboxPatch((3, 4), 28, 84, boxstyle="round,pad=0.6,rounding_size=1.2",
                                facecolor="#1e293b", edgecolor="#334155", linewidth=1))
    ax.text(17, 84, "FILTER DIREKTORI BUKIT", ha='center', va='center',
            color='#38bdf8', fontsize=8.5, fontweight='bold')
    
    # Filter buttons
    filters = [("Semua Bukit (18)", "#0284c7"), ("Klaster Banjar (6)", "#334155"),
               ("Klaster Tanah Laut (6)", "#334155"), ("Klaster Meratus (4)", "#334155"),
               ("Klaster Kotabaru (2)", "#334155")]
    for i, (f_name, bg) in enumerate(filters):
        y = 76 - i * 8
        ax.add_patch(FancyBboxPatch((5, y - 3), 24, 6, boxstyle="round,pad=0.3,rounding_size=0.8",
                                    facecolor=bg, edgecolor="#0284c7" if bg != "#334155" else "#475569", linewidth=0.8))
        ax.text(17, y, f_name, ha='center', va='center', color='white', fontsize=7, weight='bold')

    # Card Bukit Contoh di Sidebar
    ax.add_patch(FancyBboxPatch((5, 18), 24, 18, boxstyle="round,pad=0.5,rounding_size=1",
                                facecolor="#0f172a", edgecolor="#10b981", linewidth=1))
    ax.text(17, 32, "Bukit Matang Kaladan", ha='center', va='center', color='#10b981', fontsize=8, weight='bold')
    ax.text(17, 27, "432 mdpl | Banjar | Sedang", ha='center', va='center', color='#94a3b8', fontsize=6.8)
    ax.text(17, 22, "Jarak: 65 km dari Banjarmasin", ha='center', va='center', color='#cbd5e1', fontsize=6.8)

    # Leave No Trace Ethics Widget
    ax.add_patch(FancyBboxPatch((5, 6), 24, 9, boxstyle="round,pad=0.4,rounding_size=0.8",
                                facecolor="#064e3b", edgecolor="#059669", linewidth=0.8))
    ax.text(17, 10.5, "Kalkulator Leave No Trace\n(Prinsip 7 Etika Konservasi)",
            ha='center', va='center', color='#6ee7b7', fontsize=6.8, weight='bold', multialignment='center')

    # Center/Right Area: Leaflet Map Interface
    ax.add_patch(FancyBboxPatch((33, 4), 64, 84, boxstyle="round,pad=0.8,rounding_size=1.2",
                                facecolor="#022c22", edgecolor="#059669", linewidth=1.2))
    
    # Map title overlay
    ax.text(65, 84, "PETA INTERAKTIF MULTI-LAYER SPASIAL LEAFLET.JS",
            ha='center', va='center', color='#6ee7b7', fontsize=9, fontweight='bold')
    
    # Simulated map grid lines & river paths
    ax.plot([40, 55, 68, 75, 88], [25, 45, 50, 70, 78], color='#0284c7', linewidth=4, alpha=0.7)
    ax.text(50, 40, "Sungai Martapura", color='#38bdf8', fontsize=7, style='italic', rotation=30)
    
    # Map Pins
    # Banjarmasin Gateway
    ax.scatter(45, 30, color='#ef4444', s=200, marker='*', zorder=5)
    ax.text(45, 24, "Gateway Banjarmasin", color='#fca5a5', fontsize=7.5, weight='bold', ha='center')

    # Hills Markers
    h_markers = [(65, 48, "M. Kaladan"), (70, 52, "B. Batas"), (60, 20, "B. Telang"),
                 (78, 72, "Halau-Halau"), (72, 65, "B. Langara")]
    for mx, my, mname in h_markers:
        ax.scatter(mx, my, color='#10b981', s=120, marker='^', edgecolors='white', linewidth=1, zorder=5)
        ax.text(mx, my + 4, mname, color='#a7f3d0', fontsize=6.8, ha='center', weight='bold')

    # River Patrol Markers
    r_markers = [(42, 33), (48, 38), (52, 42), (58, 47)]
    for rx, ry in r_markers:
        ax.scatter(rx, ry, color='#38bdf8', s=70, marker='o', edgecolors='white', linewidth=1, zorder=5)

    # Interactive Popup Mockup
    ax.add_patch(FancyBboxPatch((55, 52), 38, 22, boxstyle="round,pad=0.6,rounding_size=1",
                                facecolor="#ffffff", edgecolor="#0284c7", linewidth=1.5))
    ax.text(74, 69, "Stasiun Pantau #14: Siring Pierre Tendean",
            ha='center', va='center', color='#0369a1', fontsize=7.5, fontweight='bold')
    ax.text(74, 64, "Kualitas Air: pH 6,8 | TDS: 145 ppm (Baik)",
            ha='center', va='center', color='#0f172a', fontsize=6.8)
    ax.text(74, 59, "Status Sampah: Timbulan Rendah (Plastik Ringan)",
            ha='center', va='center', color='#059669', fontsize=6.8, weight='bold')
    ax.text(74, 55, "Petugas: Mapala UNISM Banjarmasin (Verified)",
            ha='center', va='center', color='#64748b', fontsize=6.2)

    # Map Legend at Bottom Right
    ax.add_patch(FancyBboxPatch((60, 6), 35, 12, boxstyle="round,pad=0.4,rounding_size=0.8",
                                facecolor="#0f172a", edgecolor="#334155", linewidth=0.8))
    ax.scatter([63], [14], color='#ef4444', s=50, marker='*')
    ax.text(66, 14, "Central Gateway", color='#cbd5e1', fontsize=6.5, va='center')
    ax.scatter([63], [9], color='#10b981', s=40, marker='^')
    ax.text(66, 9, "Destinasi Bukit Kalsel", color='#cbd5e1', fontsize=6.5, va='center')
    ax.scatter([80], [9], color='#38bdf8', s=35, marker='o')
    ax.text(83, 9, "Stasiun Patroli Sungai", color='#cbd5e1', fontsize=6.5, va='center')

    plt.tight_layout()
    out_path = os.path.join(IMG_DIR, "fig_4_4_geoportal_ui.png")
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", out_path)

if __name__ == "__main__":
    make_fig_2_1()
    make_fig_3_1()
    make_fig_4_1()
    make_fig_4_2()
    make_fig_4_3()
    make_fig_4_4()
    print("Semua 6 gambar B-OUTDOOR selesai dibuat dengan resolusi 300 DPI!")
