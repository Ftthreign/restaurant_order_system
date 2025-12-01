Backend FastAPI

Masuk ke folder backend:

cd backend

Install dependency:

python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows
pip install -r requirements.txt

Jalankan migrasi database:

alembic upgrade head

Jalankan server:

uvicorn app.main:app --reload

Backend tersedia di:

http://localhost:8000

Dokumentasi API tersedia di:

http://localhost:8000/docs

▶ Frontend HTML

Masuk ke folder frontend:

cd frontend

Tidak memerlukan build.
Jalankan dengan:

Opsi 1: Buka langsung file HTML

Buka pages/\*.html di browser.

Opsi 2: Jalankan static server
python -m http.server 3000

Frontend tersedia di:

http://localhost:3000

🛢 Database

Gunakan MySQL / MariaDB dengan struktur tabel:

customers

tables

menu

reservations

orders

order_items

Semua migrasi dikelola oleh Alembic.

🧪 Pengujian

Gunakan:

Unit Test di backend (pytest)

Manual testing via frontend HTML
