# EventHub – správa akcí, vstupenek, zákazníků, plateb, míst

## Co to je
Webová aplikace (FastAPI) nad MS SQL Server pro správu akcí, prodej vstupenek s hlídáním kapacity, reporty (návštěvnost, tržby) a importy.

## Jak to spustit
1) Nainstaluj závislosti: `pip install -r requirements.txt`
2) Vytvoř DB (spusť `/db/ddl.sql` a volitelně `/db/seed.sql`)
3) Nastav `config.yaml` (connection string)
4) Spusť: `uvicorn src.app.main:app --reload`

## Co je D1
Použití vlastního **Repository patternu**: datová vrstva je oddělená od business logiky a UI/API.
