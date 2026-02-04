# PaktLang

ERP veritabanı yapılarını Pakt ekosisteminin anlayacağı ortak, standart ve versiyonlanabilir şema dili.

## 🎯 Nedir?

PaktLang, farklı ERP sistemlerinin (Logo, Netsis, Mikro, Wolvox) veritabanı yapılarını tek bir standart dilde tanımlayan JSON tabanlı bir şema dilidir.

## 🚀 Hızlı Başlangıç

```bash
# Şema validasyonu
python validator/schema_validator.py --all modules/core

# Tek modül validasyonu
python validator/schema_validator.py modules/core/stok.json
```

## 📁 Proje Yapısı

```
paktlang/
├── meta/                 # Tip tanımları ve meta bilgiler
│   ├── paktlang.meta.json
│   ├── base_types.json   # Temel veri tipleri
│   └── erp_types.json    # ERP özel tipleri
├── modules/core/         # Ana modüller
│   ├── cari.json         # Müşteri/Tedarikçi
│   ├── stok.json         # Stok yönetimi
│   ├── satis.json        # Satış işlemleri
│   ├── satin_alma.json   # Satın alma
│   ├── finans.json       # Finans/Kasa/Banka
│   └── muhasebe.json     # Muhasebe
├── relations/            # Modüller arası ilişkiler
│   └── relations.json
├── mappings/             # ERP eşleştirmeleri
│   └── erp_mappings.json
├── validator/            # Şema doğrulama aracı
│   └── schema_validator.py
└── docs/                 # Dokümantasyon
```

## 📦 Modüller

| Modül | Açıklama | Durum |
|-------|----------|-------|
| cari | Müşteri ve tedarikçi hesapları | ✅ Aktif |
| stok | Stok kartları, depolar, hareketler | ✅ Aktif |
| satis | Siparişler, irsaliyeler, faturalar | ✅ Aktif |
| satin_alma | Satın alma siparişleri, tedarik | ✅ Aktif |
| finans | Kasa, banka, ödeme/tahsilat | ✅ Aktif |
| muhasebe | Hesap planı, muhasebe fişleri | ✅ Aktif |

## 🔗 Desteklenen ERP Sistemleri

| ERP | Versiyon | Durum |
|-----|----------|-------|
| Logo | Tiger 3, Go 3 | 🔄 Planlanan |
| Netsis | Standard, Enterprise | 🔄 Planlanan |
| Mikro | Jump, Classic | 🔄 Planlanan |
| Wolvox | - | 🔄 Planlanan |

## 📖 Dokümantasyon

- [Modül Geliştirme Rehberi](docs/module_guide.md)
- [Tip Sistemi](docs/types.md)
- [ERP Mapping](docs/erp_mapping.md)
- [Katkıda Bulunma](CONTRIBUTING.md)
- [Değişiklik Günlüğü](CHANGELOG.md)

## 🛠️ Geliştirme

```bash
# Validasyon çalıştır
python validator/schema_validator.py --all modules/core

# JSON formatında çıktı
python validator/schema_validator.py --all modules/core --json
```

## 📄 Lisans

Proprietary - Pakt Team © 2026
