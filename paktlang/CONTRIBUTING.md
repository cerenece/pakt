# Katkıda Bulunma Rehberi

PaktLang projesine katkıda bulunmak istediğiniz için teşekkürler! 

## 🚀 Başlamadan Önce

1. Projeyi klonlayın
2. Mevcut yapıyı inceleyin (`meta/paktlang.meta.json`)
3. Validator'ın çalıştığından emin olun

## 📝 Yeni Modül Ekleme

### 1. Modül Dosyası Oluşturma

`modules/core/` altında yeni JSON dosyası oluşturun:

```json
{
    "$schema": "paktlang://schema/module/v1",
    "$id": "paktlang://modules/[modul_adi]/v1",
    "module": "[modul_adi]",
    "version": "1.0.0",
    "description": "Modül açıklaması",
    "tables": [...]
}
```

### 2. Tablo Yapısı

Her tablo için:

```json
{
    "pl_table": "tablo_adi",
    "description": "Tablo açıklaması",
    "is_master": true,
    "audit": true,
    "columns": [
        {
            "name": "id",
            "type": "bigint",
            "primary_key": true,
            "auto_increment": true
        }
    ]
}
```

### 3. Validasyon

```bash
python validator/schema_validator.py modules/core/[modul_adi].json
```

## 🔧 Yeni Tip Ekleme

`meta/erp_types.json` dosyasına ekleyin:

```json
"yeni_tip": {
    "description": "Tip açıklaması",
    "base_type": "string",
    "extends": {
        "max_length": 50
    },
    "metadata": {
        "category": "kategori"
    }
}
```

## 🗺️ ERP Mapping Ekleme

`mappings/erp_mappings.json` dosyasında:

```json
"[erp_adi]": {
    "version": "X.X",
    "modules": {
        "[modul]": {
            "[tablo]": {
                "erp_table": "ERP_TABLO_ADI",
                "field_mappings": { ... }
            }
        }
    }
}
```

## ✅ Kontrol Listesi

Değişiklik yapmadan önce:

- [ ] Kod stili tutarlı mı?
- [ ] Validasyon geçiyor mu?
- [ ] Açıklayıcı description'lar var mı?
- [ ] Foreign key'ler doğru mu?
- [ ] CHANGELOG güncellendi mi?

## 📋 Commit Mesajları

Format: `[tip]: açıklama`

- `feat:` Yeni özellik
- `fix:` Hata düzeltme
- `docs:` Dokümantasyon
- `refactor:` Kod düzenleme
- `test:` Test ekleme

Örnek: `feat: stok modülüne konsinye alanları eklendi`
