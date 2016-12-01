# - - - - - - - - - - - - - - - - - - - - 
# ParmCompTool
# Compares parameters to both default parameters and initial script parameters (not necessarily default)
# TODO: 
# - - - - - - - - - - - - - - - - - - - - 

#-------------------------------------------------------------------
# IMPORTS                                                          |
#-------------------------------------------------------------------

import hou
import traceback

#-------------------------------------------------------------------
# HELPERS                                                          |
#-------------------------------------------------------------------

formatted = lambda name, current, default, folders, templatetype : '{:20}:\t{:10}\t{:10}\t{:20}\t{:20}'.format(name, current, default, folders, templatetype)

def userInput():
	''' 
	Get user selected nodes and return them as list.
	'''
	nodes = hou.selectedNodes()		
	if nodes == ():
		hou.ui.displayMessage('There are no nodes selected, terminating tool', severity=hou.severityType.Error)
		return None
	
	return nodes

def isNonDefault(parm, defaultparm):
	'''
	Check both parm template default and script initialization defaults.
	
	Keyword arguments:
	parm = parameter that you want to compare
	defaultparm = parameter to which you want to compare
	'''
	if parm is not None and defaultparm is not None:
		return parm.eval() != defaultparm.eval()
	# spare parameters, essentially
	elif parm is not None:
		return True
	else:
		return False

#-------------------------------------------------------------------
# MAIN                                                             |
#-------------------------------------------------------------------

def execute():
	# get user input
	nodes = userInput()
	
	# ensure user input didn't error
	if nodes != None:	
		# iterate through selected nodes
		print ('\nNon Default Parameters-----------------------------------------')		
		header = lambda nodePath: '\n{nodepath}\n{data}'.format(nodepath = nodePath, data = formatted(str('name'), str('currentVal'), str('defaultVal'), str('Folder'), str('type or parent param')))
		
		for currentNode in nodes:		
			print(header(currentNode.path()))			
			parms = currentNode.parmTuples()
			
			# make comparison node
			cache = currentNode.parent().createNode(currentNode.type().name())
		
			# iterate through parameters of current node
			for parm, defaultParm in map(None, parms, cache.parmTuples()):
				if isNonDefault(parm, defaultParm):
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
						for current, default in zip(currentValue, defaultValue):
							if(parm.isMultiParmInstance()):						
								print(formatted(name, current, default, parm[0].containingFolders(), parm.parentMultiParm().name()))
							else:
								print(formatted(name, current, default,parm[0].containingFolders(),parm[0].parmTemplate().type()))
								
					if str(parmType) == 'parmTemplateType.Menu':
						labels = parm.parmTemplate().menuLabels()
						current = labels[currentValue[0]]
						default = labels[defaultValue]
						print(formatted(name, current, default,parm[0].containingFolders(),parm[0].parmTemplate().type()))
						
					if str(parmType) == 'parmTemplateType.Toggle':
						current = str(bool(currentValue[0]))
						default = str(defaultValue)
						print(formatted(name, current, default,parm[0].containingFolders(),parm[0].parmTemplate().type()))
						
					if str(parmType) == 'parmTemplateType.String':
						current = currentValue[0]
						default = defaultValue[0]
						print(formatted(name, current, default,parm[0].containingFolders(),parm[0].parmTemplate().type()))
						
					if str(parmType) == 'parmTemplateType.Ramp':
					#	formatprint(name, current, default,parm[0].containingFolders(),parm[0].parmTemplate().type())
						"""
						current = currentValue[0]
						default = defaultValue[0]
						print formatprint(name, current, default,parm[0].containingFolders(),parm[0].parmTemplate().type())
						if (str(parmType) == 'parmTemplateType.FolderSet' or
							str(parmType) == 'parmTemplateType.Button' or
							str(parmType) == 'parmTemplateType.Ramp' or
							str(parmType) == 'parmTemplateType.FolderSet' or
							str(parmType) == 'parmTemplateType.Separator' or
							str(parmType) == 'parmTemplateType.Label'):
		
						"""
			cache.destroy()

#-------------------------------------------------------------------
# EXECUTE                                                          |
#-------------------------------------------------------------------
execute()