
# Tying together some bits and pieces relevant for making jdl's...


import sys
import random

class JDLmaker:
  
  def __init__(self):
      self.Sandbox='sandbox.tgz'
      self.jdldic={
                   'universe':'globus',
                   'grid_resource':'gt2 red.unl.edu:2119/jobmanager-condor',
                   'transfer_input_files':'YES',
                   'should_transfer_files':'YES',
                   'notification':'NEVER',
                   'Executable':'/blah/blah',
                   'Output':'CRAPOLIO.stdout',
                   'Error':'CRAPOLIO.stderr',
                   'Log':'CRAPOLIO.log',
                   'when_to_transfer_output':'ON_EXIT'
                   }
      self.sitedic={ # this is something we should really be pulling out of SiteDB, but for now the quick and dirty thing...
                    'UCSD':'osg-gw-2.t2.ucsd.edu:2119/jobmanager-condor',
                    'UNL':'red.unl.edu:2119/jobmanager-condor',
                    'UERJ':'osgce64.hepgrid.uerj.br:2119/jobmanager-condor',
                    'UCSD2':'osg-gw-4.t2.ucsd.edu:2119/jobmanager-condor',
                    'WISC':'cmsgrid01.hep.wisc.edu:2119/jobmanager-condor',
                    'ND':'earth.crc.nd.edu:2119/jobmanager-condor',
                    'FNAL2':'cmsosgce2.fnal.gov:2119/jobmanager-condor',
                    'Caltech':'cit-gatekeeper2.ultralight.org:2119/jobmanager-condor',
                    'MIT':'ce02.cmsaf.mit.edu:2119/jobmanager-condor',
                    'UCR':'top.ucr.edu:2119/jobmanager-condor',
                    'Caltech2':'cit-gatekeeper.ultralight.org:2119/jobmanager-condor',
                    'UCDAVIS':'cms.tier3.ucdavis.edu:2119/jobmanager-condor',
                    'Purdue':'osg.rcac.purdue.edu:2119/jobmanager-condor',
                    'WISC2':'cmsgrid02.hep.wisc.edu:2119/jobmanager-condor',
                    'UNL2':'red-gw2.unl.edu:2119/jobmanager-condor',
                    'UMD':'hepcms-0.umd.edu:2119/jobmanager-condor',
                    'FNAL':'cmsosgce.fnal.gov:2119/jobmanager-condor',
                    }
      

# actually write out the jdl
  def write(self,jdlfilename='stdout'):
    try:
      if (jdlfilename.lower()=='stdout'):
        jdlout=sys.stdout
      else:
        jdlout=open(jdlfilename,'w')  
      for j in self.jdldic.keys():
        jdlout.write("%s = %s\n" % (j,self.jdldic[j])) 
      if (not jdlfilename.lower()=='stdout'): 
        jdlout.close()       
    except:
      print "somehow couldn't open %s for writing..." % jdlfilename
      raise


# set the CE we submit to through a list -- randomly select if there's more than one...
  def setCE(self,CEKey=['FNAL']):
    if len(CEKey)==0:
      print "Fed empty CE list -- going with default: %s" % self.jdldic['grid_resource']
    else:
      self.jdldic['grid_resource']='gt2 %s' % self.sitedic[random.choice(CEKey)]


# for testing...
if __name__ == "__main__":
  blorp=JDLmaker()
  blorp.setCE(['WISC','Caltech','UNL'])
  # blorp.setCE([])
  blorp.jdldic['Executable']='wiggly.sh'
  blorp.write('stdout')
  
  