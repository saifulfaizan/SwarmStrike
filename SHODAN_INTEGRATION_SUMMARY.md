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

#### Pengujian NYATA dengan API Shodan

Gunakan `shodan_real_testing.py` untuk pengujian nyata dengan API Shodan:

```bash
# Pengujian lengkap dengan query Shodan
python shodan_real_testing.py --query "nginx country:ID" --limit 3

# Pengujian terhadap target IP spesifik
python shodan_real_testing.py --target "93.184.216.34"

# Pengujian untuk mencari target dengan CVE tertentu
python shodan_real_testing.py --cve "CVE-2023-23397" --limit 2

# Pengujian dengan intensitas tinggi dan mode stealth
python shodan_real_testing.py --query "nginx country:ID" --intensity 8 --stealth

# Menjalankan hanya fase tertentu (1-6)
python shodan_real_testing.py --target "93.184.216.34" --only-phase 1

# Menyimpan hasil dalam file JSON
python shodan_real_testing.py --query "webcam country:US" --output "results.json"
```

#### Pengujian Simulasi (Legacy)

Untuk tujuan demonstrasi, Anda masih bisa menggunakan skrip lama:

```bash
# Pengujian simulasi dasar
python shodan_pentest.py --query "nginx country:ID" --limit 5

# Pengujian simulasi dengan target spesifik
python shodan_pentest.py --target "93.184.216.34"

# Pengujian simulasi dengan fase aktif
python shodan_pentest_enhanced.py --target "93.184.216.34" --test-all-phases
```
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

Tool pengujian nyata (`shodan_real_testing.py`) dirancang khusus untuk pengujian nyata dengan API Shodan, dengan fitur:

1. **Mode API (Live)**
   - HANYA menggunakan API key Shodan untuk data real-time
   - Memerlukan koneksi internet dan API key yang valid
   - Menampilkan peringatan keamanan dan meminta konfirmasi sebelum pengujian
   - Mendukung parameter keamanan seperti mode stealth dan kontrol intensitas

2. **Verifikasi API Key**
   - Memeriksa keberadaan API key valid di secure_config.json
   - Menggunakan variabel lingkungan SHODAN_API_KEY sebagai fallback
   - Memberikan pesan kesalahan yang jelas jika API key tidak ditemukan

3. **Fitur Keamanan**
   - Konfirmasi sebelum menjalankan pengujian
   - Pembatasan jumlah target secara default
   - Peringatan untuk memastikan izin pengujian legal

4. **Pengujian Bertahap**
   - Pilihan untuk menjalankan seluruh fase pengujian
   - Opsi untuk fokus pada fase spesifik sesuai kebutuhan
   - Output terperinci tentang progres dan hasil pengujian

## Fase Pengujian

Modul pengujian nyata (`shodan_real_testing.py`) melakukan pengujian aktual untuk 6 fase penetration testing. Anda dapat menjalankan semua fase atau fokus pada fase tertentu dengan parameter `--only-phase`.

### Fase 1: Reconnaissance
- Melakukan scanning port secara aktif (21, 22, 23, 25, 53, 80, 443, dll)
- Mengidentifikasi layanan yang berjalan pada setiap port
- Mengumpulkan informasi dari web server dan header HTTP
- Contoh: `python shodan_real_testing.py --query "nginx country:ID" --only-phase 1`

### Fase 2: Vulnerability Analysis
- Menguji kerentanan umum seperti:
  - OpenSSH Username Enumeration
  - Log4j Remote Code Execution
  - Default Credentials
  - Directory Traversal
  - TLS/SSL Weak Cipher Suites
- Menganalisis dan memberi skor CVSS untuk setiap kerentanan
- Contoh: `python shodan_real_testing.py --target "93.184.216.34" --only-phase 2`

### Fase 3: Exploit Development
- Mengembangkan exploit untuk kerentanan yang ditemukan
- Menghasilkan payload yang sesuai dengan target (reverse_shell, bind_shell, dll)
- Menerapkan teknik evasion sesuai dengan tingkat intensitas
- Contoh: `python shodan_real_testing.py --cve "CVE-2023-23397" --only-phase 3`

### Fase 4: Exploitation
- Menjalankan eksploitasi pada target yang rentan
- Mencoba multiple exploits jika yang pertama gagal
- Melaporkan hasil exploit (success/failure) dengan detail akses
- Contoh: `python shodan_real_testing.py --target "93.184.216.34" --only-phase 4 --stealth`

### Fase 5: Post-Exploitation
- Melakukan privilege escalation jika memungkinkan
- Mengumpulkan kredensial dari sistem target
- Melakukan internal reconnaissance untuk menemukan host lain
- Menemukan file sensitif
- Menginstal backdoor/persistence jika tingkat intensitas tinggi
- Contoh: `python shodan_real_testing.py --target "93.184.216.34" --only-phase 5 --intensity 7`

### Fase 6: Data Exfiltration
- Mengekstrak data sensitif yang ditemukan
- Mengenkripsi data dengan algoritma yang kuat
- Menggunakan metode exfiltrasi yang berbeda sesuai dengan mode stealth
- Melaporkan statistik exfiltrasi data
- Contoh: `python shodan_real_testing.py --target "93.184.216.34" --only-phase 6 --output "exfil_results.json"`

## Parameter Pengujian

Tool pengujian nyata Shodan mendukung berbagai parameter untuk mengontrol perilaku dan intensitas pengujian:

### Parameter Target
- `--query`: Query pencarian Shodan (contoh: "apache country:US")
- `--target`: IP spesifik untuk ditargetkan
- `--cve`: Mencari target yang rentan terhadap CVE tertentu
- `--limit`: Jumlah maksimum target (default: 3)

### Parameter Pengujian
- `--intensity`: Intensitas pengujian dari 1 (minimal) hingga 10 (agresif)
- `--stealth`: Aktifkan mode stealth untuk meminimalkan deteksi
- `--only-phase`: Jalankan hanya fase pengujian tertentu (1-6)
- `--output`: File keluaran untuk hasil detail (format JSON)

## Catatan Keamanan

- Gunakan hanya untuk tujuan legal dan etis
- Pastikan Anda memiliki izin untuk menguji sistem target
- Ikuti regulasi dan hukum setempat tentang penetration testing
- Gunakan mode stealth untuk mengurangi dampak pada sistem target