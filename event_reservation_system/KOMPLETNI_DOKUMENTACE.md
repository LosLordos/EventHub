# Kompletní Dokumentace Projektu EventHub

**Název projektu:** EventHub
**Autor:** (Doplňte jméno)
**Typ projektu:** Webová aplikace
**Použité technologie:** Python, Flask, MySQL, Jinja2
**Cílová platforma:** Web (Cross-platform)
**Účel projektu:** Rezervační systém pro kulturní a společenské akce.

---

## 1️⃣ Úvod

### Stručný popis projektu
EventHub je webová aplikace, která umožňuje uživatelům prohlížet seznam kulturních akcí a rezervovat si na ně vstupenky. Systém zároveň poskytuje administrátorské rozhraní pro správu akcí, míst konání (venues) a sledování prodejů.

### Motivace a cíl aplikace
Cílem projektu bylo vytvořit robustní, ale přehledný systém, který demonstruje práci s relační databází v prostředí webové aplikace. Důraz byl kladen na správné rozvrstvení architektury, transakční zpracování objednávek a oddělení datové logiky od prezentační vrstvy.

### Pro koho je aplikace určena
*   **Návštěvníci (Zákazníci):** Lidé hledající kulturu, kteří si chtějí snadno rezervovat místo.
*   **Organizátoři (Administrátoři):** Správci systému, kteří potřebují evidovat akce a vyhodnocovat tržby.

---

## 2️⃣ Analýza požadavků

### Funkční požadavky
1.  **Veřejná část:**
    *   Zobrazení seznamu nadcházejících akcí.
    *   Detail konkrétní akce s popisem a cenou.
2.  **Autentizace:**
    *   Přihlášení uživatelů (Admin / Zákazník).
    *   Odhlášení.
3.  **Zákaznická zóna:**
    *   Rezervace vstupenek na vybranou akci (možnost zvolit počet kusů).
4.  **Administrátorská zóna:**
    *   Vytváření nových akcí (přiřazení k Venue, nastavení času a ceny).
    *   Hromadný import dat o akcích a uživatelích ze souboru JSON.
    *   Zobrazení reportu tržeb (Revenue Report).

### Nefunkční požadavky
*   **Perzistence dat:** Veškerá data musí být trvale uložena v databázi MySQL.
*   **Integrita dat:** Rezervace musí probíhat v transakci (buď se uloží vše, nebo nic).
*   **Dostupnost:** Webové rozhraní musí být dostupné přes prohlížeč.
*   **Architektura:** Kód musí být členěn do logických vrstev (Repository Pattern).

---

## 3️⃣ Architektura systému

### Celkový návrh aplikace
Aplikace je postavena na frameworku **Flask**, který obsluhuje HTTP požadavky a routování. Používá se **Three-Layer Architecture** (Třívrstvá architektura):
1.  **Presentation Layer (Flask Routes):** Přijímá vstupy od uživatele a renderuje HTML šablony (Jinja2).
2.  **Service Layer (`BookingService`):** Obsahuje business logiku (např. výpočet celkové ceny, validace).
3.  **Data Access Layer (Repositories):** Zapouzdřuje SQL dotazy a komunikaci s databází.

### Použité architektonické vzory
*   **MVC (Model-View-Controller):** Flask funguje jako Controller, Jinja2 jako View, a databázové třídy jako Model.
*   **Repository Pattern:** Třídy v `repositories.py` (`EventRepository`, `BookingRepository`) abstrahují přístup k datům.
*   **Singleton:** Třída `Database` v `database.py` zajišťuje řízené připojení k databázi.

### Struktura projektu
```text
event_reservation_system/
├── app.py              # Vstupní bod, definice rout (Controller)
├── services.py         # Business logika (Service Layer)
├── repositories.py     # SQL dotazy (Data Layer)
├── database.py         # Správa DB připojení
├── importer.py         # Logika pro import JSON
├── templates/          # HTML šablony (View)
├── schema.sql          # Definice databáze
├── init_db.py          # Inicializační skript
└── config.json         # Konfigurace
```

---

## 4️⃣ Datový model

Databáze `event_system_db` je relační (MySQL).

### Seznam tabulek a relace
1.  **`venues` (Místa konání)**
    *   PK: `id`
    *   Sloupce: `name`, `address`, `capacity`
2.  **`events` (Akce)**
    *   PK: `id`
    *   FK: `venue_id` (vazba N:1 na `venues`)
    *   Sloupce: `title`, `description`, `start_time`, `base_price`
3.  **`users` (Uživatelé)**
    *   PK: `id`
    *   Sloupce: `email`, `role` (ENUM: admin/customer), `password_hash`
4.  **`bookings` (Rezervace)**
    *   PK: `id`
    *   FK: `user_id` (vazba N:1 na `users`)
    *   Sloupce: `total_price`, `status`, `created_at`
5.  **`booking_items` (Položky rezervace)**
    *   PK: `id`
    *   FK: `booking_id` (vazba N:1 na `bookings`)
    *   FK: `event_id` (vazba N:1 na `events`)
    *   *Poznámka:* Tato tabulka realizuje vazbu M:N mezi `bookings` a `events`.

### Pohledy (Views)
*   **`v_upcoming_events`**: Spojuje `events` a `venues` pro snazší výpis na webu.
*   **`v_revenue_report`**: Agreguje data z `booking_items` a počítá celkové tržby pro jednotlivé akce.

---

## 5️⃣ Popis implementace

### Klíčové třídy a metody

#### `BookingService` (services.py)
*   **`create_booking(user_id, items)`**: Klíčová metoda.
    *   Přijímá ID uživatele a seznam položek.
    *   Pro každou položku ověří existenci akce a spočítá cenu.
    *   Volá `booking_repo.create_booking_transaction` pro atomické uložení.

#### `BookingRepository` (repositories.py)
*   **`create_booking_transaction(user_id, items, total_price)`**:
    *   Zahájí databázovou transakci (`START TRANSACTION`).
    *   Vloží záznam do `bookings`.
    *   Vloží záznamy do `booking_items`.
    *   Pokud vše projde, provede `COMMIT`. Při chybě provede `ROLLBACK`.

#### `DataImporter` (importer.py)
*   **`import_from_json(json_content)`**:
    *   Parsuje vstupní JSON řetězec.
    *   Iteruje přes eventy a uživatele a vkládá je do DB.
    *   Vrací statistiku úspěchu a případné chyby.

### Zpracování chyb
Aplikace používá `try-except` bloky, zejména při práci s databází a importu. Chyby jsou zachyceny a uživateli je zobrazena srozumitelná Flash zpráva (např. "Import failed").

---

## 6️⃣ Uživatelská dokumentace

### Jak aplikaci nainstalovat
1.  Nainstalujte Python 3.8+ a MySQL Server.
2.  Nainstalujte závislosti:
    ```bash
    pip install flask mysql-connector-python
    ```
3.  Vytvořte strukturu databáze:
    ```bash
    python event_reservation_system/init_db.py
    ```

### Jak ji spustit
Spusťte webový server příkazem:
```bash
python event_reservation_system/app.py
```
Aplikace poběží na adrese `http://127.0.0.1:5000`.

### Popis ovládání
1.  **Rezervace (Jako Zákazník)**:
    *   Přihlaste se (Email: `customer@test.com`).
    *   Vyberte akci na úvodní stránce.
    *   V detailu zadejte počet lístků a potvrďte `Book Ticket`.
2.  **Správa (Jako Admin)**:
    *   Přihlaste se (Email: `admin@test.com`).
    *   Přejděte na `/admin`.
    *   Zde můžete přidávat akce přes formulář nebo importovat data.
    *   Záložka "Report" zobrazí tržby.

---

## 7️⃣ Konfigurace

Konfigurace je uložena v souboru `config.json` v kořenu aplikace.

**Příklad `config.json`:**
```json
{
    "database": {
        "host": "localhost",
        "user": "root",
        "password": "", 
        "database": "event_system_db"
    },
    "app": {
        "secret_key": "tajny_klic_pro_sessions"
    }
}
```
*   **database**: Přihlašovací údaje k MySQL serveru.
*   **app.secret_key**: Klíč pro šifrování session cookies (nutné pro Flask).

---

## 8️⃣ Import a export dat

Systém podporuje import dat ve formátu **JSON**.

### Struktura importního souboru
```json
{
    "events": [
        {
            "venue_id": 1,
            "title": "Koncert",
            "description": "...",
            "start_time": "2024-12-01 20:00:00",
            "base_price": 500
        }
    ],
    "users": [
        {
            "email": "novy@test.com",
            "role": "customer",
            "display_name": "Nový Uživatel"
        }
    ]
}
```
### Postup importu
1.  Přihlaste se jako Admin.
2.  Na Dashboardu vyhledejte sekci "Import Data".
3.  Vyberte JSON soubor z disku a odešlete formulář.

---

## 9️⃣ Testování

Během vývoje byly ověřovány tyto scénáře (viz soubor `test_cases.md`):

1.  **Instalace a Setup**: Ověření, že `init_db.py` správně vytvoří tabulky.
2.  **Rezervace (Happy Path)**: Uživatel se přihlásí, vybere akci, objedná 2 lístky -> systém vytvoří záznamy v `bookings` a `booking_items`.
3.  **Transakční integrita**: (Simulováno) Pokud selže vložení položky, nevytvoří se ani hlavička objednávky.
4.  **Admin Import**: Ověření, že systém přijme validní JSON a odmítne nevalidní formát.

---

## 🔟 Bezpečnost a omezení

### Zabezpečení dat
*   **SQL Injection**: Použití parametrizovaných dotazů v `mysql.connector` zabraňuje této zranitelnosti.
*   **Hesla**: V databázi je připraven sloupec `password_hash`.
*   **Sessions**: Flask sessions jsou podepsané tajným klíčem.

### Známá omezení
*   **Ověřování hesel**: Pro účely demonstrace je kontrola hesla zjednodušena (stačí zadat správný email). V produkční verzi by bylo nutné implementovat porovnávání hashů (např. pomocí `bcrypt`).
*   **Kapacita v reálném čase**: Kontrola kapacity sálu je implementována, ale při vysoké zátěži (race condition) by mohlo dojít k mírnému přeplnění bez pokročilého zamykání řádků.

---

## 1️⃣1️⃣ Závěr

### Shrnutí projektu
EventHub úspěšně splnil zadání vytvořit funkční rezervační systém. Aplikace demonstruje schopnost propojit Python backend s relační databází, spravovat uživatele a provádět transakční operace.

### Možnosti budoucího rozšíření
*   **Platební brána**: Integrace Stripe nebo PayPal pro reálné placení.
*   **Generování vstupenek**: Automatické odeslání PDF vstupenky na email po rezervaci.
*   **Interaktivní plánek**: Výběr konkrétních sedadel v sále.
