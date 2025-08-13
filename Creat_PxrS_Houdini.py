import hou
import os

textureChannels = ['baseColor','Roughness','height','Opacity','Metalness']

#set the base name
baseName = hou.ui.readInput(initial_contents="Insert Name", message="Set the base object name", buttons=["Save","Cancel"], title="Object BaseName")

if baseName[0] == 0 and baseName[1] != '':
    
    #set the texture directory with file input
    currentproject = os.path.dirname(hou.hipFile.path())
        
    #create shader
    selection = hou.selectedNodes()[0]
    context = selection.parent()
    
    # Create PxrMaterialBuilder node
    pxrBuild = selection.createNode("pxrmaterialbuilder", "PxrBuild_" + baseName[1] )

    # Inside the PxrBuild node
    outputCollect = pxrBuild.node("output_collect")

    # Create a pxrsurface and link it to the collect
    pxrSurface = pxrBuild.createNode("pxrsurface", "PxrS_" + baseName[1] )    
    outputCollect.setInput(0, pxrSurface, 0)
    
    #create PxrDisplace and link it to the collect
    pxrdisplace = pxrBuild.createNode("pxrdisplace", "PxrD_" + baseName[1])
    outputCollect.setInput(1, pxrdisplace, 0)
    displaceVestorNode = pxrBuild.createNode("pxrtexture", "PxrT_DispV_"+ baseName[1])
    pxrdisplace.setInput(2, displaceVestorNode, 0)



    #create PxrTexture 
        #create Diffuse
    diffuseNode = pxrBuild.createNode("pxrtexture", "PxrT_" + baseName[1] + "_diffuse")
    pxrSurface.setInput(2, diffuseNode, 0)
    
        #create Spec
    specularNode = pxrBuild.createNode("pxrtexture", "PxrT_" + baseName[1] + "_spec")
    pxrSurface.setInput(9, specularNode, 0)

        #create Roughness
    roughnessNode = pxrBuild.createNode("pxrtexture", "PxrT_" + baseName[1] + "_Roughness")
    pxrSurface.setInput(14, roughnessNode, 1)

        #create SSS
    sssNode = pxrBuild.createNode("pxrtexture", "PxrT_" + baseName[1] + "_SSS")
    pxrSurface.setInput(55, sssNode, 0)

        #create Normal
    normalNode = pxrBuild.createNode("pxrnormalmap", "PxrN_" + baseName[1])
    pxrSurface.setInput(103, normalNode, 0)