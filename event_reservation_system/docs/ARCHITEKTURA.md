# Technická Dokumentace a Architektura

Tento dokument popisuje vnitřní fungování systému EventHub. Je určen pro vývojáře, kteří chtějí projekt upravit nebo pochopit jeho strukturu.

## 1. Architektura Aplikace

Aplikace je postavena na frameworku **Flask** a dodržuje **Three-Layer Architecture** (Třívrstvou architekturu) pro oddělení odpovědností.

### Vrstvy:
1.  **Prezentační Vrstva (Flask Routes & Templates)**
    *   Soubor: `app.py`
    *   Složka: `templates/`
    *   Stará se o HTTP požadavky, renderování HTML stránek a komunikaci s uživatelem.
    *   Volá metody ze servisní vrstvy nebo repozitářů.
2.  **Servisní Vrstva (Business Logic)**
    *   Soubor: `services.py`
    *   Obsahuje složitější logiku, která nepatří do databáze ani do controlleru (např. validace dostupnosti vstupenek při nákupu, výpočet ceny).
3.  **Datová Vrstva (Repositories & Database)**
    *   Soubory: `repositories.py`, `database.py`, `schema.sql`
    *   Poskytuje rozhraní pro práci s daty (CRUD operace). Odstiňuje zbytek aplikace od SQL dotazů.

## 2. Struktura Kódu

*   `app.py`: Hlavní soubor aplikace. Definuje endpointy (`/`, `/login`, `/admin` atd.).
*   `database.py`: Třída `Database` pro správu připojení k MySQL (Singleton pattern pro připojení).
*   `repositories.py`: Třídy (`EventRepository`, `UserRepository`, ...) pro přímou manipulaci s tabulkami.
*   `services.py`: Třída `BookingService` obaluje logiku vytváření rezervace (transakce, validace).
*   `importer.py`: Logika pro import dat z JSON souboru.
*   `init_db.py`: Skript pro inicializaci databáze.

## 3. Databázové Schéma

Databáze `event_system_db` obsahuje následující entity:

### Tabulky
*   **users**: Uživatelé systému (Admin/Customer). Obsahuje email, hash hesla, roli.
*   **venues**: Místa konání akcí (Název, Adresa, Kapacita).
*   **events**: Samotné události. Provázané s `venues`.
*   **bookings**: Hlavní záznam o rezervaci. Provázáno s `users`.
*   **booking_items**: Položky rezervace (M:N vazba mezi Bookings a Events). Uchovává počet lístků a cenu v době nákupu.

### Views (Pohledy)
*   **v_upcoming_events**: Zjednodušený pohled pro výpis aktivních budoucích akcí (spojuje `events` a `venues`).
*   **v_revenue_report**: Agregovaná data pro admina. Počítá prodané lístky a tržby pro každou akci.

## 4. Klíčové Procesy

### Vytvoření Rezervace (`BookingService`)
1.  Uživatel odešle požadavek na rezervaci.
2.  `BookingService` ověří existenci akce.
3.  Vypočítá se celková cena.
4.  V jedné databázové transakci se vytvoří záznam v `bookings` a položky v `booking_items`. Obojí se uloží, nebo se v případě chyby vše vrátí zpět (rollback).

### Import Dat (`importer.py`)
1.  Admin nahraje JSON soubor.
2.  Třída `DataImporter` parsuje JSON.
3.  Používá se konstrukt `INSERT IGNORE` nebo kontrola existence, aby se zabránilo duplicitám (např. u emailů).
