# This script will boot the specified simh image and
# recursively copy the INPATH from the host OS
# to the OUTPATH on the simulated OS

INPATH = "../nsys_root"

# Specify the full outpath
OUTPATH = "/sys/nsys"

# Time between lines
# Just putting everything in will crash the simulator
TBL = 0.2

import os, time

commands = []
def execute(cmd, newline=True):
    end = '\n' if newline else ''
    print(cmd + end, end='')
    commands.append(cmd + end)
    #time.sleep(TBL)

######################################
# SIMULATOR SETUP
######################################

# start subprocess

execute("unix") # choose kernel
execute("root") # log in

######################################
# CREATE OUTPATH DIR
######################################

outpathComps = OUTPATH.split("/")
for i in range(len(outpathComps)-1):
    execute("mkdir " + '/'.join(outpathComps[:(i+2)]))

for (root, dirs, files) in os.walk(INPATH):
    simRoot = OUTPATH + root.split(INPATH)[1] + "/"
    
    # Create subdirectories
    for d in dirs:
        execute("mkdir " + simRoot + d)

    # Create Files
    for f in files:
        if f.startswith('.'):
            continue
        execute("cat > " + simRoot + f)

        # open file
        with open(root+'/'+f) as lf:
            lines = lf.read().split('\n')
            for line in lines:
                execute(line)

        # end cat with control-d
        execute('\n\x04', newline=False)

print(len(commands))