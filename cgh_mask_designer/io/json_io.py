from ..core.settings import Settings

def export_settings(path: str, settings: Settings):
    with open(path, "w") as f: f.write(settings.to_json())

def import_settings(path: str) -> Settings:
    with open(path, "r") as f: return Settings.from_json(f.read())
