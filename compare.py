# - - - - - - - - - - - - - - - - - - - - 
# ParmCompTool
# Compares parameters to both default parameters and initial script parameters (not necessarily default)
# TODO: 
# - - - - - - - - - - - - - - - - - - - - 
import traceback
nodes = hou.selectedNodes()

def formatprint(name, current, default, templateType, folders ):
        print '{:20.20}\t{:<15}\t{:<15}\t{:10.10}\t{:20}'.format( name, current, default, str(templateType).split('parmTemplateType.').pop(), folders )

#Check both parm template default and script initialization defaults
def isNonDefault(parm, defaultParm):
        if parm is not None and defaultParm is not None: 
                if not parm.eval() == defaultParm.eval():
                        return True
                else:
                        return False
        # spare parameters, essentially
        elif parm is not None:
                return True
        else:
                return False

# iterate through selected nodes
print '\nNon Default Parameters' + '-' * 80
for  node in nodes:
        # make comparison node
        selectedComparison = raw_input("select node to compare to, then press Enter:")
        cache = hou.selectedNodes()[0]
        print '\n'
        print (node.path()) + ' compared to ' + (cache.path())
        print '- ' * 40
        formatprint(str('NAME'), str('CURRENT VAL'), str('COMPARISON VAL'), str('TYPE / PARENT'), str('FOLDER'))
        parms = node.parmTuples()
        
        oldfolders = None
        
        # iterate through parameters of current node
        for parm,defaultParm in map(None,parms,cache.parmTuples()):
                try: 
                        folders = parm[0].containingFolders()[0]
                except IndexError or TypeError:
                        folders = None
                if isNonDefault(parm,defaultParm):
                        # organize and gather data
                        try:
                            parmPath = parm.node().path()
                            name =  parm.parmTemplate().label()
                            currentValue = parm.eval()
                            parmType = parm.parmTemplate().type()
                            defaultValue = defaultParm.eval()
                        except AttributeError:
                            print 'attribute error'
                        #print data
                        if str(parmType) == 'parmTemplateType.Ramp':
                        #       formatprint(name, current, default,parm[0].containingFolders(),parm[0].parmTemplate().type())
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
                        elif not oldfolders == folders:
                                print '- ' * 20
                        if str(parmType) == 'parmTemplateType.Int' or str(parmType) == 'parmTemplateType.Float':        
                                for current, default in zip(currentValue,defaultValue):
                                        if(parm.isMultiParmInstance()):
                                                formatprint( name, current, default, parm.parentMultiParm().name(), parm[0].containingFolders())
                                        else:
                                                formatprint(name, current, default, parm[0].parmTemplate().type(), parm[0].containingFolders() )
                        if str(parmType) == 'parmTemplateType.Menu':
                                labels = parm.parmTemplate().menuLabels()
                                current = labels[int(currentValue[0])]
                                default = labels[int(defaultValue[0])]
                                formatprint(name, current, default, parm[0].parmTemplate().type(), parm[0].containingFolders() )
                        if str(parmType) == 'parmTemplateType.Toggle':
                                current = str(bool(currentValue[0]))
                                default = str(bool(defaultValue[0]))
                                formatprint(name, current, default, parm[0].parmTemplate().type(), parm[0].containingFolders() )
                        if str(parmType) == 'parmTemplateType.String':
                                current = currentValue[0]
                                default = defaultValue[0]
                                formatprint(name, current, default, parm[0].parmTemplate().type(), parm[0].containingFolders() )
                        oldfolders = folders