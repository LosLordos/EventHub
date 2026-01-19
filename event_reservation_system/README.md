# EventHub - Rezervační Systém

EventHub je jednoduchá, ale robustní webová aplikace pro správu a rezervaci vstupenek na různé kulturní a společenské akce. Umožňuje uživatelům prohlížet nadcházející události a rezervovat si vstupenky, zatímco administrátoři mohou spravovat akce, venues a sledovat statistiky prodeje.

## 🚀 Rychlý Přehled

- **Jazyk**: Python 3
- **Framework**: Flask (Web), MySQL Connector (Databáze)
- **Databáze**: MySQL
- **Frontend**: HTML5, CSS3 (šablony Jinja2)
- **Architektura**: 3-vrstvá (Routes -> Services -> Repositories)

## 📂 Dokumentace

Kompletní dokumentace je k dispozici ve složce `docs/`:

1.  [**Instalace a Spuštění**](docs/INSTALACE.md) - Podrobný návod jak zprovoznit aplikaci lokálně.
2.  [**Uživatelská Příručka**](docs/UZIVATELSKA_PRIRUCKA.md) - Návod pro zákazníky i administrátory jak aplikaci používat.
3.  [**Technická Dokumentace (Architektura)**](docs/ARCHITEKTURA.md) - Popis databáze, kódu a vnitřní logiky systému.

## ✨ Klíčové Funkce

*   **Pro Zákazníky**:
    *   Výpis aktuálních akcí.
    *   Detail akce s informacemi.
    *   Rezervace vstupenek (vyžadováno přihlášení).
*   **Pro Administrátory**:
    *   Vytváření nových akcí.
    *   Import dat (uživatelů a akcí) z JSON souboru.
    *   Přehled tržeb a reporty.

## 🛠 Požadavky

*   Python 3.8+
*   MySQL Server (např. přes XAMPP nebo samostatně)
*   Knihovny: `flask`, `mysql-connector-python`

---
*Vytvořeno pro školní projekt EventHub.*
