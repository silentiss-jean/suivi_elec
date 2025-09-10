import os

def load_env(path):
    print(f"📂 Chargement du fichier .env depuis : {path}")
    if not os.path.exists(path):
        print("❌ Fichier .env introuvable")
        return False
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value
                print(f"🔑 {key} = {value[:40]}{'...' if len(value) > 40 else ''}")
    return True