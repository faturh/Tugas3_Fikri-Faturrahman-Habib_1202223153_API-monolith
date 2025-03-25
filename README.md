# API Cuaca

API ini menyediakan data cuaca terkini untuk kota-kota di seluruh dunia.

## Endpoint

**GET** `/weather?city={nama_kota}`

### Parameter
- `city` (optional): Nama kota (default: Jakarta)

### Contoh Request:
```bash
GET http://localhost:5000/weather?city=London
