import maya.cmds as cmds
import os
import shutil

# Obtenir le chemin de la scène actuelle
scene_path = cmds.file(query=True, sceneName=True)

# Extraire le nom de l'asset depuis le chemin
scene_name = os.path.splitext(os.path.basename(scene_path))[0]

# Demander à l'utilisateur de saisir le base_name via une fenêtre pop-up
result = cmds.promptDialog(
    title='Base Name Input',
    message='Enter Base Name:',
    button=['OK', 'Cancel'],
    defaultButton='OK',
    cancelButton='Cancel',
    dismissString='Cancel')

if result == 'OK':
    basename = cmds.promptDialog(query=True, text=True)
else:
    print("Action annulée par l'utilisateur.")


assetName = "_".join(scene_name.split("_")[:-4]) + "_" + basename 
# Obtenir les éléments de chemin et définir les variables nécessaires
scene_part = scene_path.split("/")
asset_type = scene_part[-6] if len(scene_part) >= 6 else "default"
old_path = "/".join(scene_part[5:-1]) if len(scene_part) >= 6 else ""
new_path = f"HUMA/09_publish/asset/{asset_type}/geo"

# Remplacer l'ancien chemin par le nouveau chemin dans la scène
new_scene_path = scene_path.replace(old_path, new_path) if old_path else scene_path

# Créer le nouveau chemin pour le fichier USD
new_scene_path = os.path.join(os.path.dirname(new_scene_path), assetName + "_P" + ".usd")
new_scene_path = new_scene_path.replace("\\", "/")

# Afficher le nouveau chemin généré
print("Nouveau chemin généré :", new_scene_path)

# Vérifier si le répertoire existe, sinon le créer
publish_dir = os.path.dirname(new_scene_path)
if not os.path.exists(publish_dir):
    os.makedirs(publish_dir)

# Vérifier et gérer l'existence du fichier
if os.path.exists(new_scene_path):
    print(f"Le fichier {new_scene_path} existe déjà.")
    old_folder = os.path.join(os.path.dirname(new_scene_path), 'old')
    if not os.path.exists(old_folder):
        os.makedirs(old_folder)
    old_file_path = os.path.join(old_folder, os.path.basename(new_scene_path))
    counter = 1
    while os.path.exists(old_file_path):
        old_file_path = os.path.join(old_folder, f"{os.path.splitext(os.path.basename(new_scene_path))[0]}_{counter}.usd")
        counter += 1
    shutil.move(new_scene_path, old_file_path)
    print(f"Fichier existant déplacé vers : {old_file_path}")
else:
    print(f"Le fichier {new_scene_path} n'existe pas. Exportation en cours.")

# Exporter la scène en fichier USD
export_options = "exportBlendShapes=0;animation=0;exportVisibility=1;mergeTransformAndShape=1;stripNamespaces=0;worldspace=0;defaultUSDFormat=usdc;"
cmds.file(new_scene_path, force=True, type="USD Export", options=export_options, exportSelected=True)
print(f"Exportation USD réussie : {new_scene_path}")
