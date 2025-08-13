import maya.cmds as cmd
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2 import QtUiTools,QtWidgets,QtCore


class MonOutil (QMainWindow):
	def __init__(self):
		super().__init__()
		self.uiFile = "\\Storage03\\Partages\\3D4\\HUMA\\00_management\\script\\UI\\Start_nodegraph.ui"

		loader= QtUiTools.QUiLoader()
		self.ui = loader.load(self.uiFile, parentWidget=self)


		#button

		self.pushButton_Start = self.ui.findChild(QtWidgets.QPushButton, "pushButton_Start")
		self.pushButton_Start.clicked.connect(self.creat_PxrS)

		#Checkbox
		self.checkBox_Diffuse =  self.ui.findChild(QtWidgets.QCheckBox, "checkBox_Diffuse")
		self.checkBox_Specular = self.ui.findChild(QtWidgets.QCheckBox, "checkBox_Specular")
		self.checkBox_Roughness = self.ui.findChild(QtWidgets.QCheckBox, "checkBox_Roughness")
		self.checkBox_SSS = self.ui.findChild(QtWidgets.QCheckBox, "checkBox_SSS")
		self.checkBox_Bump = self.ui.findChild(QtWidgets.QCheckBox, "checkBox_Bump")
		self.checkBox_Disp = self.ui.findChild(QtWidgets.QCheckBox, "checkBox_Disp")
		self.checkBox_Glow_Color = self.ui.findChild(QtWidgets.QCheckBox, "checkBox_Glow_Color")
		self.checkBox_Glow_Gain = self.ui.findChild(QtWidgets.QCheckBox, "checkBox_Glow_Gain")


		#LineEdit
		self.lineEdit_Name_Shader = self.ui.findChild(QtWidgets.QLineEdit, "lineEdit_Name_Shader")
		



		#RENDERMAN

	def creat_PxrS(self, shaderName):
	
		shaderName = self.lineEdit_Name_Shader.text()



		# creer un shader
		myShader = cmd.shadingNode('PxrSurface', asShader=True, name="PxrS_" +shaderName )
	
		# creer un shading group
		myShaderSG = cmd.sets(renderable=True, noSurfaceShader=True, empty=True, name="SG_" +myShader )
	
		# shader au shading group
	
		cmd.connectAttr('%s.outColor' % myShader, '%s.surfaceShader' % myShaderSG)



		# Creer les nodes

		#Diffuse

		if self.checkBox_Diffuse.isChecked() == 1 :

				pxrtexture_diffuse = cmd.shadingNode('PxrTexture', name='PxrT_'+shaderName+'_diffuse', asTexture=True)
				cmd.connectAttr('%s.resultRGB' % pxrtexture_diffuse, '%s.diffuseColor' % myShader)


		 #SPECULAR

		if self.checkBox_Specular.isChecked() == 1 :

			pxrtexture_spec = cmd.shadingNode('PxrTexture', name='PxrT_'+shaderName+'_specular', asTexture=True)
			cmd.connectAttr('%s.resultRGB' % pxrtexture_spec, '%s.specularFaceColor' % myShader)


		#ROUGHNESS

		if self.checkBox_Roughness.isChecked() == 1 :

			pxrtexture_roughness = cmd.shadingNode('PxrTexture', name='PxrT_'+shaderName+'_roughness', asTexture=True)
			cmd.connectAttr('%s.resultR' % pxrtexture_roughness, '%s.specularRoughness' % myShader)

		#SSS


		if self.checkBox_SSS.isChecked() == 1 :
			pxrtexture_SSS = cmd.shadingNode('PxrTexture', name='PxrT_'+shaderName+'_SSS', asTexture=True)
			cmd.connectAttr('%s.resultRGB' % pxrtexture_SSS, '%s.subsurfaceColor' % myShader)


		 #BUMP NORMAL

		if self.checkBox_Bump.isChecked() == 1 :

			pxrtexture_bump = cmd.shadingNode('PxrTexture', name='PxrT_'+shaderName+'_bump_normal', asTexture=True)
			bump = cmd.shadingNode('PxrNormalMap', name='bump_' + shaderName, asTexture=True)
			cmd.connectAttr('%s.resultRGB' % pxrtexture_bump, '%s.inputRGB' % bump)
			cmd.connectAttr('%s.resultN' % bump, '%s.bumpNormal' % myShader)
			

		#DISPLACEMENT

		if self.checkBox_Disp.isChecked() == 1 :

			 displace = cmd.shadingNode('PxrDisplace', name='PxrDisp_' + shaderName, asShader=True)
			 dispTransform = cmd.shadingNode('PxrDispTransform', name='PxrDispT_' + shaderName, asTexture=True)
			 pxrtexture_disp = cmd.shadingNode('PxrTexture', name='PxrT_' + shaderName + '_Disp', asTexture=True)
			 cmd.connectAttr('%s.resultR' % pxrtexture_disp, '%s.dispScalar' % dispTransform)
			 cmd.connectAttr('%s.resultF' % dispTransform, '%s.dispScalar' % displace)
			 cmd.connectAttr('%s.outColor' % displace, '%s.displacementShader' % myShaderSG)

		#Glow


		if self.checkBox_Glow_Color.isChecked() == 1 :
			pxrtexture_Glow_Color = cmd.shadingNode('PxrTexture', name='PxrT_' + shaderName + '_Glow_Color', asTexture=True)
			cmd.connectAttr('%s.resultRGB' % pxrtexture_Glow_Color, '%s.glowColor' % myShader)




		if self.checkBox_Glow_Gain.isChecked() == 1 :
			pxrtexture_Glow_Gain = cmd.shadingNode('PxrTexture', name='PxrT_' + shaderName + '_Glow_Gain', asTexture=True)
			cmd.connectAttr('%s.resultR' % pxrtexture_Glow_Gain, '%s.glowGain' % myShader)





monOutil = MonOutil()
monOutil.show() 