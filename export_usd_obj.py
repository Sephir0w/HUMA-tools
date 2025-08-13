import maya.cmds as cmds
import os
import shutil

# Obtenir le chemin de la scène actuelle
scene_path = cmds.file(query=True, sceneName=True)

# Définir la chaîne à remplacer et la nouvelle chaîne
scene_part = scene_path.split("/")  # Divise le chemin en liste

# Extraire dynamiquement la partie "asset type" (par exemple "02_prop")
asset_type = scene_part[-6] if len(scene_part) >= 6 else "default"  # Assurez-vous qu'il y a assez d'éléments

# Extraire l'ancien chemin (en tenant compte du fait que la liste peut ne pas être assez longue)
old_path = "/".join(scene_part[5:-1]) if len(scene_part) >= 6 else ""

keep_path = scene_part[0:4]

# Extraire le nom de l'asset depuis le chemin
current_asset = os.path.splitext(os.path.basename(scene_path))[0]

print(f"Asset type: {asset_type}")

# Créer un nouveau chemin avec la partie dynamique "asset_type"
new_path = f"HUMA/09_publish/asset/{asset_type}/geo"  # Utiliser la syntaxe f-string pour insérer asset_type

# Remplacer l'ancien chemin par le nouveau chemin dans la scène, si old_path n'est pas vide
if old_path:
    new_scene_path = scene_path.replace(old_path, new_path)
else:
    new_scene_path = scene_path

# Créer un nouveau chemin pour le fichier USD (en utilisant os.path.join)
scene_name = os.path.splitext(os.path.basename(scene_path))[0]
base_name = "_".join(scene_name.split("_")[:-2])  # Enlève la partie "E_XXX"
new_scene_path = os.path.join(os.path.dirname(new_scene_path), base_name + "_P"+".usd")

# Assurez-vous d'utiliser des barres obliques normales
new_scene_path = new_scene_path.replace("\\", "/")

# Afficher le nouveau chemin généré
print("Nouveau chemin généré :", new_scene_path)

# Vérifier si le répertoire existe, sinon le créer
publish_dir = os.path.dirname(new_scene_path)
if not os.path.exists(publish_dir):
    os.makedirs(publish_dir)

# Vérifier si le fichier existe déjà
if os.path.exists(new_scene_path):
    print(f"Le fichier {new_scene_path} existe déjà.")
    
    # Créer un dossier 'old' s'il n'existe pas déjà
    old_folder = os.path.join(os.path.dirname(new_scene_path), 'old')
    if not os.path.exists(old_folder):
        os.makedirs(old_folder)
    
    # Déplacer le fichier existant dans le dossier 'old'
    old_file_path = os.path.join(old_folder, os.path.basename(new_scene_path))
    
    # Si un fichier avec le même nom existe déjà dans 'old', renommer ce fichier
    counter = 1
    while os.path.exists(old_file_path):
        old_file_path = os.path.join(old_folder, f"{os.path.splitext(os.path.basename(new_scene_path))[0]}_{counter}.usd")
        counter += 1

    # Déplacer ou copier le fichier existant
    shutil.move(new_scene_path, old_file_path)  # Utilisation de move pour déplacer le fichier
    print(f"Fichier existant déplacé vers : {old_file_path}")
else:
    print(f"Le fichier {new_scene_path} n'existe pas. Exportation en cours.")

# Construire les options MEL pour l'export USD
export_options = "exportBlendShapes=0;animation=0;exportVisibility=1;mergeTransformAndShape=1;stripNamespaces=0;worldspace=0;defaultUSDFormat=usdc;"

# Exporter la scène en fichier USD
cmds.file(new_scene_path, force=True, type="USD Export", options=export_options, exportSelected=True)
print(f"Exportation USD réussie : {new_scene_path}")
