# PaktLang

ERP veritabanlarına erişim haritası - farklı ERP sistemlerini ortak bir dilde tanımlayan şema.

## 🎯 Nedir?

PaktLang (PL), farklı ERP sistemlerinin (Logo, Netsis, Akınsoft, Mikro) veritabanlarına **nasıl ulaşılacağını** tanımlayan bir harita dilidir.

> **Önemli:** PL veriyi taşımaz, dönüştürmez. Sadece ERP veritabanını **adresler**.

### Harita Mantığı

```
Kullanıcı: "Stok kartlarını getir"
    ↓
Sistem: PL'de stok_kart → Netsis'te TBLSTSABIT
    ↓
SQL: SELECT * FROM TBLSTSABIT
```

## 📁 Proje Yapısı

```
paktlang/
├── modules/core/         # Ana modül iskeletleri
│   └── stok.json         # Stok modülü
├── mappings/             # ERP eşleştirmeleri (TODO)
├── meta/                 # Tip tanımları
└── validator/            # Şema doğrulama
```

## 🗺️ Şema Yapısı

### Tablo Tanımı

```json
{
    "pl_table": "stok_kart",
    "real_name": [],
    "description": "Stok/ürün ana kartları",
    "is_master": true,
    "audit": true,
    "soft_delete": true,
    "columns": [...]
}
```

| Alan | Tip | Açıklama |
|------|-----|----------|
| `pl_table` | string | PL standart tablo adı |
| `real_name` | array | ERP'deki gerçek tablo(lar) |
| `is_master` | boolean | Ana kayıt tablosu mu |
| `audit` | boolean | Değişiklik takibi |
| `soft_delete` | boolean | Yumuşak silme |

### Kolon Tanımı

```json
{
    "pl_column": "stok_kodu",
    "real_name": "",
    "type": "string",
    "required": true,
    "unique": true
}
```

| Alan | Tip | Açıklama |
|------|-----|----------|
| `pl_column` | string | PL standart kolon adı |
| `real_name` | string | ERP'deki gerçek kolon adı |
| `type` | string | Veri tipi |
| `required` | boolean | Zorunlu alan |

## 📦 Stok Modülü Tabloları

| Tablo | Açıklama |
|-------|----------|
| `stok_kart` | Ürün ana kartları |
| `stok_kategori` | Kategoriler |
| `birim` | Ölçü birimleri |
| `depo` | Depo tanımları |
| `marka` | Markalar |
| `stok_hareket` | Giriş/çıkış |
| `stok_bakiye` | Güncel bakiye |
| `stok_fiyat` | Fiyat listeleri |
| `stok_birim_cevrimi` | Birim dönüşümleri |

## 🔗 Desteklenen ERP'ler

| ERP | Örnek Tablo | Durum |
|-----|-------------|-------|
| Logo | LG_XXX_ITEMS | 🔄 Planlanan |
| Netsis | TBLSTSABIT | 🔄 Planlanan |
| Akınsoft | STOK | 🔄 Planlanan |

## 💡 Örnek Eşleştirme

```json
{
    "pl_table": "stok_kart",
    "real_name": ["TBLSTSABIT"],
    "columns": [
        { "pl_column": "stok_kodu", "real_name": "STKKOD" },
        { "pl_column": "stok_adi", "real_name": "STKCINSI" }
    ]
}
```

## 📄 Lisans

Proprietary - Pakt Team © 2026
