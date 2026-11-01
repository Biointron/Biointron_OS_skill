<div align="center">

<p dir="ltr">
<a href="../../README.md" lang="en" dir="ltr">English</a> ·
<a href="README.zh-CN.md" lang="zh-CN" dir="ltr">简体中文</a> ·
<a href="README.zh-TW.md" lang="zh-TW" dir="ltr">繁體中文</a> ·
<a href="README.ja.md" lang="ja" dir="ltr">日本語</a> ·
<a href="README.ko.md" lang="ko" dir="ltr">한국어</a> ·
<a href="README.tr.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="README.ru.md" lang="ru" dir="ltr">Русский</a> ·
<a href="README.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="README.th.md" lang="th" dir="ltr">ไทย</a> ·
<a href="README.de.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="README.es.md" lang="es" dir="ltr">Español</a> ·
<a href="README.fr.md" lang="fr" dir="ltr">Français</a> ·
<a href="README.uk.md" lang="uk" dir="ltr">Українська</a> ·
<a href="README.pl.md" lang="pl" dir="ltr">Polski</a> ·
<a href="README.pt-BR.md" lang="pt-BR" dir="ltr">Português (Brasil)</a> ·
<a href="README.fa.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="README.ar.md" lang="ar" dir="rtl">العربية</a> ·
<strong lang="id" dir="ltr">Bahasa Indonesia</strong> ·
<a href="README.it.md" lang="it" dir="ltr">Italiano</a> ·
<a href="README.el.md" lang="el" dir="ltr">Ελληνικά</a> ·
<a href="README.ml.md" lang="ml" dir="ltr">മലയാളം</a> ·
<a href="README.ur-Latn.md" lang="ur-Latn" dir="ltr">Roman Urdu</a> ·
<a href="README.ro.md" lang="ro" dir="ltr">Română</a>
</p>

# Biointron OS

### Hubungkan agen AI Anda dengan layanan Biointron.

Dari permintaan pesanan hingga hasil laporan, hadirkan alur kerja Biointron dalam alat yang sudah Anda gunakan.<br />
MCP menyediakan koneksi. Skills memandu alur kerja. Kendali tetap di tangan Anda.

[![Katalog alat MCP](https://img.shields.io/badge/MCP-tool_catalog-087F8C?style=flat-square)](../../docs/tool-catalog.md)
[![Skills](https://img.shields.io/badge/Agent-Skills-234E70?style=flat-square)](../../skills/README.md)
[![Lisensi nonkomersial](https://img.shields.io/badge/License-Noncommercial-6B7280?style=flat-square)](../../LICENSE)
[![Beta Playground](https://img.shields.io/badge/Release-Beta_Playground-D7A345?style=flat-square)](#beta)

<br />

<!-- HERO: Keep the artwork path in sync across all language versions. -->
<img src="../../assets/biointron-os-hero.png" alt="Biointron OS" width="1000" />

<br />

**[Mulai](#get-started) · [Alat MCP](../../docs/tool-catalog.md) · [Skills](../../skills/README.md) · [API & contoh](../../docs/api.md) · [Platform daring](#online-platform) · [Tanya jawab](#faq)**

</div>

---

## Satu platform. Tiga cara terhubung.

Biointron OS adalah antarmuka layanan Biointron untuk agen AI, model, dan pengguna. Platform ini menyatukan akses layanan dan panduan alur kerja, dengan rencana pengembangan yang mencakup pesanan, pengajuan desain, progres, dan hasil.

| Untuk Agen | Untuk Model | Untuk Pengguna |
| :--- | :--- | :--- |
| Temukan dan panggil layanan melalui **MCP**. | Gunakan **data terstruktur** dan antarmuka yang terdokumentasi. | Akses alur kerja melalui **antarmuka interaktif**. |
| Lengkapi pemanggilan alat dengan Skills khusus tugas. | Konvensi data sedang diselaraskan selama Beta. | Pengalaman web disediakan terpisah dari repositori ini. |

Repositori ini merupakan tempat publik untuk Skills, panduan koneksi, katalog alat, dan contoh. Layanan bisnis Biointron berjalan secara terpisah.

<a id="get-started"></a>

## Mulai

### 1 · Hubungkan MCP

Dapatkan token akses layanan dan izin yang diperlukan dari kontak Biointron Anda. Pada klien MCP yang mendukung **Streamable HTTP** dan **autentikasi Bearer**, tambahkan:

| Pengaturan | Nilai |
| :--- | :--- |
| Nama | `BiointronOS_MCP` |
| Transport | Streamable HTTP |
| URL | `https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp` |
| Autentikasi | `Authorization: Bearer <MCP_ACCESS_TOKEN>` |

Pada klien yang mendukung format `mcpServers`, gabungkan konfigurasi ini dengan pengaturan yang sudah ada, lalu ganti placeholder dengan token Anda sendiri:

```json
{
  "mcpServers": {
    "BiointronOS_MCP": {
      "url": "https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp",
      "headers": {
        "Authorization": "Bearer <MCP_ACCESS_TOKEN>",
        "START_MCP_TIMEOUT_MS": "60000",
        "RUN_MCP_TIMEOUT_MS": "660000"
      }
    }
  }
}
```

Kedua header timeout merupakan bagian khusus dari konfigurasi referensi: 60000 milidetik = 60 detik, dan 660000 milidetik = 11 menit. Header ini hanya berpengaruh jika didukung oleh klien atau layanan; menambahkannya ke `headers` saja tidak menjamin perubahan waktu tunggu klien. Atur timeout sesuai dokumentasi klien yang Anda gunakan.

Lihat [panduan instalasi](../../docs/installation.md#mcp) untuk detail lebih lanjut.

### 2 · Tambahkan Skills

Pilih salah satu Skill yang disertakan dalam [katalog Skills](../../skills/README.md). Unduh seluruh foldernya, termasuk `references/` dan skrip yang disertakan, lalu letakkan di direktori Skill agen Anda. Lihat [instalasi Skill](../../docs/installation.md#skills) untuk Codex dan Claude Code.

Kedua paket kini tersedia di repositori ini: `skills/order_design/` untuk `order-design` dan `skills/auto_html_report/` untuk `auto_html_report`. Keduanya dapat diunduh; keberadaan paket tidak membuktikan bahwa seluruh alur bisnis telah divalidasi.

### 3 · Coba pengenalan hanya-baca

```text
Daftarkan alat MCP Biointron yang tersedia dalam sesi ini dan jelaskan fungsi masing-masing.
Beri tahu saya kemampuan yang sudah siap dan yang masih dalam tahap Beta.
Jangan membuat atau mengirim pesanan.
```

Penemuan alat merupakan pemeriksaan koneksi pertama. Keberhasilan suatu operasi bisnis memerlukan koneksi backend terkait yang telah divalidasi.

## Katalog alat MCP

| Alat | Tujuan | Dampak |
| :--- | :--- | :--- |
| `order_design_preflight` | Memeriksa kelayakan perusahaan dan pengujian yang tersedia. | Hanya baca |
| `start_order_design` | Mengirim XLSX yang diberikan dan menunggu konfirmasi penyimpanan desain. | Menulis data bisnis |
| `add_order_to_cart` | Menambahkan desain yang telah dikonfirmasi tersimpan ke keranjang. | Menulis data bisnis |
| `get_order_cart` | Membaca keranjang pesanan. | Hanya baca |
| `calculate_order_price` | Mendapatkan penawaran harga untuk pesanan yang dipilih. | Hanya baca |
| `submit_verified_order` | Memverifikasi harga dan mengirim pesanan yang dipilih. | Menulis data bisnis |
| `get_report_results` | Mengambil hasil laporan yang sudah ada dalam format JSON. | Hanya baca |

Ketujuh alat ini terdaftar dalam implementasi MCP saat ini. Kesiapan alur bisnis dari awal hingga akhir masih perlu diverifikasi. Lihat [parameter, status, dan batasan](../../docs/tool-catalog.md).

## Skills

| Skill | Tujuan | Status rilis |
| :--- | :--- | :--- |
| [Desain Pesanan · `order-design`](../../skills/order_design/SKILL.md) | Memandu pengajuan desain, penambahan ke keranjang, pemeriksaan penawaran harga, dan pengiriman pesanan yang telah diizinkan. | Disertakan; dapat diunduh |
| [Laporan Hasil · `auto_html_report`](../../skills/auto_html_report/SKILL.md) | Membuat laporan HTML mandiri dalam berbagai bahasa dari JSON hasil yang diberikan pengguna, dengan tabel ringkasan, grafik, dan gambar yang tersedia. | Disertakan; dapat diunduh |

MCP menyediakan operasi; Skills menjelaskan cara agen menggunakannya dalam suatu tugas. Menginstal Skill tidak memberikan akses layanan atau mendaftarkan MCP secara otomatis. [Jelajahi katalog →](../../skills/README.md)

Skill `auto_html_report` memerlukan JSON hasil yang sudah diberikan pengguna. Skill ini tidak mengambil data dari layanan; nomor pesanan saja tidak cukup.

<a id="beta"></a>

## Beta Playground

Biointron OS diperkenalkan sebagai Beta Playground. Beberapa koneksi mungkin masih belum tersedia. Laporkan hasil sebenarnya dari setiap langkah; respons HTTP yang berhasil atau nama alat yang terlihat tidak membuktikan bahwa operasi bisnis telah selesai.

Pembuatan dan pengiriman pesanan memerlukan izin pengguna. Jika operasi penulisan mengalami timeout, periksa status pesanan yang ada sebelum mencoba lagi. Untuk akses atau kemampuan yang belum tersedia, hubungi perwakilan Biointron yang memberikan akun Anda.

<a id="online-platform"></a>

## Platform Daring Biointron

Platform daring Biointron menghadirkan alur kerja proyek RushDATA di browser, dengan akses ke draf proyek, keranjang belanja, pesanan, dan asisten AI. Buka platform untuk menjelajahi layanan yang tersedia dan melihat informasi proyek.

[Kunjungi platform daring Biointron →](https://ai.biointron.com/#/landing)

<a href="https://ai.biointron.com/#/landing"><img src="../../assets/Biointron_Rushdata.png" alt="Antarmuka platform daring Biointron dengan akses ke proyek RushDATA" width="1000" /></a>

<a id="faq"></a>

## Tanya jawab

<details>
<summary><strong>Apakah saya memerlukan MCP dan Skills sekaligus?</strong></summary>

MCP menyediakan alat yang dapat dipanggil. Skills menambahkan petunjuk alur kerja dan mungkin memiliki dependensi sendiri. Ikuti persyaratan setiap Skill yang dirilis; mengunduh Skill saja tidak menghubungkan layanan.

</details>

<details>
<summary><strong>Apakah alat yang terdaftar berarti siap digunakan untuk operasi bisnis?</strong></summary>

Tidak. Penemuan hanya memastikan alat telah terdaftar. Konfigurasi backend, akses akun, dan operasi yang diminta juga harus divalidasi. Katalog mencatat perbedaan tersebut.

</details>

<details>
<summary><strong>Di mana server dan implementasi bisnisnya?</strong></summary>

Repositori ini mendistribusikan materi integrasi publik dan Skills. Layanan yang dihosting dan implementasi bisnis privat dipelihara secara terpisah.

</details>

## Dokumentasi

| Mulai di sini | Referensi |
| :--- | :--- |
| [Instal MCP & Skills](../../docs/installation.md) | [Katalog alat MCP](../../docs/tool-catalog.md) |
| [Katalog Skills](../../skills/README.md) | [API & contoh JSON](../../docs/api.md) |
| [Berkontribusi](../../CONTRIBUTING.md) | [Status lisensi](../../docs/license.md) |

Panduan terperinci tersedia dalam bahasa Mandarin dan Inggris.

## Lisensi

Dilisensikan berdasarkan [PolyForm Noncommercial 1.0.0](../../LICENSE). **Penggunaan komersial tidak diizinkan oleh lisensi ini.** Kode sumber repositori ini tersedia untuk penggunaan nonkomersial. Lihat [cakupan dan ketentuan](../../docs/license.md).

---

<div align="center">
<sub>Biointron OS · Untuk Agen. Untuk Model. Untuk Pengguna.</sub>
</div>

