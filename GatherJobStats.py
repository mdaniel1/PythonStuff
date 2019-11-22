from Deadline.Scripting import *
from Deadline.Jobs import *
import datetime
import os
import Tkinter, tkFileDialog

data = {}
data["path"] = os.environ['USERPROFILE']+"\\Documents\\"
data["file"] = ""
data["date"] = str(datetime.date.today())
data["filepath"] = ""

root = Tkinter.Tk()
root.withdraw()

def formatJobTitle(jobName, epNumber, jobComment):
    shotNumber = ""
    lines = jobName.split(" ")

    for line in lines:
        if line.startswith(epNumber):
            shotNumber = line[6:]
    jobTitle = "("+ epNumber +") " + shotNumber
    if "lightRenderFinal" in jobName:
        jobTitle += " | lightRenderFinal "
        if len(lines) == 9:
            for l in lines[8].split('_'):
                if "layer" in l.lower():
                    jobTitle += l
    elif "BATCHER" in jobName:
        jobTitle += jobComment[8:14] + " | Build"
    elif "preCompBuild" in jobName:
        jobTitle += " | preCompBuild"
    elif "preCompRender" in jobName:
        jobTitle += " | preCompRender"

    return jobTitle

def formatTime(str):
    str = str.replace(":", "h", 1)
    str = str.replace(":", "m", 1)
    if(str.count(".") == 2):
        str = str.replace(".", "j", 1)
    str = str.replace(".", "s@", 1)
    line = str.split("@")
    str = line[0]

    return str

def writeToFile(logFile, jobName, episode, jobComment, jobId, jobTotalTaskRenderTime, jobAVGFrameTime):
    #print("Writing stats to file...")
    logFile.write("######" + formatJobTitle(jobName, episode, jobComment) + " ("+ jobId +")######")
    logFile.write("\n")
    logFile.write("Total task render time : \t" + jobTotalTaskRenderTime)
    logFile.write("\n")
    logFile.write("Average frame time : \t\t" + jobAVGFrameTime)
    logFile.write("\n")
    logFile.write("\n")

def updateFile(episode, shot=""):
    data["file"]= data["date"]+"_"+episode+"_"+shot+".txt"
    data["filepath"] = data["path"]+data["file"]

def __main__():
    os.system("cls")
    episodeNumber = raw_input("Episode number to filter : ")
    episode = "ep"+episodeNumber
    data["file"]= data["date"]+"_"+episode+".txt"
    data["filepath"] = data["path"]+data["file"]

    while True:
        os.system("cls")
        print("---MENU---")
        print("1) Get stats for shot")
        print("2) Get stats for all")
        print("3) Change episode")
        print("4) Change output file directory")
        print("9) Quit")
        print("\n")
        choice = int(input("Choice : "))

        if choice == 1:
            number = int(input("Shot number : "))
            shot = "sh"+"{:04d}".format(number)
            updateFile(episode, shot)

            try:
                logFile = open(data["filepath"], "a+")
            except:
                print("Couldn't open file " + data["filepath"])
                exit()
            for job in RepositoryUtils.GetJobs(True):
                jobName = job.JobName
                if shot in jobName or shot in job.JobComment:
                    #print("(DEBUG) job found : " + jobName + " | " + job.JobComment)
                    jobId = job.JobId
                    job = RepositoryUtils.GetJob(job.JobId, True)
                    tasks = RepositoryUtils.GetJobTasks(job, True)
                    stats = JobUtils.CalculateJobStatistics(job, tasks)
                    jobAVGFrameTime = stats.AverageFrameTimeAsString
                    jobAVGFrameTime = formatTime(jobAVGFrameTime)
                    jobTotalTaskRenderTime = stats.TotalTaskRenderTimeAsString
                    jobTotalTaskRenderTime = formatTime(jobTotalTaskRenderTime)
                    writeToFile(logFile, jobName, episode, job.JobComment, job.JobId, jobTotalTaskRenderTime, jobAVGFrameTime)
            print("Done.\n")
            logFile.close()
            updateFile(episode)
            os.system("pause")
        elif choice == 2:
            try:
                logFile = open(data["filepath"], "a+")
            except:
                print("Couldn't open file " + data["filepath"])
                exit()
            for job in RepositoryUtils.GetJobs(True):
                jobName = job.JobName
                if episode in jobName or episode in job.JobComment:
                    jobId = job.JobId
                    job = RepositoryUtils.GetJob(job.JobId, True)
                    tasks = RepositoryUtils.GetJobTasks(job, True)
                    stats = JobUtils.CalculateJobStatistics(job, tasks)
                    jobAVGFrameTime = stats.AverageFrameTimeAsString
                    jobAVGFrameTime = formatTime(jobAVGFrameTime)
                    jobTotalTaskRenderTime = stats.TotalTaskRenderTimeAsString
                    jobTotalTaskRenderTime = formatTime(jobTotalTaskRenderTime)
                    writeToFile(logFile, jobName, episode, job.JobComment, job.JobId, jobTotalTaskRenderTime, jobAVGFrameTime)
            print("Done.\n")
            logFile.close()
            os.system("pause")
        elif choice == 3:
            episodeNumber = raw_input("Episode number to filter : ")
            episode = "ep"+episodeNumber
        elif choice == 4:
            print("Currently : " + data["filepath"])
            if(raw_input("Change? (y/n) : ") == 'y'):
                data["path"] = tkFileDialog.askdirectory() + "/"
                data["path"] = data["path"].replace("/", "\\")
                updateFile(episode)
        elif choice == 9:
            os.system("cls")
            break
