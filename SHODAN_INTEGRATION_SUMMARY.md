# Dokumentasi Integrasi Shodan

## File yang Dibuat atau Dimodifikasi

1. **ai_modules/shodan_intelligence.py**
   - Modul utama untuk integrasi Shodan
   - Mendukung pencarian target, analisis kerentanan, pencarian exploit

2. **shodan_pentest.py**
   - Script untuk menjalankan penetration test dengan target dari Shodan
   - Mendukung pencarian berdasarkan query, CVE, atau IP spesifik

3. **secure_config.json**
   - Ditambahkan konfigurasi untuk API key Shodan

4. **requirements.txt**
   - Ditambahkan dependensi Shodan, ipaddress, dan tqdm

5. **ADVANCED_USAGE_GUIDE.md**
   - Ditambahkan bagian dokumentasi untuk modul Shodan
   - Ditambahkan contoh kode dan penggunaan

6. **SHODAN_MODULE_README.md**
   - Dokumentasi khusus untuk modul Shodan dalam bahasa Inggris
   - Mencakup petunjuk instalasi, konfigurasi, dan penggunaan

7. **PANDUAN_SHODAN.md**
   - Panduan penggunaan modul Shodan dalam bahasa Indonesia
   - Contoh query dan kode untuk pengguna Indonesia

## Cara Menggunakan

### 1. Konfigurasi API Key

Edit file `secure_config.json` dan tambahkan API key Shodan:

```json
{
  "api_keys": {
    "primary": "f5b95a2c7c51bc19640456b3cb12ce2466ef92a94ee240284c8e0d34919de539",
    "secondary": "2c0a5a66ce98efeb88229f9a9a18b76fd885499195cc617f52aa58c02f78e61a",
    "shodan": "YOUR_SHODAN_API_KEY_HERE"
  }
}
```

### 2. Instal Dependensi

```bash
pip install shodan ipaddress tqdm
```

### 3. Jalankan Penetration Test dengan Shodan

```bash
# Mencari target di Indonesia yang menggunakan Nginx
python shodan_pentest.py --query "nginx country:ID" --limit 5

# Mencari target berdasarkan kerentanan
python shodan_pentest.py --cve "CVE-2023-23397" --limit 5

# Menarget IP spesifik
python shodan_pentest.py --target "93.184.216.34"
```

### 4. Menggunakan API dalam Kode Python

```python
from ai_modules.shodan_intelligence import ShodanIntelligence

# Inisialisasi modul Shodan
shodan = ShodanIntelligence()

# Cari target menggunakan query
hasil = shodan.search_targets("nginx country:ID", limit=5)

# Tampilkan hasil
for target in hasil['targets']:
    print(f"IP: {target['ip']}")
    print(f"Organisasi: {target.get('org', 'Tidak diketahui')}")
    print(f"Port terbuka: {', '.join(map(str, target['ports']))}")
```

## Fitur Utama

1. **Pencarian Target**
   - Berdasarkan query Shodan
   - Filter berdasarkan negara, port, layanan

2. **Analisis Kerentanan**
   - Identifikasi sistem yang rentan terhadap CVE tertentu
   - Evaluasi risiko keamanan

3. **Pencarian Exploit**
   - Menemukan exploit yang tersedia untuk kerentanan
   - Mencocokkan dengan sistem target

4. **Laporan Intelijen**
   - Laporan komprehensif tentang target
   - Informasi geolokasi, organisasi, port terbuka

5. **Penetration Testing Otomatis**
   - Menggunakan target dari Shodan untuk penetration test
   - Simulasi serangan dengan berbagai intensitas

## Mode Operasi

Modul ini dapat beroperasi dalam dua mode:

1. **Mode API (Live)**
   - Menggunakan API key Shodan untuk data real-time
   - Memerlukan koneksi internet dan API key yang valid

2. **Mode Simulasi**
   - Berjalan tanpa API key
   - Menghasilkan data simulasi untuk demonstrasi dan testing

## Catatan Keamanan

- Gunakan hanya untuk tujuan legal dan etis
- Pastikan Anda memiliki izin untuk menguji sistem target
- Ikuti regulasi dan hukum setempat tentang penetration testing
- Gunakan mode stealth untuk mengurangi dampak pada sistem target