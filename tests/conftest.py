import sys
from unittest.mock import MagicMock

MOCK_MODULES = [
    "postgres_helpers",
    "cliente_contratos",
    "cliente_postgres",
    "cliente_siafi",
    "cliente_email"
]

for module_name in MOCK_MODULES:
    sys.modules[module_name] = MagicMock()
