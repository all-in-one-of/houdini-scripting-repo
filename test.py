# - - - - - - - - - - - - - - - - - - - - 
# ParmCompTool
# Compares parameters to both default parameters and initial script parameters (not necessarily default)
# TODO: 
# - - - - - - - - - - - - - - - - - - - - 
import traceback
nodes = hou.selectedNodes()

def formatprint(name, current, default, folders,templateType):
	print '{:20}:\t{:10}\t{:10}\t{:20}\t{:20}'.format(name, current, default,folders,templateType)


print 'after'
# iterate through selected nodes
print '\nNon Default Parameters-----------------------------------------'
for  node in nodes:
	print '\n'
	print node.path()
	formatprint(str('name'), str('currentVal'), str('defaultVal'), str('Folder'), str('type or parent param'))	
	parms = node.parmTuples()
	# make comparison node
	cache = node.parent().createNode( node.type().name())

	# iterate through parameters of current node
	for parm,defaultParm in map(None,parms,cache.parmTuples()):
		if not parm.isAtDefault() and  not defaultParm.eval() == parm.eval():
			# organize and gather data
			parmPath = parm.node().path()
			name =  parm.parmTemplate().label()
			currentValue = parm.eval()
			parmType = parm.parmTemplate().type()
			try:
				defaultValue = parm.parmTemplate().defaultValue()

			except AttributeError:
				defaultValue = None

			#print data
			if str(parmType) == 'parmTemplateType.Int' or str(parmType) == 'parmTemplateType.Float': 	
				for current, default in zip(currentValue,defaultValue):
					if(parm.isMultiParmInstance()):
						formatprint(name, current, default, parm[0].containingFolders(), parm.parentMultiParm().name())
					else:
						formatprint(name, current, default,parm[0].containingFolders(),parm[0].parmTemplate().type())
			if str(parmType) == 'parmTemplateType.Menu':
				labels = parm.parmTemplate().menuLabels()
				current = labels[currentValue[0]]
				default = labels[defaultValue]
				formatprint(name, current, default,parm[0].containingFolders(),parm[0].parmTemplate().type())
			if str(parmType) == 'parmTemplateType.Toggle':
				current = str(bool(currentValue[0]))
				default = str(defaultValue)
				formatprint(name, current, default,parm[0].containingFolders(),parm[0].parmTemplate().type())
			if str(parmType) == 'parmTemplateType.String':
				current = currentValue[0]
				default = defaultValue[0]
				formatprint(name, current, default,parm[0].containingFolders(),parm[0].parmTemplate().type())
			if str(parmType) == 'parmTemplateType.Ramp':
				print 'RAMP PARAMETER'
				formatprint(name, current, default,parm[0].containingFolders(),parm[0].parmTemplate().type())
				"""
				current = currentValue[0]
				default = defaultValue[0]
				print formatprint(name, current, default,parm[0].containingFolders(),parm[0].parmTemplate().type())
				if (str(parmType) == 'parmTemplateType.FolderSet' or
					str(parmType) == 'parmTemplateType.Button' or
				  	str(parmType) == 'parmTemplateType.FolderSet' or
				   	str(parmType) == 'parmTemplateType.Separator' or
				    str(parmType) == 'parmTemplateType.Label'):

				"""
	cache.destroy()