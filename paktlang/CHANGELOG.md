# Değişiklik Günlüğü

Tüm önemli değişiklikler bu dosyada belgelenmektedir.

Format: [Semantic Versioning](https://semver.org/)

---

## [1.1.0] - 2026-02-04

### Eklenenler
- `mappings/erp_mappings.json` - Logo, Netsis, Mikro, Wolvox ERP eşleştirmeleri
- `stok_hareket` tablosuna ERP uyumlu alanlar:
  - `belge_tipi_kod` (Netsis STHAR_FTIRSIP)
  - `hareket_turu_kod` (Netsis STHAR_HTUR)
  - `kaynak_belge_tipi`
  - `siparis_id`, `siparis_no`
  - `konsinye`, `mustahsil`
- `erp_types.json`'a yeni tipler:
  - `netsis_belge_tipi`
  - `netsis_hareket_turu`
  - `logo_trcode`
  - `logo_firma_kodu`
- `paktlang.meta.json`'a `mapping_layer` eklendi

### Değişenler
- `hareket_turu` enum genişletildi (17 → 27 değer)
- Validator Unicode karakter sorunu düzeltildi (Windows uyumu)

---

## [1.0.0] - 2026-02-03

### Eklenenler
- İlk sürüm
- 6 çekirdek modül: cari, stok, satis, satin_alma, finans, muhasebe
- Temel ve ERP veri tipleri
- Modüller arası ilişki tanımları
- Schema validator aracı

### Modüller
- **cari**: Müşteri/tedarikçi kartları, gruplar, adresler
- **stok**: Stok kartları, kategoriler, depolar, hareketler, fiyat listeleri
- **satis**: Siparişler, irsaliyeler, faturalar, e-Fatura desteği
- **satin_alma**: Satın alma siparişleri, irsaliyeleri, faturaları
- **finans**: Kasa, banka, çek/senet, ödeme/tahsilat
- **muhasebe**: Hesap planı, muhasebe fişleri, defterler

---

## Sürüm Notları

### Versiyon Formatı
- **MAJOR**: Geriye uyumsuz değişiklikler
- **MINOR**: Geriye uyumlu yeni özellikler
- **PATCH**: Geriye uyumlu hata düzeltmeleri
