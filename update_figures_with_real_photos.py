import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
import numpy as np

IMG_DIR = r"c:\Users\Nor Anisa\Downloads\LOMBA SI\B-OUTDOOR\img"

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

def update_fig_4_4():
    fig, ax = plt.subplots(figsize=(9.2, 5.2), dpi=300)
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
               ("Klaster Tanah Laut (6)", "#334155"), ("Klaster Meratus (4)", "#334155")]
    for i, (f_name, bg) in enumerate(filters):
        y = 76 - i * 7
        ax.add_patch(FancyBboxPatch((5, y - 2.5), 24, 5.2, boxstyle="round,pad=0.3,rounding_size=0.8",
                                    facecolor=bg, edgecolor="#0284c7" if bg != "#334155" else "#475569", linewidth=0.8))
        ax.text(17, y, f_name, ha='center', va='center', color='white', fontsize=6.8, weight='bold')

    # Card Bukit Contoh di Sidebar DENGAN FOTO ASLI MATANG KALADAN
    card_y = 17
    ax.add_patch(FancyBboxPatch((5, card_y), 24, 30, boxstyle="round,pad=0.5,rounding_size=1",
                                facecolor="#0f172a", edgecolor="#10b981", linewidth=1.2))
    
    # Embed real Matang Kaladan photo thumbnail
    img_mk = Image.open(os.path.join(IMG_DIR, "bukit-matang-kaladan.jpg"))
    img_mk.thumbnail((260, 150))
    im_box_mk = OffsetImage(img_mk, zoom=0.28)
    ab_mk = AnnotationBbox(im_box_mk, (17, card_y + 20), frameon=True, pad=0.1,
                           bboxprops=dict(edgecolor='#10b981', linewidth=0.8))
    ax.add_artist(ab_mk)

    ax.text(17, card_y + 10, "Bukit Matang Kaladan", ha='center', va='center', color='#10b981', fontsize=7.8, weight='bold')
    ax.text(17, card_y + 6, "400 mdpl | Banjar | Pemula", ha='center', va='center', color='#94a3b8', fontsize=6.5)
    ax.text(17, card_y + 2.5, "±68 km dari Banjarmasin", ha='center', va='center', color='#cbd5e1', fontsize=6.5)

    # Leave No Trace Ethics Widget
    ax.add_patch(FancyBboxPatch((5, 5.5), 24, 9, boxstyle="round,pad=0.4,rounding_size=0.8",
                                facecolor="#064e3b", edgecolor="#059669", linewidth=0.8))
    ax.text(17, 10, "Kalkulator Leave No Trace\n(7 Prinsip Konservasi Alam Bebas)",
            ha='center', va='center', color='#6ee7b7', fontsize=6.5, weight='bold', multialignment='center')

    # Center/Right Area: Leaflet Map Interface
    ax.add_patch(FancyBboxPatch((33, 4), 64, 84, boxstyle="round,pad=0.8,rounding_size=1.2",
                                facecolor="#022c22", edgecolor="#059669", linewidth=1.2))
    
    # Map title overlay
    ax.text(65, 84, "PETA INTERAKTIF MULTI-LAYER SPASIAL LEAFLET.JS",
            ha='center', va='center', color='#6ee7b7', fontsize=9, fontweight='bold')
    
    # Simulated map grid lines & river paths
    ax.plot([40, 52, 65, 75, 88], [25, 42, 48, 68, 78], color='#0284c7', linewidth=4, alpha=0.7)
    ax.text(50, 38, "Sungai Martapura", color='#38bdf8', fontsize=7, style='italic', rotation=30)
    
    # Map Pins
    # Banjarmasin Gateway
    ax.scatter(43, 28, color='#ef4444', s=200, marker='*', zorder=5)
    ax.text(43, 22, "Gateway Banjarmasin", color='#fca5a5', fontsize=7.5, weight='bold', ha='center')

    # Hills Markers
    h_markers = [(65, 48, "M. Kaladan"), (72, 52, "B. Batas"), (58, 18, "B. Telang"),
                 (80, 72, "Halau-Halau"), (74, 65, "B. Langara")]
    for mx, my, mname in h_markers:
        ax.scatter(mx, my, color='#10b981', s=120, marker='^', edgecolors='white', linewidth=1, zorder=5)
        ax.text(mx, my + 3.8, mname, color='#a7f3d0', fontsize=6.8, ha='center', weight='bold')

    # River Patrol Markers
    r_markers = [(41, 31), (46, 36), (50, 40), (56, 45)]
    for rx, ry in r_markers:
        ax.scatter(rx, ry, color='#38bdf8', s=70, marker='o', edgecolors='white', linewidth=1, zorder=5)

    # Interactive Popup Mockup with Real Photo of Bukit Batas
    popup_x, popup_y = 54, 46
    ax.add_patch(FancyBboxPatch((popup_x, popup_y), 41, 30, boxstyle="round,pad=0.6,rounding_size=1",
                                facecolor="#ffffff", edgecolor="#0284c7", linewidth=1.5))
    
    # Embed real Bukit Batas thumbnail in popup
    img_bb = Image.open(os.path.join(IMG_DIR, "bukit-batas.jpg"))
    img_bb.thumbnail((240, 140))
    im_box_bb = OffsetImage(img_bb, zoom=0.28)
    ab_bb = AnnotationBbox(im_box_bb, (popup_x + 10, popup_y + 15), frameon=True, pad=0.1,
                           bboxprops=dict(edgecolor='#0284c7', linewidth=0.8))
    ax.add_artist(ab_bb)

    # Popup text details
    ax.text(popup_x + 21, popup_y + 24, "Bukit Batas (550 mdpl)",
            ha='left', va='center', color='#0369a1', fontsize=7.5, fontweight='bold')
    ax.text(popup_x + 21, popup_y + 19, "Panorama Waduk Riam Kanan",
            ha='left', va='center', color='#0f172a', fontsize=6.8, style='italic')
    ax.text(popup_x + 21, popup_y + 14, "Jarak: 72 km | Klotok: 30 mnt",
            ha='left', va='center', color='#475569', fontsize=6.5)
    ax.text(popup_x + 21, popup_y + 9.5, "Status: Buka & Ramah Kemah",
            ha='left', va='center', color='#059669', fontsize=6.5, weight='bold')
    ax.text(popup_x + 21, popup_y + 5, "Verified: Mapala Banjarmasin",
            ha='left', va='center', color='#64748b', fontsize=6.0)

    # Map Legend at Bottom Right
    ax.add_patch(FancyBboxPatch((60, 6), 35, 11, boxstyle="round,pad=0.4,rounding_size=0.8",
                                facecolor="#0f172a", edgecolor="#334155", linewidth=0.8))
    ax.scatter([63], [13.5], color='#ef4444', s=50, marker='*')
    ax.text(66, 13.5, "Central Gateway", color='#cbd5e1', fontsize=6.5, va='center')
    ax.scatter([63], [9], color='#10b981', s=40, marker='^')
    ax.text(66, 9, "Destinasi Bukit Kalsel", color='#cbd5e1', fontsize=6.5, va='center')
    ax.scatter([80], [9], color='#38bdf8', s=35, marker='o')
    ax.text(83, 9, "Stasiun Patroli Sungai", color='#cbd5e1', fontsize=6.5, va='center')

    plt.tight_layout()
    out_path = os.path.join(IMG_DIR, "fig_4_4_geoportal_ui.png")
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Updated:", out_path)

def make_fig_hills_gallery():
    # 3x3 Photo Grid of 9 Hills
    fig, axes = plt.subplots(3, 3, figsize=(9.6, 9.6), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    hills_info = [
        ("bukit-matang-kaladan.jpg", "1. Bukit Matang Kaladan", "400 mdpl | Aranio, Banjar", "Gugusan Waduk Riam Kanan"),
        ("bukit-telang.jpg", "2. Bukit Telang", "350 mdpl | Tambang Ulang, Tala", "Savana Berundak Hijau"),
        ("bukit-batas.jpg", "3. Bukit Batas", "550 mdpl | Tiwingan Lama, Banjar", "Jalur Hutan & Panorama Danau"),
        ("bukit-birah.jpg", "4. Bukit Birah", "380 mdpl | Panyipatan, Tala", "Pemandangan Savana & Garis Laut"),
        ("bukit-langara.jpg", "5. Bukit Langara", "500 mdpl | Loksado, HSS", "Tebing Karst Purba Meratus"),
        ("puncak-halau-halau.jpg", "6. Puncak Halau-Halau", "1.901 mdpl | Batang Alai, HST", "Atap Tertinggi Hutan Tropis Kalsel"),
        ("bukit-mawar.jpg", "7. Bukit Mawar (Kiram)", "320 mdpl | Karang Intan, Banjar", "Ekowisata Pinus Ramah Keluarga"),
        ("bukit-lebak-naga.jpg", "8. Bukit Lebak Naga", "360 mdpl | Pelaihari, Tala", "Lekukan Punggung Naga Savana"),
        ("bukit-riam-bejanjang.jpg", "9. Bukit Riam Bejanjang", "410 mdpl | Batu Ampar, Tala", "Kombinasi Air Terjun & Bukit")
    ]

    for idx, (img_file, title, meta, desc) in enumerate(hills_info):
        r, c = idx // 3, idx % 3
        ax = axes[r, c]
        ax.set_facecolor('#f8fafc')
        
        img_p = os.path.join(IMG_DIR, img_file)
        if os.path.exists(img_p):
            with Image.open(img_p) as im:
                # Center-crop or fit to 4:3
                im_rgb = im.convert('RGB')
                w, h = im_rgb.size
                target_ratio = 4.0 / 3.0
                current_ratio = w / h
                if current_ratio > target_ratio:
                    new_w = int(h * target_ratio)
                    left = (w - new_w) // 2
                    im_crop = im_rgb.crop((left, 0, left + new_w, h))
                else:
                    new_h = int(w / target_ratio)
                    top = (h - new_h) // 2
                    im_crop = im_rgb.crop((0, top, w, top + new_h))
                
                ax.imshow(im_crop)
        
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color('#166534')
            spine.set_linewidth(1.5)

        # Labels below image
        ax.set_title(title, fontsize=8.5, fontweight='bold', color='#166534', pad=4)
        ax.set_xlabel(f"{meta}\n({desc})", fontsize=7.2, color='#334155', labelpad=3)

    plt.suptitle("DOKUMENTASI FOTOGRAFI 9 DESTINASI PERBUKITAN EKSOTIS KALIMANTAN SELATAN\n(Platform Geoportal B-OUTDOOR — Titik Tolak Central Gateway Kota Banjarmasin)",
                 fontsize=10.5, fontweight='bold', color='#14532d', y=0.99)
    plt.tight_layout()
    out_gallery = os.path.join(IMG_DIR, "fig_hills_gallery.png")
    fig.savefig(out_gallery, dpi=300, bbox_inches='tight')
    plt.close()
    print("Created Gallery:", out_gallery)

if __name__ == "__main__":
    update_fig_4_4()
    make_fig_hills_gallery()
