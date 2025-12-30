from dataclasses import dataclass
import yaml

@dataclass(frozen=True)
class Settings:
    connection_string: str
    mode: str
    import_max_rows: int

def load_settings(path: str = "config.yaml") -> Settings:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    try:
        cs = data["db"]["connection_string"]
        mode = data.get("app", {}).get("mode", "dev")
        max_rows = int(data.get("imports", {}).get("max_rows", 5000))
        if max_rows <= 0:
            raise ValueError("imports.max_rows musí být > 0")
        return Settings(connection_string=cs, mode=mode, import_max_rows=max_rows)
    except KeyError as e:
        raise RuntimeError(f"Chybí povinná hodnota v configu: {e}") from e
