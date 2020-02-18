#v1.03, by Daniel Martin
#In collaboration with Raphael Jouretz

from Deadline.Scripting import *
import os
import re

def getFramesForJob(job):
    frames = job.JobFrames.split("-")
    framesNum = (int(frames[1])-int(frames[0]))+1 #+1 because the frame 100 is included
    return framesNum

def __main__(*args):    
    deadlinePlugin = args[0]
    deadlinePlugin.LogInfo("---[STARTING POST-TASK SCRIPT]---")
    deadlinePlugin.LogStdout("Current task ID is {}".format(deadlinePlugin.GetCurrentTaskId()))
    deadlinePlugin.LogInfo("OS is " + os.name)
    if os.name == "nt":
        command = "COPY "
    else:
        command = "cp "
    job = deadlinePlugin.GetJob()

    outputDirectory = job.JobOutputDirectories[0]
    outputName = job.JobOutputFileNames[0]   

    if deadlinePlugin.GetCurrentTaskId() == "0":
        deadlinePlugin.LogStdout("This task is the first frame. Fetching amount of frames to copy...")
        frames = getFramesForJob(job)
        deadlinePlugin.LogStdout("Fetch OK, copying first frame " + str(frames-1) + " times.")
        for number in range(101, getFramesForJob(job)+100):
            pathToInitialFile = os.path.normpath(os.path.join(outputDirectory, outputName.replace("####", "{:04d}".format(100))))
            pathToFile = os.path.normpath(os.path.join(outputDirectory, outputName.replace("####", "{:04d}".format(number))))
            deadlinePlugin.LogInfo("Copying first frame to " + pathToFile)
            fullCommand = command + pathToInitialFile + " " + pathToFile
            deadlinePlugin.LogInfo("Starting command " + fullCommand)
            os.system(fullCommand)
            deadlinePlugin.LogStdout("End of copy")
    else:
        deadlinePlugin.LogStdout("Nothing to do")
    deadlinePlugin.LogInfo("---[ENDING POST-TASK SCRIPT]---")
