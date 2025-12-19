# SocialX — Lokalt utvecklings-README

Detta repo innehåller en enkel Flask-app (SocialX) med användarregistrering, inloggning och inlägg. Följ stegen nedan för att köra appen lokalt med Docker.

## Förutsättningar
- Docker
- docker-compose

## Snabbstart (rekommenderat)
1. Bygg och starta tjänsterna (app + MySQL):

```bash
docker-compose up --build
```

2. Öppna appen i webbläsaren:

```
http://localhost:5000
```

3. Stoppa och ta bort containers (inkl. volymer):

```bash
docker-compose down -v
```

## Miljövariabler
- `SQLALCHEMY_DATABASE_URI` kan konfigureras för att peka på en extern databas. I `docker-compose.yml` sätts den automatiskt till `mysql+pymysql://dbadm:P%40ssw0rd@db:3306/socialx`.
- `SECRET_KEY` används av Flask för sessioner. Byt den i produktion.

Tips: skapa en `.env`-fil och kör `export $(cat .env | xargs)` eller använd Compose `env_file` för att undvika hårdkodade lösenord.

## Kör utan Docker (lokalt Python-venv)
1. Skapa och aktivera ett virtuellt env:

```bash
python -m venv venv
source venv/bin/activate
```

2. Installera beroenden:

```bash
pip install -r requirements.txt
```

3. Sätt miljövariabler (exempel):

```bash
export SQLALCHEMY_DATABASE_URI="mysql+pymysql://dbadm:P%40ssw0rd@Timpa.local/socialx?charset=utf8mb4"
export SECRET_KEY="change-me"
```

4. Kör appen:

```bash
python app.py
```

## Databas
- `docker-compose.yml` skapar en MySQL-container och initialiserar schema från `sql/ddl.sql` på första start.
- För utveckling körs `db.create_all()` i `app.py` (bekvämlighet). I produktion rekommenderas migrations (Flask-Migrate/Alembic).

## Vanliga problem
- `ERR_EMPTY_RESPONSE` från webbläsaren: kontrollera att Flask körs på `0.0.0.0:5000` och att Docker mappar port 5000.
- `cryptography`-fel för MySQL-auth: se till att `cryptography` är i `requirements.txt` och bygg om imagen.
- Schema-fel (saknad kolumn): radera volymen och starta om för att injicera nytt `ddl.sql`:

```bash
docker-compose down -v
docker-compose up --build
```