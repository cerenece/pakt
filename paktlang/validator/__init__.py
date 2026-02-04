"""
PaktLang Validator Package
"""

from .schema_validator import SchemaValidator, ValidationError

__version__ = "1.0.0"
__all__ = ["SchemaValidator", "ValidationError"]
