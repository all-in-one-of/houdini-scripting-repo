import traceback
nodes = hou.selectedNodes()
# iterate through selected nodes
print '\nNon Default Parameters-----------------------------------------'
for  node in nodes:
	print '\n'
	print node.path()
	parms = node.parmTuples()
	# iterate through parameters of current node
	for parm in parms:
		if not parm.isAtDefault():
			# organize and gather data
			parmPath = parm.node().path()
			name =  parm.parmTemplate().label()
			currentValue = parm.eval()
			try:
				defaultValue = parm.parmTemplate().defaultValue()
			except AttributeError:
				defaultValue = None
			parmTuple = (name, currentValue, defaultValue)
			parmType = parm.parmTemplate().type()

			#print data
			if str(parmType) == 'parmTemplateType.Int' or str(parmType) == 'parmTemplateType.Float': 	
				for current, default in zip(currentValue,defaultValue):
					print '{:10.10}:\t{:10.10}\t{:10.10}'.format(name, current, default)
			if str(parmType) == 'parmTemplateType.Menu':
				labels = parm.parmTemplate().menuLabels()
				current = labels[currentValue[0]]
				default = labels[defaultValue]
				print '{:10.10}:\t{:10.10}\t{:10.10}'.format(name, current, default)
			if str(parmType) == 'parmTemplateType.Toggle':
				current = str(bool(currentValue[0]))
				default = str(defaultValue)
				print '{:10.10}:\t{:10.10}\t{:10.10}'.format(name, current, default)
			if str(parmType) == 'parmTemplateType.String':
				current = currentValue[0]
				default = defaultValue[0]
				print '{:10.10}:\t{:20.20}\t{:10.10}'.format(name, current, default)
			if str(parmType) == 'parmTemplateType.FolderSet':
				print 'This is a folderSet'
