# ERP Mapping Rehberi

PaktLang şemaları farklı ERP sistemlerine eşleştirilebilir. Bu rehber mapping yapısını açıklar.

## Desteklenen ERP'ler

| ERP | Versiyon | Durum |
|-----|----------|-------|
| Netsis | Standard, Enterprise | Mapping mevcut |
| Logo | Tiger 3, Go 3 | Mapping mevcut |
| Mikro | Jump, Classic | Temel mapping |
| Wolvox | - | Temel mapping |

## Mapping Yapısı

`mappings/erp_mappings.json` dosyasında her ERP için eşleştirmeler tanımlıdır.

### Tablo Mapping

```json
"netsis": {
    "modules": {
        "stok": {
            "stok_kart": {
                "erp_table": "TBLSTKART",
                "field_mappings": {
                    "stok_kodu": "STKKOD",
                    "stok_adi": "STKCINSI"
                }
            }
        }
    }
}
```

### Alan Mapping

| PaktLang | Netsis | Logo |
|----------|--------|------|
| stok_kodu | STKKOD | CODE |
| stok_adi | STKCINSI | NAME |
| barkod | BARKOD1 | BARCODE |

### Özel Alanlar

Bazı ERP'ler özel kodlama kullanır:

```json
"special_fields": {
    "belge_tipi_kod": {
        "erp_field": "STHAR_FTIRSIP",
        "mappings": {
            "1": "satis_fatura",
            "2": "alis_fatura"
        }
    }
}
```

## Netsis Mapping

### TBLSTHAR (Stok Hareket)

| PaktLang | Netsis Alan | Değerler |
|----------|-------------|----------|
| belge_tipi_kod | STHAR_FTIRSIP | 1-9, A |
| hareket_turu_kod | STHAR_HTUR | A-M |
| kaynak_belge_tipi | STHAR_BGTIP | F, I |

### Hareket Türleri

| Kod | Açıklama |
|-----|----------|
| A | Devir |
| B | Transfer |
| C | Üretim |
| F | Konsinye |
| G | Müstahsil |
| I | Kapalı Fatura |
| J | Açık Fatura |
| L | İade |

## Logo Mapping

### Tablo Adlandırma

Logo tabloları firma kodlu prefix kullanır:
- `LG_{FIRMA}_ITEMS` → Stok Kartları
- `LG_{FIRMA}_STLINE` → Stok Hareketleri
- `LG_{FIRMA}_CLCARD` → Cari Kartlar

### TRCODE Değerleri

| Kod | Açıklama |
|-----|----------|
| 1 | Alış |
| 2-3 | Satış |
| 4-5 | Konsinye |
| 11 | Fire |
| 25 | Transfer |

## Dönüşüm Kuralları

### Tarih Formatları

| ERP | Format |
|-----|--------|
| PaktLang | YYYY-MM-DD |
| Netsis | YYYY-MM-DD |
| Logo | YYYY-MM-DD HH:mm:ss |
| Mikro | DD.MM.YYYY |

### Boolean Değerler

| ERP | True | False |
|-----|------|-------|
| Netsis | 1 | 0 |
| Logo | 1 | 0 |
| Mikro | E | H |

## Yeni ERP Ekleme

1. `erp_mappings.json`'a yeni ERP bloğu ekle
2. Tablo mapping'lerini tanımla
3. Özel alanları belirle
4. Dönüşüm kurallarını ekle
