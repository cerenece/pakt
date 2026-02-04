#!/usr/bin/env python
"""
PaktLang CLI
Komut satırı arayüzü
"""

import argparse
import json
import sys
from pathlib import Path

# Proje path'ini ekle
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from paktlang.validator.schema_validator import SchemaValidator


def cmd_validate(args):
    """validate komutu"""
    validator = SchemaValidator(args.base_path)
    
    if args.file:
        is_valid, _ = validator.validate_module(args.file)
        result = {
            "file": args.file,
            "valid": is_valid,
            "errors": [e.to_dict() for e in validator.errors],
            "warnings": [w.to_dict() for w in validator.warnings]
        }
    else:
        result = validator.validate_all()
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print_validation_result(result)
    
    return 0 if result.get("valid", False) else 1


def cmd_info(args):
    """info komutu - modül bilgilerini göster"""
    validator = SchemaValidator(args.base_path)
    
    is_valid, data = validator.validate_json_syntax(args.file)
    if not is_valid:
        print(f"Hata: Dosya okunamadı")
        return 1
    
    print(f"\n{'='*50}")
    print(f"Modül: {data.get('module', 'N/A')}")
    print(f"Versiyon: {data.get('version', 'N/A')}")
    print(f"Açıklama: {data.get('description', 'N/A')}")
    print(f"{'='*50}\n")
    
    print("Tablolar:")
    for table in data.get("tables", []):
        table_name = table.get("pl_table")
        col_count = len(table.get("columns", []))
        is_master = "✓" if table.get("is_master") else " "
        has_audit = "✓" if table.get("audit") else " "
        print(f"  • {table_name} ({col_count} kolon) [master:{is_master}] [audit:{has_audit}]")
    
    print(f"\nToplam: {len(data.get('tables', []))} tablo")
    
    deps = data.get("dependencies", [])
    if deps:
        print(f"Bağımlılıklar: {', '.join(deps)}")
    
    return 0


def cmd_list(args):
    """list komutu - tüm modülleri listele"""
    base_path = Path(args.base_path) if args.base_path else Path.cwd()
    modules_dir = base_path / "paktlang" / "modules" / "core"
    
    print(f"\nPaktLang Modülleri ({modules_dir}):\n")
    
    for json_file in sorted(modules_dir.glob("*.json")):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            module_name = data.get("module", json_file.stem)
            version = data.get("version", "?")
            table_count = len(data.get("tables", []))
            priority = data.get("priority", "normal")
            
            print(f"  {module_name:15} v{version:8} {table_count:2} tablo  [{priority}]")
        except Exception as e:
            print(f"  {json_file.stem:15} ❌ Hata: {e}")
    
    return 0


def cmd_stats(args):
    """stats komutu - istatistikleri göster"""
    base_path = Path(args.base_path) if args.base_path else Path.cwd()
    modules_dir = base_path / "paktlang" / "modules" / "core"
    
    stats = {
        "modules": 0,
        "tables": 0,
        "columns": 0,
        "indexes": 0,
        "views": 0,
        "relations": 0
    }
    
    for json_file in modules_dir.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            stats["modules"] += 1
            
            for table in data.get("tables", []):
                stats["tables"] += 1
                stats["columns"] += len(table.get("columns", []))
                stats["indexes"] += len(table.get("indexes", []))
            
            stats["views"] += len(data.get("views", []))
        except Exception:
            pass
    
    # Relations dosyası
    relations_file = base_path / "paktlang" / "relations" / "relations.json"
    if relations_file.exists():
        try:
            with open(relations_file, 'r', encoding='utf-8') as f:
                rel_data = json.load(f)
            stats["relations"] = len(rel_data.get("cross_module_relations", []))
        except Exception:
            pass
    
    print(f"\n{'='*40}")
    print("PaktLang İstatistikleri")
    print(f"{'='*40}\n")
    print(f"  Modüller:    {stats['modules']:>5}")
    print(f"  Tablolar:    {stats['tables']:>5}")
    print(f"  Kolonlar:    {stats['columns']:>5}")
    print(f"  İndeksler:   {stats['indexes']:>5}")
    print(f"  View'lar:    {stats['views']:>5}")
    print(f"  İlişkiler:   {stats['relations']:>5}")
    print(f"\n{'='*40}\n")
    
    return 0


def print_validation_result(result):
    """Doğrulama sonucunu güzel formatta yazdır"""
    print(f"\n{'='*50}")
    print("PaktLang Schema Validation Report")
    print(f"{'='*50}\n")
    
    if "modules" in result:
        for mod_name, mod_result in result["modules"].items():
            status = "[OK]" if mod_result["valid"] else "[FAIL]"
            print(f"{status} {mod_name}")
            
            for err in mod_result.get("errors", []):
                print(f"  [ERROR] [{err['code']}] {err['message']}")
            
            for warn in mod_result.get("warnings", []):
                print(f"  [WARN] [{warn['code']}] {warn['message']}")
        
        summary = result.get("summary", {})
        print(f"\n{'='*50}")
        print(f"Toplam: {summary.get('valid_modules', 0)}/{summary.get('total_modules', 0)} modul gecerli")
        print(f"Hatalar: {summary.get('total_errors', 0)}, Uyarilar: {summary.get('total_warnings', 0)}")
    else:
        status = "[OK] Gecerli" if result.get("valid") else "[FAIL] Gecersiz"
        print(f"Dosya: {result.get('file', 'N/A')}")
        print(f"Durum: {status}\n")
        
        for err in result.get("errors", []):
            print(f"[ERROR] [{err['code']}] {err['path']}: {err['message']}")
        
        for warn in result.get("warnings", []):
            print(f"[WARN] [{warn['code']}] {warn['path']}: {warn['message']}")


def main():
    parser = argparse.ArgumentParser(
        prog="paktlang",
        description="PaktLang Şema Yönetim Aracı"
    )
    parser.add_argument(
        "--base-path", "-b",
        help="Proje ana dizini",
        default=None
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Komutlar")
    
    # validate komutu
    validate_parser = subparsers.add_parser("validate", help="Şema doğrulama")
    validate_parser.add_argument("--file", "-f", help="Tek dosya doğrula")
    validate_parser.add_argument("--json", action="store_true", help="JSON çıktı")
    validate_parser.set_defaults(func=cmd_validate)
    
    # info komutu
    info_parser = subparsers.add_parser("info", help="Modül bilgileri")
    info_parser.add_argument("file", help="Modül dosyası")
    info_parser.set_defaults(func=cmd_info)
    
    # list komutu
    list_parser = subparsers.add_parser("list", help="Modülleri listele")
    list_parser.set_defaults(func=cmd_list)
    
    # stats komutu
    stats_parser = subparsers.add_parser("stats", help="İstatistikler")
    stats_parser.set_defaults(func=cmd_stats)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
