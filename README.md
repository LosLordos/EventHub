

## 1. Požadavky (Prerequisites)

Než začnete, ujistěte se, že máte nainstalované následující:

1.  **Python** (verze 3.8 nebo novější)
    *   Ke stažení na [python.org](https://www.python.org/downloads/).
    *   **DŮLEŽITÉ:** Při instalaci zaškrtněte možnost **"Add Python to PATH"**.
2.  **MySQL Server**
    *   Může být součástí balíčku **XAMPP** (doporučeno pro začátečníky) nebo samostatná instalace MySQL Community Server.
    *   Ke stažení XAMPP: [apachefriends.org](https://www.apachefriends.org/download.html).

---

## 2. Příprava databáze

Aplikace potřebuje běžící MySQL databázi.

1.  **Spusťte MySQL server**.
    *   Pokud máte **XAMPP**, otevřete XAMPP Control Panel a klikněte na **Start** u modulu **MySQL**.
2.  **Připravte si přihlašovací údaje**.
    *   Výchozí údaje pro XAMPP bývají:
        *   **Host:** `localhost`
        *   **Uživatel:** `root`
        *   **Heslo:** (prázdné)
    *   Pokud máte vlastní instalaci MySQL, použijte údaje, které jste zadali při instalaci.

3.  **Nastavení konfigurace v projektu**:
    *   Otevřete soubor `config.json` v textovém editoru (např. Notepad).
    *   Upravte sekci `"database"` podle vašich údajů:

    ```json
    "database": {
        "host": "localhost",
        "user": "root",
        "password": "", 
        "database": "event_system_db"
    }
    ```
    *(Poznámka: Název databáze `event_system_db` nechte beze změny, skript si ji vytvoří automaticky.)*

---

## 3. Instalace projektu a závislostí

Doporučujeme použít virtuální prostředí (venv), aby se knihovny nemíchaly s ostatními projekty v systému.

Otevřete **PowerShell** (nebo Příkazový řádek) ve složce s projektem (`event_reservation_system`) a postupujte následovně:

1.  **Vytvoření virtuálního prostředí:**
    ```powershell
    python -m venv venv
    ```
    *(Tento příkaz vytvoří složku `venv` v adresáři projektu.)*

2.  **Aktivace virtuálního prostředí:**
    *   Pro **PowerShell**:
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
        *(Pokud dostanete chybu o zákazu skriptů, spusťte tento příkaz pro dočasné povolení: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`, a poté zkuste aktivaci znovu.)*
    *   Pro **Příkazový řádek (CMD)**:
        ```cmd
        venv\Scripts\activate.bat
        ```
    *   *Po úspěšné aktivaci uvidíte na začátku řádku závorku `(venv)`.*

3.  **Instalace knihoven:**
    ```powershell
    pip install -r requirements.txt
    ```

---

## 4. Inicializace databáze

Nyní, když máme knihovny a běžící MySQL server, vytvoříme strukturu databáze.

Ujistěte se, že máte stále aktivní virtuální prostředí `(venv)` a spusťte:

```powershell
python init_db.py
```

Pokud vše proběhne v pořádku, uvidíte výpis:
`Database initialized successfully.`

---

## 5. Spuštění aplikace

Aplikaci spustíte následujícím příkazem:

```powershell
python app.py
```

Po spuštění byste měli vidět výpis podobný tomuto:
` * Running on http://127.0.0.1:5000`

Otevřete svůj webový prohlížeč a přejděte na adresu:
**[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 6. Používání aplikace

*   **Zákazník:**
    *   Pro testování rezervací se přihlaste jako zákazník.
    *   Email: `customer@test.com` (nebo jiný vytvořený v importu/databázi)
    *   Heslo: (aplikace v demo režimu kontroluje pouze existenci emailu, heslo není ověřováno, ale v reálu by bylo).
*   **Administrátor:**
    *   Pro správu akcí přejděte na `/admin` nebo se přihlaste.
    *   Email: `admin@test.com`

---

## Řešení problémů (Troubleshooting)

*   **Chyba `Module not found`**: Nemáte aktivní virtuální prostředí nebo jste nenainstalovali závislosti. Zkontrolujte, zda vidíte `(venv)` a zkuste znovu `pip install -r requirements.txt`.
*   **Chyba připojení k databázi (Access denied / Unknown host)**: Zkontrolujte údaje v `config.json`. Ujistěte se, že MySQL server běží.
*   **Chyba "Skript nelze načíst..." v PowerShellu**: Viz bod 3.2 – je potřeba povolit spouštění skriptů ve Windows.
