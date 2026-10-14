# 🏔️ B-OUTDOOR: Geoportal Wisata Petualangan Perbukitan Kalimantan Selatan & Konservasi Sungai

[![GitHub Pages](https://img.shields.io/badge/Live_Demo-B--OUTDOOR-15803d?style=for-the-badge&logo=leaflet&logoColor=white)](https://nouranisa.github.io/B-OUTDOOR/)
[![License: MIT](https://img.shields.io/badge/License-MIT-0284c7?style=for-the-badge)](LICENSE)
[![LKTI Bappedalitbang 2026](https://img.shields.io/badge/LKTI_Banjarmasin-2026-d97706?style=for-the-badge)](https://nouranisa.github.io/B-OUTDOOR/)

> **"B-OUTDOOR: Rancang Bangun Geoportal Wisata Petualangan Perbukitan Kalimantan Selatan dan Konservasi Sungai Berbasis Komunitas Pecinta Alam di Kota Banjarmasin"**  
> *Karya Tulis Ilmiah — Lomba Karya Tulis Ilmiah (LKTI) Bappedalitbang Kota Banjarmasin Tahun 2026 | Kategori Umum*

---

## 🌟 Ringkasan Inovasi
**B-OUTDOOR** adalah platform sistem informasi geospasial (*WebGIS Geoportal*) terpadu yang memposisikan **Kota Banjarmasin sebagai Central Gateway (Pintu Gerbang & Pusat Hub)** ekowisata alam bebas Kalimantan Selatan. Platform ini mengintegrasikan direktori spasial jalur pendakian perbukitan eksotis di wilayah hulu (Kawasan Geopark Meratus, Kabupaten Banjar, Tanah Laut, dan Hulu Sungai) dengan aksi pemantauan kebersihan sungai lahan basah (*Citizen Science River Patrol*) di hilir Kota Banjarmasin.

---

## 🚀 Fitur Utama Sistem

1. **🗺️ Multi-Layer Geoportal Spasial (Leaflet.js):**
   * Visualisasi interaktif sebaran 18+ destinasi bukit di Kalimantan Selatan lengkap dengan elevasi (mdpl), foto jalur, estimasi jarak/waktu tempuh dari Titik Nol Banjarmasin, serta rute Google Maps sekali klik.
   * Lapisan spasial 36 titik *River Patrol* kebersihan sungai dan status kualitas air (pH, TDS) di anak-anak sungai Kota Banjarmasin.
   * Lapisan sebaran *Outdoor Hub & Basecamp Mapala* (persewaan alat gunung, dermaga klotok, dan posko siaga bencana di Banjarmasin).

2. **⛰️ Direktori & Ensiklopedia Bukit Kalsel:**
   * Informasi komprehensif klaster bukit: Kawasan Waduk Riam Kanan (Bukit Matang Kaladan, Bukit Batas), Savana Tanah Laut (Bukit Telang, Bukit Birah, Bukit Lebak Naga), Karst & Puncak Meratus (Bukit Langara, Puncak Halau-Halau 1.901 mdpl).
   * Filter dinamis berdasarkan kabupaten dan tingkat kesulitan pendakian (Pemula, Menengah, Ekspedisi).
   * Integrasi berbagi info rute ke WhatsApp komunitas petualang.

3. **🌊 Citizen Science & River Patrol Banjarmasin:**
   * Log pemantauan berkala sampah sungai (plastik sekali pakai, eceng gondok/ilung, residu domestik) dan mutu air fisik (TDS & pH) dibandingkan baku mutu Peraturan Pemerintah (PP) No. 22 Tahun 2021.
   * Grafik analitik visual menggunakan Chart.js.

4. **📢 Formulir Partisipasi Cepat (Citizen Reporting):**
   * Formulir pelaporan titik timbulan sampah sungai atau kerusakan jalur bukit dengan integrasi deteksi geolokasi satelit GPS otomatis dari peramban.

5. **🌱 Panduan Zero-Waste & Leave No Trace (LNT):**
   * Edukasi 7 etika penjelajah alam bebas dan nomor kontak darurat terpadu (BASARNAS Banjarmasin, BPBD, Posko Relawan Mapala).

6. **🏛️ Matriks Rekomendasi Aksi Lintas OPD Pemkot Banjarmasin (2026–2028):**
   * Peta jalan kolaboratif lintas sektor bagi Dinas Lingkungan Hidup (DLH), Disparbud, Bappedalitbang, dan BPBD Kota Banjarmasin.

7. **📊 Akses Terbuka Data Riset (Open Data Science):**
   * Ekspor instan seluruh data direktori spasial dalam format `.csv` dan `.geojson` untuk mendukung reprodusibilitas penelitian.

---

## 🛠️ Tumpukan Teknologi (Tech Stack)
* **Frontend:** HTML5 Semantic, Tailwind CSS (Modern Glassmorphism & Responsive UI)
* **Peta Spasial:** Leaflet.js v1.9.4 & OpenStreetMap CartoDB Tiles
* **Visualisasi Data:** Chart.js v4
* **Ikonografi:** Font Awesome 6.5 & Lucide Icons
* **Hosting & CI/CD:** GitHub Pages (Serverless & Zero Cost Deployment)

---

## 💻 Cara Menjalankan Secara Lokal
```bash
# Klon repositori ini
git clone https://github.com/NourAnisa/B-OUTDOOR.git

# Masuk ke direktori
cd B-OUTDOOR

# Buka file index.html di peramban web favorit Anda
# Atau jalankan lokal server python:
python -m http.server 8000
```
Buka `http://localhost:8000` pada peramban web Anda.

---

## 👥 Tim Peneliti & Pengembang
* **Ketua Peneliti / Mahasiswa:** Tim Komunitas Mahasiswa Pecinta Alam (Mapala)
* **Dosen Pembimbing:** Nor Anisa, M.Kom. (Program Studi Sistem Informasi, Fakultas Sains dan Teknologi, Universitas Sari Mulia, Banjarmasin)
* **Email:** `noranisa@unism.ac.id`

---
*Didedikasikan untuk Pelestarian Alam Bebas, Kejayaan Geopark Meratus, dan Kebersihan Sungai Kota Banjarmasin Menuju 500 Tahun Banjarmasin (1526–2026).*
