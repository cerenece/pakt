# PaktLang Tip Sistemi

PaktLang iki katmanlı bir tip sistemi kullanır: **Temel Tipler** ve **ERP Tipleri**.

## Temel Tipler (base_types.json)

| Tip | Açıklama | PostgreSQL | MySQL | MSSQL |
|-----|----------|------------|-------|-------|
| `integer` | Tam sayı | INTEGER | INT | INT |
| `bigint` | Büyük tam sayı | BIGINT | BIGINT | BIGINT |
| `decimal` | Ondalık sayı | DECIMAL | DECIMAL | DECIMAL |
| `string` | Metin | VARCHAR | VARCHAR | NVARCHAR |
| `text` | Uzun metin | TEXT | TEXT | NVARCHAR(MAX) |
| `boolean` | Mantıksal | BOOLEAN | TINYINT(1) | BIT |
| `date` | Tarih | DATE | DATE | DATE |
| `datetime` | Tarih/Saat | TIMESTAMP | DATETIME | DATETIME2 |
| `time` | Saat | TIME | TIME | TIME |
| `enum` | Seçenekler | VARCHAR | ENUM | VARCHAR |
| `json` | JSON veri | JSONB | JSON | NVARCHAR(MAX) |
| `uuid` | Benzersiz ID | UUID | CHAR(36) | UNIQUEIDENTIFIER |
| `binary` | İkili veri | BYTEA | BLOB | VARBINARY |

## ERP Tipleri (erp_types.json)

### Finansal

| Tip | Açıklama | Precision | Örnek |
|-----|----------|-----------|-------|
| `currency` | Para tutarı | 18,4 | 1234.5678 |
| `unit_price` | Birim fiyat | 18,6 | 12.345678 |
| `exchange_rate` | Döviz kuru | 18,6 | 34.567890 |
| `tax_rate` | Vergi oranı | 5,2 | 18.00 |
| `discount_rate` | İskonto | 5,2 | 10.50 |
| `percentage` | Yüzde | 5,2 | 25.00 |

### Stok

| Tip | Açıklama | Örnek |
|-----|----------|-------|
| `quantity` | Miktar | 100.000000 |
| `unit_code` | Birim kodu | AD, KG, LT |
| `warehouse_code` | Depo kodu | DEPO-01 |

### Kimlik

| Tip | Açıklama | Örnek |
|-----|----------|-------|
| `erp_code` | ERP kodu | STK-001 |
| `document_number` | Belge no | FAT2024000001 |
| `tax_number` | Vergi no | 1234567890 |
| `tc_kimlik` | TC Kimlik | 12345678901 |
| `iban` | IBAN | TR33... |

### İletişim

| Tip | Açıklama | Örnek |
|-----|----------|-------|
| `phone` | Telefon | +90 532 123 45 67 |
| `email` | E-posta | info@sirket.com |
| `country_code` | Ülke kodu | TR |
| `currency_code` | Para birimi | TRY |

### Muhasebe

| Tip | Açıklama | Örnek |
|-----|----------|-------|
| `account_code` | Hesap kodu | 320.001.001 |
| `fiscal_year` | Mali yıl | 2024 |
| `fiscal_period` | Mali dönem | 1-12 |

### ERP Mapping

| Tip | ERP | Açıklama |
|-----|-----|----------|
| `netsis_belge_tipi` | Netsis | STHAR_FTIRSIP |
| `netsis_hareket_turu` | Netsis | STHAR_HTUR |
| `logo_trcode` | Logo | STLINE.TRCODE |
| `logo_firma_kodu` | Logo | Firma prefix |

## Kullanım Örneği

```json
{
    "name": "toplam_tutar",
    "type": "currency",
    "description": "Toplam tutar"
},
{
    "name": "miktar",
    "type": "quantity",
    "required": true
},
{
    "name": "cari_kodu",
    "type": "erp_code",
    "unique": true
}
```
