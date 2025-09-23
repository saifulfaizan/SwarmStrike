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

# Menjalankan test aktif untuk semua fase (1-6)
python shodan_pentest_enhanced.py --target "93.184.216.34" --test-all-phases

# Pengujian dengan intensitas tinggi dan mode stealth
python shodan_pentest_enhanced.py --query "nginx country:ID" --intensity 10 --stealth --test-all-phases

# Menjalankan demo cepat untuk semua fase
python run_shodan_demo.py --demo-type quick

# Menjalankan demo lengkap dengan multiple targets (simulasi)
python run_shodan_demo.py --demo-type full

# Menjalankan pengujian NYATA dengan API Shodan sebenarnya
python run_shodan_demo.py --demo-type real

# Menjalankan demo dengan mode stealth
python run_shodan_demo.py --demo-type stealth

# Menjalankan demo yang terfokus pada target spesifik
python run_shodan_demo.py --demo-type focused --target "192.168.1.100"
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

## Fase Pengujian

Modul enhanced (`shodan_pentest_enhanced.py`) melakukan pengujian aktual untuk 6 fase penetration testing:

### Fase 1: Reconnaissance
- Melakukan scanning port secara aktif (21, 22, 23, 25, 53, 80, 443, dll)
- Mengidentifikasi layanan yang berjalan pada setiap port
- Mengumpulkan informasi dari web server dan header HTTP

### Fase 2: Vulnerability Analysis
- Menguji kerentanan umum seperti:
  - OpenSSH Username Enumeration
  - Log4j Remote Code Execution
  - Default Credentials
  - Directory Traversal
  - TLS/SSL Weak Cipher Suites
- Menganalisis dan memberi skor CVSS untuk setiap kerentanan

### Fase 3: Exploit Development
- Mengembangkan exploit untuk kerentanan yang ditemukan
- Menghasilkan payload yang sesuai dengan target (reverse_shell, bind_shell, dll)
- Menerapkan teknik evasion sesuai dengan tingkat intensitas

### Fase 4: Exploitation
- Menjalankan eksploitasi pada target yang rentan
- Mencoba multiple exploits jika yang pertama gagal
- Melaporkan hasil exploit (success/failure) dengan detail akses

### Fase 5: Post-Exploitation
- Melakukan privilege escalation jika memungkinkan
- Mengumpulkan kredensial dari sistem target
- Melakukan internal reconnaissance untuk menemukan host lain
- Menemukan file sensitif
- Menginstal backdoor/persistence jika tingkat intensitas tinggi

### Fase 6: Data Exfiltration
- Mengekstrak data sensitif yang ditemukan
- Mengenkripsi data dengan algoritma yang kuat
- Menggunakan metode exfiltrasi yang berbeda sesuai dengan mode stealth
- Melaporkan statistik exfiltrasi data

## Catatan Keamanan

- Gunakan hanya untuk tujuan legal dan etis
- Pastikan Anda memiliki izin untuk menguji sistem target
- Ikuti regulasi dan hukum setempat tentang penetration testing
- Gunakan mode stealth untuk mengurangi dampak pada sistem target