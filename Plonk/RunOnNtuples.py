#!/usr/bin/python 

# this sucks in a list of xrootd files, then produces jdl's to feed the ntuple analysis executable.  
# will need to deal with environment, etc.  Probably scram things up with some randome release just 
# to get the root env, etc.

import sys,getopt

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



def main(argv):
  xrootdlist=''                            # the list of root files to suck in 
  myexecutable='CrapExe'                   # the name of the executable going to run 
  filesperjob=1                            # number of files out of xrootdlist to drop into each job.
  
  executablefilelistargument='-inputfilelist'            # the argument the thing uses to identify its list of input files
  executableOtherArguments='-printinterval 100 -copyevents -processevents -1'              # a text string with the rest of the arguments that get passed to myexecutable
  
  outputname='test'
  analysis='Pho'
  
  try:
    opts,args=getopt.getopt(argv,"",["xrootdlist=","filesperjob=","outputname=","analysis="])
  except getopt.GetoptError:
    print 'RunOnNtuples --xrootdlist=<file with xrootd URLs>'
    print '             --filesperjob=#'
    print '             --outputname=<text string base for output files>'
    print '             --analysis=Pho|LL (default Pho)'

  for opt,arg in opts:
    if opt == '--xrootdlist':
      xrootdlist=arg
    elif opt == '--filesperjob':
      filesperjob=int(arg)
    elif opt == '--outputname':
      outputname=arg
    elif opt == '--analysis':
      analysis=arg

# now we suck in our files...

  xrootfilelist=[]

  try:
    xrootfilefile=open(xrootdlist,'r')
  except IOError:
    print "Not able to open %s..." % xrootdlist
  else:
    for line in xrootfilefile:
      if (line.find('root')!=-1):
        xrootfilelist.append(line.strip())
    xrootfilefile.close
   
    
  if len(xrootfilelist)>0:
    filecount=0
    argstring='-inputfilelist'
    for xrootfile in xrootfilelist:
      argstring+=" " + xrootfile 
      if filecount%filesperjob==0:
        print myexecutable + " " + argstring
        argstring='-inputfilelist'
      filecount+=1
  else:
    print "Um... We didn't get any files in our list..."





if __name__ == "__main__":
  main(sys.argv[1:])
  
  
 

