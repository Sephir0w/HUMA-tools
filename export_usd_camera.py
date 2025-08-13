from PySide2 import QtWidgets
import maya.cmds as cmds
import os
import shutil

class UsdExportUI(QtWidgets.QDialog):
    def __init__(self):
        super(UsdExportUI, self).__init__()

        # Layout principal
        self.setWindowTitle("Export USD")
        self.setGeometry(300, 300, 300, 250)
        layout = QtWidgets.QVBoxLayout()

        # Champs pour frame range
        self.assetName_label = QtWidgets.QLabel("Asset Name:")
        layout.addWidget(self.assetName_label)
        self.assetName = QtWidgets.QLineEdit()
        self.assetName.setPlaceholderText("assetName")
        layout.addWidget(self.assetName)

        # Champs pour frame range
        self.frame_in_label = QtWidgets.QLabel("Frame In:")
        layout.addWidget(self.frame_in_label)
        self.frame_in = QtWidgets.QLineEdit()
        self.frame_in.setPlaceholderText("Frame In")
        layout.addWidget(self.frame_in)

        self.frame_out_label = QtWidgets.QLabel("Frame Out:")
        layout.addWidget(self.frame_out_label)
        self.frame_out = QtWidgets.QLineEdit()
        self.frame_out.setPlaceholderText("Frame Out")
        layout.addWidget(self.frame_out)

        # Bouton Exporter
        self.export_button = QtWidgets.QPushButton("Exporter")
        self.export_button.clicked.connect(self.export_usd)
        layout.addWidget(self.export_button)

        # Configurer le layout
        self.setLayout(layout)


    def export_usd(self):

        # Récupérer les valeurs de l'interface
        assetName = self.assetName.text()
        frame_in = self.frame_in.text()
        frame_out = self.frame_out.text()
        print(frame_in)
        print(frame_out)       
        # Vérifier que les valeurs de frame_in et frame_out sont valides
        try:
            frame_in = int(frame_in)
            frame_out = int(frame_out)
        except ValueError:
            cmds.error("Les valeurs Frame In et Frame Out doivent être des entiers valides.")

        # Exemple de chemin de scène
        scene_path = cmds.file(query=True, sceneName=True)
        print(scene_path)
        scene_part = scene_path.split("/")  # Divise le chemin en liste
        print(scene_part)
        # Extraire dynamiquement la partie "sequenceName" (par exemple "seq010")
        sequenceName = scene_part[-5] if len(scene_part) >= 5 else "default"  # Assurez-vous qu'il y a assez d'éléments
        print(sequenceName)
        shotName = scene_part[-4] if len(scene_part) >= 4 else "default"  # Assurez-vous qu'il y a assez d'éléments
        print(shotName)


        if scene_path:
            print("Chemin de la scène actuelle :", scene_path)

            # Uniformiser les barres obliques dans le chemin
            scene_path = scene_path.replace("\\", "/")
            print("Chemin après remplacement des barres obliques inverses :", scene_path)


            # Définir la chaîne à remplacer et la nouvelle chaîne
            old_path = "/".join(scene_part[5:-1]) if len(scene_part) >= 6 else ""  # Ajusté pour correspondre à la structure exacte
            print(old_path)

            new_path = f"HUMA/09_publish/shot/{sequenceName}/{shotName}/camera"  # Utiliser la syntaxe f-string pour insérer asset_type

            # Afficher les valeurs pour débogage
            print(f"Ancien chemin à remplacer : {old_path}")
            print(f"Chemin de la scène avant remplacement : {scene_path}")

            # Vérifier si la chaîne à remplacer existe dans le chemin source
            if old_path in scene_path:  # Comparaison exacte
                # Remplacer l'ancienne chaîne par la nouvelle
                new_scene_path = scene_path.replace(old_path, new_path)

                # Créer le nouveau chemin avec le nom de base sans la version (E_003)
                scene_name = os.path.splitext(os.path.basename(scene_path))[0]
                base_name = "_".join(scene_name.split("_")[:-2])  # Enlève la partie "E_003"
                new_scene_path = os.path.join(os.path.dirname(new_scene_path), base_name + "_" + assetName + ".usd")

                # Assurez-vous d'utiliser des barres obliques normales
                new_scene_path = new_scene_path.replace("\\", "/")

                # Afficher le nouveau chemin généré
                print("Nouveau chemin généré :", new_scene_path)

                # Vérifier si le répertoire existe, sinon le créer
                publish_dir  = os.path.dirname(new_scene_path)
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

                # Construire les options MEL pour l'export USD
                export_options = f"exportBlendShapes=1;exportVisibility=1;animation=1;startTime={frame_in};endTime={frame_out};mergeTransformAndShape=1;stripNamespaces=0;worldspace=0;defaultUSDFormat=usdc;"


                # Exporter la scène en fichier USD
                cmds.file(new_scene_path, force=True, type="USD Export", options=export_options, exportSelected=True)
                print(f"Exportation USD réussie : {new_scene_path}")
            else:
                print(f"Erreur : Le chemin source ne contient pas la chaîne à remplacer '{old_path}'")
        else:
            print("La scène n'a pas encore été enregistrée.")

# Lancer l'UI
def show_usd_export_ui():
    try:
        # Vérifier si l'UI est déjà ouverte
        for widget in QtWidgets.QApplication.topLevelWidgets():
            if isinstance(widget, UsdExportUI):
                widget.show()
                return
    except:
        pass
    
    # Créer et afficher l'UI
    ui = UsdExportUI()
    ui.show()
    ui.exec_()  # Garder l'UI ouverte en modal

# Afficher l'UI
show_usd_export_ui()
