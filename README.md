# RestockHub — MVP (Full Demo)

✅ Полный рабочий скелет Django + DRF с демо-данными.
- БД: SQLite по умолчанию (0 настроек)
- Валюта: EUR (символ € в API)
- Команда `seed_demo` создаёт пользователей, товары, заказ, оффер, предзаказ, календарь, отзывы, избранное, waitlist.

## Быстрый старт (macOS/Linux/Windows PowerShell одинаково, меняется только активация venv)
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt

cd backend
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Открой: http://127.0.0.1:8000/api/

Демо-логины:
- Restaurant: demo_restaurant / demo12345
- Supplier:  demo_supplier  / demo12345
- Farmer:    demo_farmer    / demo12345

## Переключение на PostgreSQL (опционально)
```bash
cp .env.example .env    # отредактируй DB_BACKEND=postgres и POSTGRES_* переменные
cd backend
python manage.py migrate
python manage.py runserver
```
