from Deadline.Scripting import *
import os

def findJob(job, deadlinePlugin):
    currentJob = None
    
    deadlinePlugin.LogInfo("Looking for current job...")
    AllJobs = RepositoryUtils.GetJobs(True)
    for j in AllJobs:
        if str(job) in j.JobName:
            deadlinePlugin.LogInfo("Job found, name is " + str(job))
            currentJob = RepositoryUtils.GetJob(j.JobId, True)
    return currentJob

def getFramesForJob(job):
    frames = job.JobFrames.split("-")
    framesNum = (int(frames[1])-int(frames[0]))+1 #+1 because the frame 100 is included
    return framesNum

def __main__(*args):
    deadlinePlugin = args[0]
    deadlinePlugin.LogInfo("---[STARTING PRE-TASK SCRIPT]---")
    deadlinePlugin.LogStdout("OS is " + os.name)
    deadlinePlugin.LogStdout("DEBUG : Current task ID is {}".format(deadlinePlugin.GetCurrentTaskId()))
    
    #These are used for debugging
    #job = deadlinePlugin.GetJob()
    #currentJob = findJob(job, deadlinePlugin)
    #outputDirectory = currentJob.JobOutputDirectories[0]
    #outputName = currentJob.JobOutputFileNames[0]
    #for number in range(100, getFramesForJob(currentJob)+101):
    #        deadlinePlugin.LogStdout(str(number))
    
    if deadlinePlugin.GetCurrentTaskId() != "0":
        deadlinePlugin.LogStdout("This task isn't the first frame, setting to complete")
        tasks = []
        tasks.append(deadlinePlugin.GetCurrentTask())
        job = deadlinePlugin.GetJob()
        slaveName = deadlinePlugin.GetSlaveName()
        deadlinePlugin.SetProgress(100)
        RepositoryUtils.CompleteTasks(job, tasks, slaveName)
    else:
        deadlinePlugin.LogStdout("This task is the first frame, proceed with frame rendering")
    deadlinePlugin.LogInfo("---[ENDING PRE-TASK SCRIPT]---")
