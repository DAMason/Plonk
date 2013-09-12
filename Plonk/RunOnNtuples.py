#!/usr/bin/python 

# this sucks in a list of xrootd files, then produces jdl's to feed the ntuple analysis executable.  
# will need to deal with environment, etc.  Probably scram things up with some random release just 
# to get the root env, etc.

import sys,getopt,os
from JDLmaker import JDLmaker
from ExeMaker import ExeMaker
from StageOutStringMaker import StageOutStringMaker

# Just so we don't forget these ---
#     cout << "Something is wonky with the command line args..." << endl;
#     cout << "Usage: " << endl;
#     cout << "CrapExe  " << endl;
#     cout << "                -analysis      Pho||LL" << endl;
#     cout << "                -outputname    <output file base> " << endl;
#     cout << "                -copyevents    (no argument -- bool)" << endl;
#     cout << "                -printinterval <int # events>" << endl;
#     cout << "                -printlevel    <int # 0-2> " << endl;
#     cout << "                -addHLTlist    <file> " << endl;
#     cout << "                -logfile       <file> " << endl;
#     cout << "                -inputfilefiles    <file> " << endl;
#     cout << "                -inputfilelist <file> <file> <file> ..." << endl;
#     cout << "                -includejson   <file>  (can be used repeatedly)" << endl;       



# MAIN IS HERE:

def main(argv):
  xrootdlist=''                            # the list of root files to suck in 
  myexecutable='bin/CrapExe'               # the name of the executable going to run 
  filesperjob=1                            # number of files out of xrootdlist to drop into each job.
  
  executablefilelistargument=' -inputfilelist '            # the argument the thing uses to identify its list of input files
  executableOtherArguments=' -analysis Pho -printinterval 100 -copyevents -processevents -1 '              # a text string with the rest of the arguments that get passed to myexecutable
  
  outputname='test'
  analysis='Pho'
  sandbox='sandbox.tgz'
  
  try:
    opts,args=getopt.getopt(argv,"",["xrootdlist=","filesperjob=","outputname=","analysis="])
  except getopt.GetoptError:
    print 'RunOnNtuples --xrootdlist=<file with xrootd URLs>'
    print '             --filesperjob=#'
    print '             --outputname=<text string base for output files>'
    print '             --analysis=Pho|LL (default Pho)'
    print '             --sandbox=<sandbox path>'

  for opt,arg in opts:
    if opt == '--xrootdlist':
      xrootdlist=arg
    elif opt == '--filesperjob':
      filesperjob=int(arg)
    elif opt == '--outputname':
      outputname=arg
    elif opt == '--analysis':
      analysis=arg
    elif opt == '--sandbox':
      sandbox=arg
      
  # lets do some checks first...
    
  sandbox=os.path.realpath(sandbox) # spiffy it up a bit... need the full path for the jdl...
  if not os.path.exists(sandbox):
    print "Couldn't find sandbox in %s" % sandbox
    sys.exit(1)
    
  if not os.path.exists(xrootdlist):
    print "Couldn't find list of files at: %s" % xrootdlist
    sys.exit(1)
      
  
  print "Now constructing a work area named: %s" % outputname
  
  MyNewPath=os.path.join(os.getcwd(),outputname)
  print "Gonna make working directory %s" % MyNewPath

  try:
    os.mkdir(MyNewPath)
  except OSError:
    print "Something bad happened in trying to make the directory..."
    raise # want to make noise if it already existed for example (or anything else bad happened)

  TheFileList=LineOfFileNames(xrootdlist,filesperjob)
  print "Got a list of %s batches of files (which then become jobs)..." % len(TheFileList)

  
  # OK -- now we should have all the pieces to start making some jobs in the work dir...
  
  jobcounter=0
  for xrootdchunk in TheFileList:
    
    thisjobsbasename="%s_%s" % (outputname,jobcounter)
    basenamearg=" -outputname %s" % thisjobsbasename

    # construct executable command line first...
    crapexeline=myexecutable + basenamearg + executableOtherArguments + executablefilelistargument + xrootdchunk
    # print crapexeline
    
    # next we make our executable
    thisjobexe=ExeMaker()
    thisjobexe.TheRestOfIt=''

    thisjobexe.TheRestOfIt+="ls -alt \n"
    thisjobexe.TheRestOfIt+="export SCRAM_ARCH=slc5_amd64_gcc462 \n"
    thisjobexe.TheRestOfIt+="scramv1 project CMSSW CMSSW_5_3_9 \n"
    thisjobexe.TheRestOfIt+="mv %s CMSSW_5_3_9/src \n" % os.path.basename(sandbox)
    thisjobexe.TheRestOfIt+="cd CMSSW_5_3_9/src \n"
    thisjobexe.TheRestOfIt+="tar -xzvf %s \n" % os.path.basename(sandbox)
    thisjobexe.TheRestOfIt+=crapexeline + "\n\n"
    
    # now we try to stage out all the results -- getting a generic stageout line
    # the idea here is to construct something that catches all the root files that are found, but puts 
    # them in generic directories with the job unique part removed...  So all the hist_whatever_xxx.root files
    # go in a hist subdir, then foo_whatever_xxx.root go in the foo subdir, etc.

    # Would certainly be easier if this was all python handled but not quite there yet...
    
    thisjobexe.TheRestOfIt+="for outfile in `ls *.root` ;\n"
    thisjobexe.TheRestOfIt+=" do $fname=$outfile \n"
    thisjobexe.TheRestOfIt+="    outsubbase=`echo fname|sed -e 's/_%s//g'|sed -e 's/\.root//g'` \n" % thisjobsbasename
    thisjobexe.TheRestOfIt+="    outfname=$outsubbase/$fname \n"
    
    genericstage=StageOutStringMaker()
    genericstage.InputFile="$fname"
    genericstage.OutputFile="%s/$outfname" % outputname
    
    thisjobexe.TheRestOfIt+="    %s \n" % genericstage.constructCommand()
    thisjobexe.TheRestOfIt+=" done \n\n"
    
    thisjobexefile="%s.sh" % jobcounter
    thisjobexepath=os.path.join(MyNewPath,thisjobexefile) # note also use this later...
    thisjobexe.write(thisjobexepath)  # Write out the exe file.  
    

    # Nwe write out the jdl for this job...
    
    thisjobjdl=JDLmaker()
    thisjobjdl.jdldic['Sandbox']=sandbox
    thisjobjdl.jdldic['Executable']=thisjobexepath
    thisjobjdl.jdldic['Output']=os.path.join(MyNewPath,str(jobcounter)+".stdout")
    thisjobjdl.jdldic['Error']=os.path.join(MyNewPath,str(jobcounter)+".stderr")
    thisjobjdl.jdldic['Log']=os.path.join(MyNewPath,str(jobcounter)+".log")  
      
    thisjobjdlfile="%s.jdl" % jobcounter  
    thisjobjdl.write(os.path.join(MyNewPath,thisjobjdlfile))  
      
      
    jobcounter+=1  # end of loop -- now go to the next job...
      
      

# Utility bits...

def LineOfFileNames(xrootlistfilename="",howmany=1):
      howmany=int(abs(howmany)) # wiseguy protection...
      if (xrootlistfilename==""): # and this too...
        return []
      
      xrootfilelist=[]
      
      try:
        xrootfilefile=open(xrootlistfilename,'r')
      except IOError:
        print "Not able to ope %s..." % xrootlistfilename
        return []
      else:
        for line in xrootfilefile:
          if line.find('root')!=-1:
            xrootfilelist.append(line.strip())
        xrootfilefile.close
      
      # now we should have read in the files and converted them to a list of strings...
      
      returnlist=[]
      
      if len(xrootfilelist)>0:
        filecount=0
        linecount=0
        argstring=''
        for xrootfile in xrootfilelist:
          argstring+=" " + xrootfile
          if (filecount+1)%howmany==0:
            returnlist.append(argstring)
            linecount+=1
            argstring=''
          filecount+=1
      else:
        print "Um... We didn't get any files in our list..."  
        return []
      
      return returnlist
    
    
        


if __name__ == "__main__":
  main(sys.argv[1:])
  
  
 

