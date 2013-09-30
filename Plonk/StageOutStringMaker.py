
# Just constructs an lcg-cp or srmcp command string given some inputs.

class StageOutStringMaker:
  def __init__(self):
    self.BaseCommand="lcg-cp -v -D srmv2 -b"
    self.InputPrefix="file:"
    self.InputFile="blork.root"
    self.OutputURL="srm://cmseos.fnal.gov:8443/srm/v2/server?SFN="
    self.OutputBaseDir="/eos/uscms/store/user/lpcpjm/"
    self.OutputFile=self.InputFile
    
  def constructCommand(self):
    
    fullCommandString="%s \"%s%s\" \"%s%s%s\"" % (self.BaseCommand.strip(),self.InputPrefix.strip(),self.InputFile.strip(),self.OutputURL.strip(),self.OutputBaseDir.strip(),self.OutputFile.strip())
    
    return fullCommandString
  
  
  
  
if __name__=="__main__":
    bloopy=StageOutStringMaker()
    bloopy.InputFile="fuzzy.root"
    bloopy.OutputBaseDir="/eos/uscms/store/user/lpcpjm/PrivateMC/gobbltygook/blomp/"
    print "%s" % bloopy.constructCommand()