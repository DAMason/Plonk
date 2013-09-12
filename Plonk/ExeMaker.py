
# write out a bootstrap executable...

import sys

class ExeMaker:
  def __init__(self):
    
    self.ExecHeader="""
#!/bin/bash
printenv
uname -a
if [ -e /uscmst1/prod/sw/cms/setup/shrc ]
    then
      . /uscmst1/prod/sw/cms/setup/shrc
    else if [ -e $OSG_APP/cmssoft/cms/cmsset_default.sh ]
    then
      source $OSG_APP/cmssoft/cms/cmsset_default.sh
    fi
fi
export HOME=$PWD
    """
    
    self.TheRestOfIt="""
    """
    
  def write(self,execfilename='stdout'):
    try:
      if (execfilename.lower()=='stdout'):
        execout=sys.stdout
      else:
        execout=open(execfilename,'w')  
        
      execout.write(self.ExecHeader)
      execout.write(self.TheRestOfIt)
      if (not execfilename.lower()=='stdout'): 
        execout.close()    
    except:
      print "somehow couldn't open %s for writing..." % execfilename
      raise

 
# for testing... 
if __name__=="__main__":
  froopy=ExeMaker()
  froopy.TheRestOfIt="""
ls -alt
  """
  froopy.write('stdout')
  
