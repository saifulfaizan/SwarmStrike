# Panduan Penggunaan Modul Shodan dalam Framework Keamanan Siber

## Pengenalan

Modul Shodan memberikan kemampuan untuk melakukan penetration test terhadap target yang ditemukan melalui Shodan - "mesin pencari untuk perangkat yang terhubung ke internet". Dengan modul ini, Anda dapat menemukan target eksternal nyata untuk pengujian keamanan.

## Persiapan Awal

1. **Instal Dependensi yang Diperlukan**:
   ```
   pip install shodan ipaddress tqdm
   ```

2. **Dapatkan API Key Shodan**:
   - Daftar akun di [Shodan.io](https://account.shodan.io/register)
   - Dapatkan API key dari halaman akun Anda
   - Tambahkan API key ke file `secure_config.json`:
   ```json
   {
     "api_keys": {
       "shodan": "API_KEY_ANDA_DISINI"
     }
   }
   ```

## Cara Penggunaan

### Mencari Target dengan Query

```bash
# Mencari target di Indonesia yang menggunakan Nginx
python shodan_pentest.py --query "nginx country:ID" --limit 5

# Mencari target di Malaysia yang menggunakan Apache
python shodan_pentest.py --query "apache country:MY" --limit 10

# Mencari target berdasarkan port terbuka
python shodan_pentest.py --query "port:22 country:ID" --limit 5
```

### Mencari Target dengan Kerentanan Tertentu

```bash
# Mencari target yang rentan terhadap CVE tertentu
python shodan_pentest.py --cve "CVE-2023-23397" --limit 5

# Mencari target yang rentan terhadap Log4j
python shodan_pentest.py --query "vuln:CVE-2021-44228" --limit 5
```

### Menarget IP Spesifik

```bash
# Lakukan penetration test terhadap IP spesifik
python shodan_pentest.py --target "93.184.216.34"
```

### Opsi Lanjutan

```bash
# Gunakan mode stealth untuk mengurangi kemungkinan deteksi
python shodan_pentest.py --query "apache country:ID" --stealth

# Atur intensitas serangan (1-10)
python shodan_pentest.py --query "apache country:ID" --intensity 10
```

## Contoh Kode Python

### Mencari Target

```python
from ai_modules.shodan_intelligence import ShodanIntelligence

# Inisialisasi modul Shodan
shodan = ShodanIntelligence()

# Cari target menggunakan query
hasil = shodan.search_targets("nginx country:ID", limit=5)

# Tampilkan hasil
print(f"Ditemukan {hasil['returned_results']} target")
for target in hasil['targets']:
    print(f"IP: {target['ip']}")
    print(f"Organisasi: {target.get('org', 'Tidak diketahui')}")
    print(f"Port terbuka: {', '.join(map(str, target['ports']))}")
    print(f"Negara: {target.get('country', 'Tidak diketahui')}")
```

### Mencari Sistem yang Rentan

```python
# Cari sistem yang rentan terhadap CVE tertentu
rentan = shodan.discover_vulnerable_targets("CVE-2023-23397", limit=5)

# Tampilkan hasil
print(f"Ditemukan {rentan['returned_results']} sistem yang rentan")
for target in rentan['targets']:
    print(f"Sistem rentan: {target['ip']} ({target.get('org', 'Tidak diketahui')})")
    print(f"Kerentanan: {', '.join(target.get('vulns', []))}")
```

### Laporan Intelijen Lengkap

```python
# Dapatkan laporan intelijen lengkap untuk target
laporan = shodan.get_shodan_intelligence_report("93.184.216.34")

# Tampilkan informasi laporan
print(f"Target: {laporan['target']}")
print(f"Organisasi: {laporan['host_info'].get('org', 'Tidak diketahui')}")
print(f"Negara: {laporan['host_info'].get('country', 'Tidak diketahui')}")
print(f"Port terbuka: {', '.join(map(str, laporan['host_info'].get('ports', [])))}")
```

## Tips Penggunaan

1. **Batasi Query**: Gunakan query yang spesifik untuk mendapatkan hasil yang lebih relevan

2. **Gunakan Filter Country**: Tambahkan filter negara (`country:ID` untuk Indonesia, `country:MY` untuk Malaysia) untuk menargetkan wilayah tertentu

3. **Filter Berdasarkan Layanan**:
   - `apache` untuk server Apache
   - `nginx` untuk server Nginx
   - `ftp` untuk server FTP
   - `ssh` untuk server SSH
   - `webcam` untuk webcam yang terhubung internet

4. **Filter Berdasarkan Port**:
   - `port:80` untuk HTTP
   - `port:443` untuk HTTPS
   - `port:22` untuk SSH
   - `port:21` untuk FTP

5. **Mode Stealth**: Selalu gunakan opsi `--stealth` saat melakukan pengujian untuk mengurangi kemungkinan deteksi

## Catatan Keamanan

- **Hanya gunakan untuk tujuan legal**: Pastikan Anda memiliki izin untuk menguji sistem yang Anda targetkan
- **Jangan menyerang sistem tanpa izin**: Penggunaan untuk menyerang sistem tanpa izin adalah ilegal
- **Perhatikan batasan geografis**: Beberapa negara memiliki aturan ketat tentang scanning dan penetration testing
- **Gunakan dengan tanggung jawab**: Alat ini dibuat untuk tujuan edukasi dan keamanan yang sah

## Memecahkan Masalah

- **API Key tidak ditemukan**: Pastikan API key telah ditambahkan dengan benar di `secure_config.json`
- **Rate limiting**: Shodan membatasi jumlah permintaan API. Upgrade ke akun berbayar untuk batas yang lebih tinggi
- **Hasil simulasi**: Jika tidak menggunakan API key, modul akan menghasilkan data simulasi yang tidak nyata

Untuk informasi lebih lanjut, lihat [dokumentasi lengkap](ADVANCED_USAGE_GUIDE.md#8-shodan-intelligence).