import maya.cmds as cmd
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2 import QtUiTools, QtWidgets, QtCore

class SanityChecker :
	def __init__(self) :
		self.allObj = cmd.ls(exactType = ["mesh", "joint", "nurbsCurve","camera"])		#pour définir tout les objects que vous voulez séléctionner
		self.geo = cmd.ls(exactType = "mesh")
		self.camera = cmd.ls(exactType = "camera")
		self.NameRenderCam = "rendercam"		# pour défénir le nom de la caméra de rendu
		self.formatRenderWidth = 2048		# pour défénir la longueur du rendu 960 pour HD540, 1280 pour HD720, 1920 pour HD1080
		self.formatRenderHeight = 858		# pour défénir la hauteur du rendu 540 pour HD540, 720 pour HD720, 1920 pour HD1080
		self.engineName = "renderman"		# pour défénir le moteur de rendu 
		self.listBaseNameCheck = ['pCube', 'pSphere' ,'pCylinder' ,'pCone' ,'pTorus' ,'pPlane' ,'pDisc' ,'pPlatonic' ,'nurbsCircle' ,'curve' ,'joint']	

	def getReport(self) :

		self.listError = []
		self.listError.append(self.checkCam())
		self.listError.append(self.sizeRender())
		self.listError.append(self.subdivScheme())
		self.listError.append(self.engine())
		self.listError.append(self.doubleName())
		self.listError.append(self.baseName())
		self.listError.append(self.triangle())
		self.listError.append(self.ngons())
		#print(self.listError)

		self.PopupErrors = PopupErrors(self.listError)
		return self.listError 


	def checkCam(self) :

		front = cmd.getAttr("frontShape.renderable")
		persp = cmd.getAttr("perspShape.renderable")
		side = cmd.getAttr("sideShape.renderable")
		top =  cmd.getAttr("topShape.renderable") 
		
		for obj in self.camera:
			if "cameraShape" in obj :
				return'Renomme tes caméras'
			else :
				if front == True or persp == True or side == True or top == True:	
					return 'retire les cam de base des renter setting'

		if self.NameRenderCam + "Shape" not in self.allObj :
			return 'Créer ta rendercam'


	def doubleName(self) :

		doublon = []
		nbDoublon = 0	

		for obj in self.allObj :
			if "|" in obj:
				doublon.append(obj.split('|',)[1])
				nbDoublon += 1

		if nbDoublon > 1 :		 
			return f'Il y a {nbDoublon} doublons dans la scenes, dégage moi tous ca : {doublon}'
		else :
			return "Il n'y a pas de doublon"

	def sizeRender(self) :

		if cmd.getAttr('defaultResolution.width') != self.formatRenderWidth and cmd.getAttr('defaultResolution.height') != self.formatRenderHeight :
			return f"La résolution n'est pas en {self.formatRenderHeight}"
		else :
			return f"La résolution est en HD{self.formatRenderHeight}"
	
	def subdivScheme(self) : 

		objSub = 0

		for obj in self.geo :
			if cmd.getAttr(f"{obj}.rman_subdivScheme") == 0 :
				objSub += 1
		if objSub > 1 :		
			return f'Il y a {objSub} obj non subdiv dans la scene'
		else :
			return 'Tous les obj sont bien catmull_Clark'

	def engine(self) :
		
		if cmd.getAttr("defaultRenderGlobals.currentRenderer") != self.engineName :
			return f"le moteur n'est pas sur {self.engineName}"
		else :
			return f"le moteur est bien sur {self.engineName}"

	def baseName(self) : 
		
		listBaseName = []
		nbName = 0
		
		for obj in self.allObj :
			objCheckName = obj.split("Shape")[0]
			if objCheckName in self.listBaseNameCheck :
				listBaseName.append(obj)
				nbName += 1
		if nbName > 1 :
			return f"Tu as {nbName} obj non renommé, renomme tous ca : {listBaseName}"
		else :
			return "Tous les obj sont renommés et la paul t'en remercie"

	def triangle(self) :

		listTriangle = []
		nbTriangle = 0 

		for obj in self.geo :
			cmd.select(obj, replace = True,)
			cmd.polySelectConstraint(mode = 3, type = 0x0008, size = 1)
			numFace = cmd.polyEvaluate(faceComponent = True)
			if numFace > 1 :
				nbTriangle += 1
				listTriangle.append(obj.split('Shape')[0])
		if nbTriangle > 1 :		
			return f"Tu as {nbTriangle} obj avec des triangles, attention a tous ca : {listTriangle}"
		else :
			return "Tu n'as aucun triangles GGWP"

	def ngons(self) :

		listNgons = []
		nbNgons = 0

		for obj in self.geo :
			cmd.select(obj, replace = True,)
			cmd.polySelectConstraint(mode = 3, type = 0x0008, size = 3)
			numFace = cmd.polyEvaluate(faceComponent = True)
			if numFace > 1 :
				nbNgons += 1
				listNgons.append(obj.split('Shape')[0])

		if nbNgons > 1 :		
			return f"Tu as {nbNgons} obj avec des ngons, fais TRES ATTENTION a tous ca : {listNgons}"
		else :
			return "Aucun ngon"


	def checkTexture(self):
		pxrT = cmd.ls(type=['PxrTexture'])
		countPxrT =len(pxrT)

		if countPxrT !=0:
			for texture in pxrT:
				filename = cmd.getAttr(texture + ".filename")
				if not filename.startwith('<ws>/'):
					return

			return "les textures sont en relatif"
		else:
			return "Il n'y a pas de PxrTexture dans la scène"



class PopupErrors(QMainWindow):

	def __init__(self, listError):
		super().__init__()
		self.uiFile = r"\\storage03\\Partages\\3D4\\HUMA\\00_management\\script\\UI\\SanitycheckerQt.ui"
		loader = QtUiTools.QUiLoader()      
		self.ui = loader.load(self.uiFile, parentWidget = self)
		self.allObj = cmd.ls(exactType = ["mesh", "joint", "nurbsCurve","camera"])		#pour définir tout les objects que vous voulez séléctionner
		self.geo = cmd.ls(exactType = "mesh")
		self.camera = cmd.ls(exactType = "camera")
		self.NameRenderCam = "rendercam"		# pour défénir le nom de la caméra de rendu
		self.formatRenderWidth = 1920		# pour défénir la longueur du rendu	
		self.formatRenderHeight = 1080		# pour défénir la hauteur du rendu
		self.engineName = "renderman"		# pour défénir le moteur de rendu 
		self.listBaseNameCheck = ['pCube', 'pSphere' ,'pCylinder' ,'pCone' ,'pTorus' ,'pPlane' ,'pDisc' ,'pPlatonic' ,'nurbsCircle' ,'curve' ,'joint']

		self.listError = sanity.listError

		#button
		self.button_pass = self.ui.findChild(QtWidgets.QPushButton, "PushButton_Pass")
		self.button_repair = self.ui.findChild(QtWidgets.QPushButton, "PushButton_Repair")
		self.button_repair.clicked.connect(self.correctError)


		#Text
		self.text = self.ui.findChild(QtWidgets.QTextBrowser ,"TextError")
		self.show()

		for error in self.listError:
			print(error)
		self.text.setText(str(self.listError).replace(",","\n"))
		self.button_pass.clicked.connect(self.close)



	def correctError(self):
	
		self.correctEngine()
		self.correctsubdivScheme()
		self.correctCamRenderable()
		self.correctSizeRender()
		self.correctWorkspace()
		self.correctPxrT_Tex()


	def correctEngine(self):
		if cmd.getAttr("defaultRenderGlobals.currentRenderer") != self.engineName :
			cmd.setAttr("defaultRenderGlobals.currentRenderer", "renderman", type="string")
		return f"le moteur n'était pas bon et a été changer pour {self.engineName}"
	
	def correctsubdivScheme(self) : 
	
			objSub = 0
	
			for obj in self.geo :
				if cmd.getAttr(f"{obj}.rman_subdivScheme") == 0 :
					objSub += 1
					cmd.setAttr(f"{obj}.rman_subdivScheme", 1)
			if objSub > 1 :		
				return f'Il y avait {objSub} obj non subdiv dans la scene'
			else :
				return "Tous les obj sont bien catmull_Clark"

	def correctCamRenderable(self):
			if self.NameRenderCam + "Shape" in self.allObj :
				cmd.setAttr("rendercam.renderable",1)
				if front == True or persp == True or side == True or top == True:
					cmd.setAttr("frontShape.renderable",0)
					cmd.setAttr("perspShape.renderable",0)
					cmd.setAttr("sideShape.renderable",0)
					cmd.setAttr("topShape.renderable",0)
			return 'camera corriger'

	def correctSizeRender(self):
		if cmd.getAttr('defaultResolution.width') != self.formatRenderWidth and cmd.getAttr('defaultResolution.height') != self.formatRenderHeight :
			cmd.setAttr('defaultResolution.width',self.formatRenderWidth)
			cmd.setAttr('defaultResolution.height',self.formatRenderHeight)

		else :
			pass

		return 'size corriger'

	def correctWorkspace(self):


		pxrT = cmds.ls(type = ['PxrTexture'])

		for texture in pxrT: 
			
			filename = cmds.getAttr(texture + ".filename")
			filename = filename.split('sourceimages')
			relative = '<ws>/sourceimages'
			filename = '%s%s' %(relative, filename[1])
			cmds.setAttr(texture + '.filename', filename, type='string')

		return 'Workspace corriger pour les PxrTexture'




	def correctPxrT_Tex(self):


	
		pxrTextures = cmds.ls(type='PxrTexture')
		
		for pxrTexture in pxrTextures:
		
			currentPath = cmds.getAttr(pxrTexture + ".filename")
		
			newPath = currentPath.rsplit('.', 1)[0] + '.tex'
		
		
			cmds.setAttr(pxrTexture + ".filename", newPath, type="string")
		
			return'Les images des PxrTexture ont maintenant l\'extension .tex'
	


sanity = SanityChecker()
sanity.getReport()

PopupErrors = PopupErrors()	
PopupErrors.correctError()