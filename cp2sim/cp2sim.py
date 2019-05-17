# This script will boot the specified simh image and
# recursively copy the INPATH from the host OS
# to the OUTPATH on the simulated OS

INPATH = "../nsys_root"

# Specify the full outpath
OUTPATH = "/sys/nsys"

SIMPATH = "../../HistoryUnix/simh/BIN/pdp11"
SIMINI = "./boot.ini"

# Time between lines
# Just putting everything in will crash the simulator
TBL = 0.1

print("Execution started")

import os, time, sys
import subprocess, threading, psutil
from appscript import app, k


commands = []
def execute(cmd, newline=True, control=None, timeskip=0):
    end = '\n' if newline else ''
    #print(cmd + end, end='')
    commands.append(((cmd + end), control, timeskip))
    #time.sleep(TBL)

######################################
# GATHER COMMANDS
######################################

#execute("unix") # choose kernel
#execute("root") # log in

### CREATE OUTPATH DIRECTORIES ###
outpathComps = OUTPATH.split("/")
for i in range(len(outpathComps)-1):
    execute("mkdir " + '/'.join(outpathComps[:(i+2)]))

### CREATE AND FILL FILES AND SUBDIRS ###
for (root, dirs, files) in os.walk(INPATH):
    simRoot = OUTPATH + root.split(INPATH)[1] + "/"
    
    # Create subdirectories
    for d in dirs:
        execute("mkdir " + simRoot + d)

    # Create Files
    for f in files:
        execute("", timeskip=2)
        if f.startswith('.'):
            continue
        execute("cat > " + simRoot + f)

        # open file
        with open(root+'/'+f) as lf:
            lines = lf.read().split('\n')
            for line in lines:
                execute(line)

        # end cat with control-d
        execute('d', newline=False, control=k.control_down)

execute('sync')
execute('sync')
execute('sync')
execute('sync')
execute('e', newline=False, control=k.control_down) # control e to quit simh
execute('exit')

print ("Will now paste %d lines" % (len(commands)))
s = len(commands) * TBL
print ("Will take about %d seconds (%.2f minutes)" % (s, s/60))
try:
    input("Continue with ENTER\n")
except KeyboardInterrupt:
    print("Aborted")

######################################
# START SIMULATOR
######################################

print("Now select the Terminal")
time.sleep(4)

n = 0
for cmd in commands:
    n += 1
    if cmd[2] > 0:
        print("Command: %05d / %05d" % (n, len(commands)))
        time.sleep(cmd[2])
        continue
    time.sleep(TBL)
    print(cmd[0], end='')
    if cmd[1]:
        app('System Events').keystroke(cmd[0], using=cmd[1])
    else:
        app('System Events').keystroke(cmd[0])