import os
import re

def standardize_assets():
    base_dir = os.path.normpath("assets/sprites")
    
    race_map = {
        "H": "humano",
        "A": "anao",
        "E": "elfo",
        "D": "draconato",
        "O": "meio_orc",
        "T": "tiefling",
        "HL": "halfling"
    }

    enemy_prefixes = ["CS.", "L.", "P.", "SC."]

    for root, dirs, files in os.walk(base_dir):
        for filename in files:
            if not filename.lower().endswith(".png"):
                continue
            
            orig_path = os.path.join(root, filename)
            new_name = filename.replace(".png", "").replace(".PNG", "")
            
            # Remove "Icone" (case-insensitive)
            new_name = re.sub(r'(?i)icone\s*', '', new_name)
            
            # Map enemy prefixes out
            for ep in enemy_prefixes:
                if new_name.startswith(ep):
                    new_name = new_name[len(ep):]
            
            new_name = new_name.strip()
            
            # Map hero prefixes
            for prefix, race_name in race_map.items():
                if new_name.startswith(f"{prefix}."):
                    new_name = new_name[len(prefix)+1:].strip()
                    new_name = f"{race_name}_{new_name}"
                    break
            
            # Replace spaces with underscores and lower case
            new_name = new_name.lower().replace(" ", "_")
            
            # Map genders: "_m" -> "_male", "_f" -> "_female"
            if new_name.endswith("_m"):
                new_name = new_name[:-2] + "_male"
            elif new_name.endswith("_f"):
                new_name = new_name[:-2] + "_female"
            elif new_name.endswith("_m-"):
                new_name = new_name[:-3] + "_male"
                
            # Handle some typos in original files (e.g., Guereeiro)
            new_name = new_name.replace("guereeiro", "guerreiro")
            
            new_filename = f"{new_name}.png"
            new_path = os.path.join(root, new_filename)
            
            if orig_path != new_path:
                print(f"Renomeando: {orig_path} -> {new_path}")
                os.rename(orig_path, new_path)

if __name__ == "__main__":
    standardize_assets()
