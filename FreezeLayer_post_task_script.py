from Deadline.Scripting import *
import os
import re

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
	deadlinePlugin.LogInfo("---[STARTING POST-TASK SCRIPT]---")
	deadlinePlugin.LogStdout("DEBUG : Current task ID is {}".format(deadlinePlugin.GetCurrentTaskId()))

	job = deadlinePlugin.GetJob()
	currentJob = findJob(job, deadlinePlugin)

	outputDirectory = currentJob.JobOutputDirectories[0]
	outputName = currentJob.JobOutputFileNames[0] # Initial format has '####' instead of numbers

	if deadlinePlugin.GetCurrentTaskId() == "0":
		deadlinePlugin.LogStdout("This task is the first frame. Fetching amount of frames to copy...")
		frames = getFramesForJob(currentJob)
		deadlinePlugin.LogStdout("Fetch OK, copying first frame " + str(frames-1) + " times.")
		for number in range(101, getFramesForJob(currentJob)+100):
			pathToFile = outputDirectory + "\\" + outputName.replace("####", "{:04d}".format(number))
			deadlinePlugin.LogInfo("DEBUG : Copying first frame to " + pathToFile)
			if os.name == "nt":
				os.system("COPY "+outputDirectory+"\\"+outputName.replace("####", "{:04d}".format(100))+" "+ pathToFile)
			else:
				os.system("cp "+outputDirectory+"/"+outputName.replace("####", "{:04d}".format(100))+" "+outputDirectory+"/"+outputName.replace("####", "{:04d}".format(number)))
				deadlinePlugin.LogStdout("End of copy")
	deadlinePlugin.LogInfo("---[ENDING POST-TASK SCRIPT]---")
