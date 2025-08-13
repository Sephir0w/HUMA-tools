import hou
import nodesearch

suffix = "_solo_node"

def getCurrentContext():
	return hou.ui.curDesktop().paneTabOfType(hou.paneTabType.NetworkEditor).pwd()

def getSoloConstant(context_node):
	for node in context_node.children():
		node_name = node.name()
		if node_name.endswith(suffix):
			matcher = nodesearch.Name(node_name.removesuffix(suffix), exact=True)
			if matcher.nodes(context_node):
				return node
	return None

def destroySolo(context_node, constant_node, out_node):
		node_to_connect = constant_node.name().removesuffix(suffix)
		matcher = nodesearch.Name(node_to_connect, exact=True)
		match_nodes = matcher.nodes(context_node)
		if match_nodes:
			node_to_connect = match_nodes[0]

		out_node.setInput(0, node_to_connect)

		constant_node.destroy()


solo_node = None
out_node = None

selected_nodes = hou.selectedNodes()
if selected_nodes:
	solo_node = selected_nodes[0]

if solo_node is not None:
	context_node = solo_node.parent()
else:
	context_node = getCurrentContext()

for node in context_node.children():
	if node.type().name() == "collect":
		out_node = node
		break

constant_node = getSoloConstant(context_node)

if solo_node is not None:
	if constant_node is None:
		if out_node is not None:
			connected_node = out_node.inputs()[0]

		constant_node = context_node.createNode("pxrconstant")
		constant_node.setInput(0, solo_node)
		constant_node.setName(f"{connected_node}{suffix}")

		out_node.setInput(0, constant_node)
	else:
		if constant_node in solo_node.outputs():
			destroySolo(context_node, constant_node, out_node)
		else:
			constant_node.setInput(0, solo_node)


else:
	if constant_node is not None:
		destroySolo(context_node, constant_node, out_node)