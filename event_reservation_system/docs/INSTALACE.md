# Návod na Instalaci a Spuštění

Tento dokument vás provede procesem instalace a spuštění projektu EventHub na vašem lokálním počítači (Windows/macOS/Linux).

## 1. Prerekvizity

Před začátkem se ujistěte, že máte nainstalováno:

*   **Python 3.8** nebo novější. [Stáhnout Python](https://www.python.org/downloads/)
*   **MySQL Server**. Doporučujeme balíček **XAMPP** (obsahuje MySQL i PHPMyAdmin) nebo oficiální MySQL Community Server.

## 2. Stažení a Příprava Prostředí

1.  Otevřete terminál (příkazový řádek) ve složce s projektem:
    ```bash
    cd /cesta/k/projektu/EventHub
    ```

2.  Nainstalujte potřebné Python knihovny:
    ```bash
    pip install flask mysql-connector-python
    ```
    *(Pokud příkaz `pip` nefunguje, zkuste `pip3` nebo `python -m pip`)*

## 3. Konfigurace Databáze

Projekt potřebuje vědět, jak se připojit k vaší databázi.

1.  Otevřete soubor `event_reservation_system/config.json`.
2.  Upravte sekci `"database"` podle vašeho nastavení MySQL.
    
    **Příklad pro XAMPP (výchozí nastavení):**
    ```json
    "database": {
        "host": "localhost",
        "user": "root",
        "password": "", 
        "database": "event_system_db"
    }
    ```
    *Poznámka: Název databáze `event_system_db` neměňte, pokud nechcete měnit i zdrojový kód.*

## 4. Inicializace Databáze

Nyní vytvoříme strukturu databáze (tabulky a data). Spusťte tento skript v kořenové složce projektu (tam, kde je složka `event_reservation_system`):

```bash
python event_reservation_system/init_db.py
```
*(Na macOS/Linux použijte `python3` místo `python`, pokud je to potřeba.)*

Pokud vše proběhne v pořádku, uvidíte zprávu: `Database initialized successfully.`

## 5. Spuštění Aplikace

Spusťte webový server příkazem:

```bash
python event_reservation_system/app.py
```

Po spuštění byste měli vidět výpis informující, že server běží, obvykle na adrese:
`http://127.0.0.1:5000`

Otevřete tuto adresu ve svém webovém prohlížeči.

## 6. Řešení Častých Problémů

### Chyba: `ModuleNotFoundError: No module named 'flask'`
**Řešení**: Nemáte nainstalované knihovny. Spusťte znovu krok 2: `pip install flask mysql-connector-python`.

### Chyba: `mysql.connector.errors.DatabaseError: 2003 (HY000): Can't connect to MySQL server`
**Řešení**: Váš MySQL server neběží. Spusťte XAMPP Control Panel a zapněte modul MySQL.

### Chyba: `Access denied for user 'root'@'localhost'`
**Řešení**: Máte špatné heslo v `config.json`. Zkontrolujte přihlašovací údaje k vaší databázi.
