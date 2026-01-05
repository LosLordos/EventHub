# Návod na spuštění projektu na školním PC



## 1. Příprava Databáze (MySQL)



1.  **Spusťte MySQL Server** (pokud neběží).
2.  **Zjistěte přihlašovací údaje**:
    *   Obvykle na školních PC nebo XAMPP bývá:
        *   Host: `localhost`
        *   User: `root`
        *   Password: ` ` (prázdné) nebo `root`
3.  **Nastavení v projektu**:
    *   Otevřete soubor `event_reservation_system/config.json`.
    *   Upravte sekci `"database"` podle vašich údajů. Příklad pro XAMPP/Localhost:
        ```json
        "database": {
            "host": "localhost",
            "user": "root",
            "password": "", 
            "database": "event_system_db"
        }
        ```
        *(Poznámka: Položku "database" neměňte, skript si ji vytvoří sám.)*

## 2. Instalace a Příprava Prostředí

Otevřete příkazový řádek (CMD nebo PowerShell) ve složce s projektem.

1.  **Nainstalujte potřebné knihovny**:
    ```bash
    py -m pip install flask mysql-connector-python
    ```
    *(Pokud příkaz `py` nefunguje, zkuste `python` nebo `python3`)*

2.  **Inicializace Databáze**:
    Tento krok vytvoří potřebné tabulky a pohledy ve vaší databázi.
    ```bash
    py event_reservation_system/init_db.py
    ```
    *Počkejte na výpis: "Database initialized successfully."*

## 3. Spuštění Aplikace

1.  **Spusťte webový server**:
    ```bash
    py event_reservation_system/app.py
    ```
2.  **Otevřete aplikaci**:
    *   Otevřete webový prohlížeč (Chrome, Firefox, Edge).
    *   Přejděte na adresu: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 4. Použití Aplikace

*   **Zákazník**: Můžete prohlížet akce na úvodní stránce. Pro rezervaci se přihlaste jako `customer@test.com` (heslo libovolné).
*   **Administrátor**: Přihlaste se jako `admin@test.com`.
    *   Adrese: [http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin)
    *   Zde můžete přidávat akce nebo importovat data ze souboru JSON.

## Řešení problémů

*   **Chyba "Unknown MySQL server host"**: Zkontrolujte, zda máte v `config.json` správně `localhost`.
*   **Chyba "Access denied"**: Zkontrolujte uživatelské jméno a heslo v `config.json`.
*   **Chyba "Module not found"**: Zopakujte krok instalace knihoven (`pip install ...`).
