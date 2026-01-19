# Uživatelská Příručka

Tato příručka slouží koncovým uživatelům aplikace EventHub.

## Role v Systému

Systém rozlišuje dvě základní role:
1.  **Zákazník (Customer)**: Může prohlížet akce a nakupovat vstupenky.
2.  **Administrátor (Admin)**: Může spravovat obsah aplikace, přidávat akce a vidět reporty.

---

## Pro Zákazníky

### 1. Prohlížení Akcí
Hned po příchodu na domovskou stránku vidíte seznam **nadcházejících akcí**. U každé akce vidíte:
*   Název a datum.
*   Místo konání.
*   Cenu vstupenky.

### 2. Rezervace Vstupenek
Pro nákup musíte být přihlášeni.
1.  V menu klikněte na **Login**.
2.  Přihlaste se jako zákazník (ve výchozím nastavení email: `customer@test.com`).
3.  Vyberte si akci a klikněte na **Detail**.
4.  Zadejte počet vstupenek a potvrďte rezervaci.

---

## Pro Administrátory

### 1. Přihlášení do Administrace
1.  V menu klikněte na **Login**.
2.  Přihlaste se administrátorským emailem (výchozí: `admin@test.com`).
3.  Budete přesměrováni na **Admin Dashboard**.

### 2. Vytvoření Nové Akce
Na nástěnce (Dashboardu) vyplňte formulář *Create New Event*:
*   **Venue**: Vyberte místo z nabídky.
*   **Title**: Název akce.
*   **Description**: Popis.
*   **Start Time**: Datum a čas (formát RRRR-MM-DD HH:MM).
*   **Base Price**: Cena za lístek.

Kliknutím na tlačítko akci vytvoříte.

### 3. Import Dat
Pokud máte data v souboru JSON, můžete je hromadně nahrát v sekci *Import Data*.
*   Vyberte soubor `.json`.
*   Potvrďte nahrání.
*   Systém vás informuje o počtu importovaných položek a případných chybách.

### 4. Reporty Tržeb
V menu klikněte na **Reporty**. Uvidíte tabulku, která ukazuje:
*   Název akce.
*   Celkový počet prodaných lístků.
*   Celkovou tržbu (Revenue).

---

## Testovací Účty (Demo Data)

Pokud jste použili přiložená demo data (`init_db.py`), můžete použít tyto účty:

| Role | Email | Heslo |
| :--- | :--- | :--- |
| **Admin** | `admin@test.com` | (libovolné v demu) |
| **Zákazník** | `customer@test.com` | (libovolné v demu) |
