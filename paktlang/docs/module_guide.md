# Modül Geliştirme Rehberi

Bu rehber, PaktLang'da yeni modül oluşturma veya mevcut modülleri güncelleme sürecini açıklar.

## Modül Yapısı

Her modül aşağıdaki yapıyı takip etmelidir:

```json
{
    "$schema": "paktlang://schema/module/v1",
    "$id": "paktlang://modules/[modul]/v1",
    "module": "[modul]",
    "version": "1.0.0",
    "description": "Modül açıklaması",
    "tables": [...]
}
```

## Tablo Tanımlama

### Ana Tablo (Master)

```json
{
    "pl_table": "stok_kart",
    "description": "Stok kartları",
    "is_master": true,
    "audit": true,
    "soft_delete": true,
    "columns": [...],
    "indexes": [...]
}
```

| Alan | Açıklama |
|------|----------|
| `pl_table` | Tablo adı (zorunlu) |
| `is_master` | Ana/referans tablosu mu |
| `audit` | created_at, updated_at otomatik |
| `soft_delete` | Silme yerine is_deleted |

### Kolon Tanımlama

```json
{
    "name": "stok_kodu",
    "type": "erp_code",
    "unique": true,
    "required": true,
    "indexed": true,
    "description": "Benzersiz stok kodu"
}
```

### Foreign Key

```json
{
    "name": "cari_id",
    "type": "bigint",
    "foreign_key": {
        "table": "cari_kart",
        "column": "id",
        "on_delete": "RESTRICT"
    }
}
```

**on_delete seçenekleri:**
- `RESTRICT`: Silmeyi engelle
- `CASCADE`: İlişkili kayıtları da sil
- `SET NULL`: NULL yap

## İndeksler

```json
"indexes": [
    {
        "name": "idx_stok_kategori",
        "columns": ["kategori_id", "stok_kodu"],
        "unique": false
    }
]
```

## Örnek: Basit Modül

```json
{
    "$schema": "paktlang://schema/module/v1",
    "$id": "paktlang://modules/ornek/v1",
    "module": "ornek",
    "version": "1.0.0",
    "description": "Örnek modül",
    "tables": [
        {
            "pl_table": "ornek_tablo",
            "description": "Örnek tablo",
            "is_master": true,
            "columns": [
                {
                    "name": "id",
                    "type": "bigint",
                    "primary_key": true,
                    "auto_increment": true
                },
                {
                    "name": "kod",
                    "type": "erp_code",
                    "unique": true,
                    "required": true
                },
                {
                    "name": "adi",
                    "type": "string",
                    "max_length": 200,
                    "required": true
                }
            ]
        }
    ]
}
```
