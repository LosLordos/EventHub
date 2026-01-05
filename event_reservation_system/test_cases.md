# Testovací scénáře - Rezervační systém akcí

## 1. Testovací scénář: Instalace a Spuštění (Setup)
**Cíl**: Ověřit, že aplikace lze nainstalovat, inicializovat databázi a spustit.

**Kroky**:
1.  **Konfigurace**:
    *   Otevřete `config.json`.
    *   Nastavte `host`, `user`, `password` podle vaší MySQL databáze.
2.  **Instalace závislostí**:
    *   Spusťte příkaz: `pip install flask mysql-connector-python`
3.  **Inicializace Databáze**:
    *   Spusťte skript: `python event_reservation_system/init_db.py`
    *   **Očekávaný výsledek**: Výpis "Database initialized successfully."
    *   **Ověřte v MySQL Workbench**: Musí existovat databáze `event_system_db` s tabulkami `users`, `events`, `bookings`, `venues`, `booking_items` a pohledy `v_upcoming_events`.
4.  **Spuštění Aplikace**:
    *   Spusťte: `python event_reservation_system/app.py`
    *   Otevřete prohlížeč na `http://127.0.0.1:5000`.
    *   **Očekávaný výsledek**: Zobrazí se úvodní stránka se seznamem akcí.

## 2. Testovací scénář: Rezervace Vstupenek (Transakce)
**Cíl**: Ověřit funkčnost M:N vazby a transakčního zpracování objednávky.

**Kroky**:
1.  **Přihlášení**:
    *   Jděte na `/login`.
    *   Zadejte email: `customer@test.com` (heslo libovolné).
    *   **Očekávaný výsledek**: Přesměrování na domovskou stránku s uvítací zprávou.
2.  **Výběr Akce**:
    *   Klikněte na "View Details" u libovolné akce.
3.  **Vytvoření Objednávky**:
    *   Zadejte počet vstupenek (např. 2).
    *   Klikněte na "Confirm Booking".
    *   **Očekávaný výsledek**: Zpráva "Booking successful!".
4.  **Ověření v Databázi**:
    *   Podívejte se do tabulky `bookings`. Musí existovat nový záznam pro uživatele.
    *   Podívejte se do tabulky `booking_items`. Musí existovat záznam propojující `booking_id` a `event_id` s `quantity=2`.
    *   *Poznámka*: Toto potvrzuje, že transakce uložila data do obou tabulek.

## 3. Testovací scénář: Admin a Import Dat
**Cíl**: Ověřit funkci importu (JSON) a reportingu.

**Kroky**:
1.  **Přihlášení jako Admin**:
    *   Jděte na `/login` -> zadejte `admin@test.com`.
2.  **Import Dat**:
    *   Jděte na "Admin" v menu.
    *   V sekci "Import Data" vyberte soubor `data_import.json` (Vytvořte testovací soubor s klíči `events` a `users`).
    *   Klikněte "Import Data".
    *   **Očekávaný výsledek**: Zpráva o počtu importovaných záznamů.
3.  **Kontrola Reportu**:
    *   Klikněte na "View Revenue Report".
    *   **Očekávaný výsledek**: Tabulka zobrazující akce, počty prodaných lístků a tržby (data z pohledu `v_revenue_report`).
    *   Zkontrolujte, že se započítala i rezervace z předchozího scénáře.
