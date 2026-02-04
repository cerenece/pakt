"""
PaktLang Schema Validator
Şema dosyalarını doğrulama modülü
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any


class ValidationError:
    """Doğrulama hatası"""
    def __init__(self, code: str, message: str, path: str = "", severity: str = "error"):
        self.code = code
        self.message = message
        self.path = path
        self.severity = severity  # error, warning
    
    def __str__(self):
        return f"[{self.code}] {self.path}: {self.message}"
    
    def to_dict(self) -> Dict:
        return {
            "code": self.code,
            "message": self.message,
            "path": self.path,
            "severity": self.severity
        }


class SchemaValidator:
    """PaktLang şema dosyalarını doğrulayan sınıf"""
    
    # Hata kodları
    ERROR_CODES = {
        "PL001": "Geçersiz JSON formatı",
        "PL002": "Bilinmeyen veri tipi",
        "PL003": "Zorunlu alan eksik",
        "PL004": "Duplike kolon adı",
        "PL005": "Geçersiz foreign key referansı",
        "PL006": "Döngüsel bağımlılık tespit edildi",
        "PL007": "Versiyon uyumsuzluğu",
        "PL008": "Geçersiz pattern (regex)",
        "PL009": "Değer aralık dışında",
        "PL010": "Reserved keyword kullanımı"
    }
    
    # Temel veri tipleri
    BASE_TYPES = [
        "integer", "bigint", "decimal", "string", "text", "boolean",
        "date", "datetime", "time", "enum", "json", "uuid", "binary"
    ]
    
    # ERP özel tipleri
    ERP_TYPES = [
        "currency", "quantity", "unit_price", "percentage", "tax_rate",
        "discount_rate", "exchange_rate", "erp_code", "document_number",
        "tax_number", "tc_kimlik", "phone", "email", "iban",
        "currency_code", "country_code", "unit_code", "fiscal_year",
        "fiscal_period", "account_code", "warehouse_code"
    ]
    
    # Zorunlu modül alanları
    REQUIRED_MODULE_FIELDS = ["module", "version", "description", "tables"]
    
    # Zorunlu tablo alanları
    REQUIRED_TABLE_FIELDS = ["pl_table", "columns"]
    
    # Zorunlu kolon alanları
    REQUIRED_COLUMN_FIELDS = ["name", "type"]
    
    # Reserved keywords (SQL)
    RESERVED_KEYWORDS = [
        "select", "insert", "update", "delete", "from", "where", "and", "or",
        "table", "index", "create", "drop", "alter", "primary", "foreign", "key"
    ]
    
    def __init__(self, base_path: str = None):
        """
        Args:
            base_path: PaktLang şema dosyalarının bulunduğu ana dizin
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []
        self.loaded_modules: Dict[str, Dict] = {}
    
    def validate_json_syntax(self, file_path: str) -> Tuple[bool, Optional[Dict]]:
        """JSON syntax doğrulaması"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return True, data
        except json.JSONDecodeError as e:
            self.errors.append(ValidationError(
                "PL001", f"JSON parse hatası: {str(e)}", file_path
            ))
            return False, None
        except FileNotFoundError:
            self.errors.append(ValidationError(
                "PL001", f"Dosya bulunamadı", file_path
            ))
            return False, None
    
    def validate_type(self, type_name: str, column_path: str) -> bool:
        """Veri tipi doğrulaması"""
        all_types = self.BASE_TYPES + self.ERP_TYPES
        if type_name not in all_types:
            self.errors.append(ValidationError(
                "PL002", f"Bilinmeyen veri tipi: {type_name}", column_path
            ))
            return False
        return True
    
    def validate_column(self, column: Dict, table_name: str, col_index: int) -> bool:
        """Kolon doğrulaması"""
        col_path = f"{table_name}.columns[{col_index}]"
        is_valid = True
        
        # Zorunlu alanlar
        for field in self.REQUIRED_COLUMN_FIELDS:
            if field not in column:
                self.errors.append(ValidationError(
                    "PL003", f"Zorunlu alan eksik: {field}", col_path
                ))
                is_valid = False
        
        if not is_valid:
            return False
        
        col_name = column.get("name", "unknown")
        col_path = f"{table_name}.{col_name}"
        
        # Tip doğrulama
        if "type" in column:
            self.validate_type(column["type"], col_path)
        
        # Reserved keyword kontrolü
        if col_name.lower() in self.RESERVED_KEYWORDS:
            self.errors.append(ValidationError(
                "PL010", f"Reserved keyword kullanılmış: {col_name}", col_path
            ))
            is_valid = False
        
        # Pattern doğrulama (varsa)
        if "pattern" in column:
            try:
                re.compile(column["pattern"])
            except re.error:
                self.errors.append(ValidationError(
                    "PL008", f"Geçersiz regex pattern", col_path
                ))
                is_valid = False
        
        # Enum değerleri kontrolü
        if column.get("type") == "enum":
            if "values" not in column or not column["values"]:
                self.errors.append(ValidationError(
                    "PL003", "Enum tipi için 'values' zorunlu", col_path
                ))
                is_valid = False
        
        # Decimal constraints
        if column.get("type") == "decimal":
            precision = column.get("precision", 18)
            scale = column.get("scale", 2)
            if scale > precision:
                self.errors.append(ValidationError(
                    "PL009", f"Scale ({scale}) precision'dan ({precision}) büyük olamaz", col_path
                ))
                is_valid = False
        
        return is_valid
    
    def validate_table(self, table: Dict, module_name: str, table_index: int) -> bool:
        """Tablo doğrulaması"""
        table_path = f"{module_name}.tables[{table_index}]"
        is_valid = True
        
        # Zorunlu alanlar
        for field in self.REQUIRED_TABLE_FIELDS:
            if field not in table:
                self.errors.append(ValidationError(
                    "PL003", f"Zorunlu alan eksik: {field}", table_path
                ))
                is_valid = False
        
        if not is_valid:
            return False
        
        table_name = table.get("pl_table", "unknown")
        table_path = f"{module_name}.{table_name}"
        
        # Kolon adları benzersizlik kontrolü
        column_names = []
        for i, column in enumerate(table.get("columns", [])):
            col_name = column.get("name")
            if col_name:
                if col_name in column_names:
                    self.errors.append(ValidationError(
                        "PL004", f"Duplike kolon adı: {col_name}", table_path
                    ))
                    is_valid = False
                else:
                    column_names.append(col_name)
            
            # Kolon doğrulama
            if not self.validate_column(column, table_path, i):
                is_valid = False
        
        # Primary key kontrolü
        has_pk = any(col.get("primary_key") for col in table.get("columns", []))
        if not has_pk:
            self.warnings.append(ValidationError(
                "PL003", "Primary key tanımlanmamış", table_path, "warning"
            ))
        
        return is_valid
    
    def validate_module(self, file_path: str) -> Tuple[bool, List[ValidationError]]:
        """Modül şemasını doğrular"""
        self.errors = []
        self.warnings = []
        
        # JSON syntax
        is_valid, data = self.validate_json_syntax(file_path)
        if not is_valid:
            return False, self.errors
        
        module_name = data.get("module", Path(file_path).stem)
        
        # Zorunlu modül alanları
        for field in self.REQUIRED_MODULE_FIELDS:
            if field not in data:
                self.errors.append(ValidationError(
                    "PL003", f"Zorunlu alan eksik: {field}", module_name
                ))
                is_valid = False
        
        # Versiyon format kontrolü
        version = data.get("version", "")
        if not re.match(r'^\d+\.\d+\.\d+$', version):
            self.errors.append(ValidationError(
                "PL007", f"Geçersiz versiyon formatı: {version} (beklenen: X.Y.Z)", module_name
            ))
            is_valid = False
        
        # Tablo doğrulamaları
        for i, table in enumerate(data.get("tables", [])):
            if not self.validate_table(table, module_name, i):
                is_valid = False
        
        # Bağımlılık kontrolü
        self.loaded_modules[module_name] = data
        
        return is_valid, self.errors + self.warnings
    
    def validate_foreign_keys(self, modules: Dict[str, Dict]) -> List[ValidationError]:
        """Modüller arası foreign key tutarlılığını kontrol eder"""
        errors = []
        
        for module_name, module_data in modules.items():
            for table in module_data.get("tables", []):
                table_name = table.get("pl_table")
                
                for column in table.get("columns", []):
                    fk = column.get("foreign_key")
                    if not fk:
                        continue
                    
                    # Foreign key referansı kontrolü
                    target_module = fk.get("module", module_name)
                    target_table = fk.get("table")
                    target_column = fk.get("column")
                    
                    # Hedef modül var mı?
                    if target_module not in modules:
                        errors.append(ValidationError(
                            "PL005",
                            f"Foreign key hedef modülü bulunamadı: {target_module}",
                            f"{module_name}.{table_name}.{column.get('name')}"
                        ))
                        continue
                    
                    # Hedef tablo var mı?
                    target_mod = modules[target_module]
                    target_tables = [t.get("pl_table") for t in target_mod.get("tables", [])]
                    
                    if target_table not in target_tables:
                        errors.append(ValidationError(
                            "PL005",
                            f"Foreign key hedef tablosu bulunamadı: {target_module}.{target_table}",
                            f"{module_name}.{table_name}.{column.get('name')}"
                        ))
        
        return errors
    
    def validate_all(self, modules_path: str = None) -> Dict[str, Any]:
        """Tüm modülleri doğrular"""
        if modules_path:
            modules_dir = Path(modules_path)
        else:
            modules_dir = self.base_path / "paktlang" / "modules" / "core"
        
        results = {
            "valid": True,
            "modules": {},
            "errors": [],
            "warnings": [],
            "summary": {}
        }
        
        all_modules = {}
        
        # Her modülü doğrula
        for json_file in modules_dir.glob("*.json"):
            module_name = json_file.stem
            is_valid, issues = self.validate_module(str(json_file))
            
            results["modules"][module_name] = {
                "valid": is_valid,
                "errors": [e.to_dict() for e in self.errors],
                "warnings": [w.to_dict() for w in self.warnings]
            }
            
            if not is_valid:
                results["valid"] = False
                results["errors"].extend([e.to_dict() for e in self.errors])
            
            results["warnings"].extend([w.to_dict() for w in self.warnings])
            
            # Modülü yükle
            _, data = self.validate_json_syntax(str(json_file))
            if data:
                all_modules[module_name] = data
        
        # Cross-module foreign key kontrolü
        fk_errors = self.validate_foreign_keys(all_modules)
        if fk_errors:
            results["valid"] = False
            results["errors"].extend([e.to_dict() for e in fk_errors])
        
        # Özet
        results["summary"] = {
            "total_modules": len(results["modules"]),
            "valid_modules": sum(1 for m in results["modules"].values() if m["valid"]),
            "total_errors": len(results["errors"]),
            "total_warnings": len(results["warnings"])
        }
        
        return results


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="PaktLang Schema Validator")
    parser.add_argument("path", nargs="?", help="Şema dosyası veya modüller dizini")
    parser.add_argument("--all", action="store_true", help="Tüm modülleri doğrula")
    parser.add_argument("--json", action="store_true", help="JSON formatında çıktı")
    
    args = parser.parse_args()
    
    validator = SchemaValidator()
    
    if args.all or not args.path:
        results = validator.validate_all(args.path)
        
        if args.json:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            print(f"\n{'='*50}")
            print("PaktLang Schema Validation Report")
            print(f"{'='*50}\n")
            
            for mod_name, mod_result in results["modules"].items():
                status = "[OK]" if mod_result["valid"] else "[FAIL]"
                print(f"{status} {mod_name}")
                
                for err in mod_result["errors"]:
                    print(f"  [ERROR] [{err['code']}] {err['message']}")
                
                for warn in mod_result["warnings"]:
                    print(f"  [WARN] [{warn['code']}] {warn['message']}")
            
            print(f"\n{'='*50}")
            print(f"Toplam: {results['summary']['valid_modules']}/{results['summary']['total_modules']} modul gecerli")
            print(f"Hatalar: {results['summary']['total_errors']}, Uyarilar: {results['summary']['total_warnings']}")
    else:
        is_valid, issues = validator.validate_module(args.path)
        
        if args.json:
            print(json.dumps({
                "valid": is_valid,
                "errors": [e.to_dict() for e in validator.errors],
                "warnings": [w.to_dict() for w in validator.warnings]
            }, indent=2, ensure_ascii=False))
        else:
            print(f"Dosya: {args.path}")
            print(f"Geçerli: {'Evet' if is_valid else 'Hayır'}\n")
            
            for err in validator.errors:
                print(f"❌ {err}")
            
            for warn in validator.warnings:
                print(f"⚠️ {warn}")


if __name__ == "__main__":
    main()
