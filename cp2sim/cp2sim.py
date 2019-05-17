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
TBL = 1.0

print("Execution started")

import os, time, sys
import subprocess, threading, psutil
from appscript import app, k


commands = []
def execute(cmd, newline=True):
    end = '\n' if newline else ''
    #print(cmd + end, end='')
    commands.append(cmd + end)
    #time.sleep(TBL)

######################################
# GATHER COMMANDS
######################################

execute("unix") # choose kernel
execute("root") # log in

### CREATE OUTPATH DIRECTORIES ###
outpathComps = OUTPATH.split("/")
for i in range(len(outpathComps)-1):
    execute("mkdir " + '/'.join(outpathComps[:(i+2)]))

### CREATE AND FILL FILES AND SUBDIRS ###
for (root, dirs, files) in os.walk(INPATH):
    continue
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

execute('\x05', newline=False) # control e to quit simh
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

#sim = subprocess.Popen([SIMPATH, SIMINI], stdin=subprocess.PIPE, shell=True)
sim = subprocess.Popen(["sh"], stdin=subprocess.PIPE)

try:
    execute(SIMPATH)
    #for cmd in commands:
    #    time.sleep(TBL)
    #    sim.stdin.write(cmd.encode())
    #    sim.stdin.flush()

    #sim.stdin.write('\x04'.encode())

    sim.stdin.write((SIMPATH + "\n").encode())
    sim.stdin.flush()

    time.sleep(2)

    parent = psutil.Process(sim.pid)
    for p in parent.children(recursive=True):
        print(p)

    sim.stdin.write(b"unix\n")

    time.sleep(2)
    sim.stdin.write(b"root\n")
    
    print("Done commands")
    time.sleep(5)
    sim.stdin.close()
finally:
    sim.terminate()
    try:
        sim.wait(timeout=0.2)
        print('== subprocess exited with rc =', sim.returncode)
    except subprocess.TimeoutExpired:
        print('subprocess did not terminate in time')