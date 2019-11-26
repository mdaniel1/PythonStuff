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

def getFramesForJob(job):
    if "BATCHER" in job.JobName:
        return job.JobFrames
    else:
        frames = job.JobFrames.split("-")
        framesNum = int(frames[1])-int(frames[0])
        return framesNum

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

def fixBATCHER(job):
    job.SetJobEnvironmentKeyValue("PYTHONPATH", "K:\\SUPERPROD;K:\\SUPERPROD\\lib;K:\\SUPERPROD\\TOTO;K:\\SUPERPROD\\AUTORIG;K:\\SUPERPROD\\TOTO\\plugins;K:\\SUPERPROD\\runtime")
    job.SetJobEnvironmentKeyValue("foundry_LICENSE", "4101@192.168.124.249")
    RepositoryUtils.SaveJob(job)

def fixPreComp(job):
    job.SetJobEnvironmentKeyValue("PYTHONPATH", "K:\\SUPERPROD;K:\\SUPERPROD\\lib;K:\\SUPERPROD\\TOTO;K:\\SUPERPROD\\runtime")
    job.SetJobEnvironmentKeyValue("foundry_LICENSE", "4101@192.168.124.249")
    RepositoryUtils.SaveJob(job)

def writeToFile(logFile, jobName, episode, jobComment, jobId, jobTotalTaskRenderTime, jobAVGFrameTime, frames):
    #print("Writing stats to file...")
    logFile.write("######" + formatJobTitle(jobName, episode, jobComment) + " ("+ jobId +")######")
    logFile.write("\n")
    logFile.write("Total task render time : \t" + jobTotalTaskRenderTime)
    logFile.write("\n")
    logFile.write("Average frame time : \t\t" + jobAVGFrameTime)
    logFile.write("\n")
    logFile.write("Frames : \t\t\t" + str(frames))
    logFile.write("\n")
    logFile.write("\n")


def updateFile(episode, shot=""):
    data["file"]= data["date"]+"_"+episode+"_"+shot+".txt"
    data["filepath"] = data["path"]+data["file"]

def __main__():
    os.system("cls")
    loop = True
    while loop:
        try:
            episodeNumber = raw_input("Episode number to filter : ")
            if episodeNumber.isdigit() == False:
                raise Exception("")
            episode = "ep"+episodeNumber
            data["file"]= data["date"]+"_"+episode+".txt"
            data["filepath"] = data["path"]+data["file"]
            loop = False
        except:
            print("Not a number")

    while True:
        os.system("cls")
        print("---MENU---")
        print("1) Get stats for shot")
        print("2) Get stats for all")
        print("3) Change episode to filter (currently : "+ episode +")")
        print("4) Change output stat file directory")
        print("5) Fix BATCHER environment variables")
        print("6) Fix PreComp environment variables")
        print("7) Remove 64GB Limit for layerCharsHair jobs")
        print("8) Help")
        print("9) Quit")
        print("\n")
        choice = int(input("Choice : "))

        if choice == 1:
            try:
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
                        frames = getFramesForJob(job)
                        jobTotalTaskRenderTime = stats.TotalTaskRenderTimeAsString
                        jobTotalTaskRenderTime = formatTime(jobTotalTaskRenderTime)
                        writeToFile(logFile, jobName, episode, job.JobComment, job.JobId, jobTotalTaskRenderTime, jobAVGFrameTime, frames)
                print("Done.\n")
                logFile.close()
                updateFile(episode)
                os.system("pause")
            except:
                print("Not a number")
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
                    frames = getFramesForJob(job)
                    writeToFile(logFile, jobName, episode, job.JobComment, job.JobId, jobTotalTaskRenderTime, jobAVGFrameTime, frames)
            print("Done.\n")
            logFile.close()
            os.system("pause")
        elif choice == 3:
            try:
                episodeNumber = raw_input("Episode number to filter : ")
                if episodeNumber.isdigit() == False:
                    raise Exception("")
                episode = "ep"+episodeNumber
                data["file"]= data["date"]+"_"+episode+".txt"
                data["filepath"] = data["path"]+data["file"]
            except:
                print("Not a number")
        elif choice == 4:
            print("Currently : " + data["filepath"])
            if((raw_input("Change? (y/n) : ")).lower() == 'y'):
                data["path"] = tkFileDialog.askdirectory() + "/"
                data["path"] = data["path"].replace("/", "\\")
                updateFile(episode)
        elif choice == 5:
            for job in RepositoryUtils.GetJobs(True):
                jobName = job.JobName
                if (episode in jobName or episode in job.JobComment) and "BATCHER" in jobName:
                    print("found job " + jobName)
                    job = RepositoryUtils.GetJob(job.JobId, True)
                    fixBATCHER(job)
            print("Done.")
            os.system("pause")
        elif choice == 6:
            for job in RepositoryUtils.GetJobs(True):
                jobName = job.JobName
                if (episode in jobName or episode in job.JobComment) and "preComp" in jobName:
                    print("found job " + jobName)
                    job = RepositoryUtils.GetJob(job.JobId, True)
                    fixPreComp(job)
            print("Done.")
            os.system("pause")
        elif choice == 7:
            for job in RepositoryUtils.GetJobs(True):
                if "VRAY_RENDER_layerCharsHair" in job.JobName:
                    job = RepositoryUtils.GetJob(job.JobId, True)
                    limit = list()
                    limit.append("vray4maya")
                    limit.append("64g")
                    job.SetJobLimitGroups(limit)
                    RepositoryUtils.SaveJob(job)
                    #limits = job.JobLimitGroups
                    #for line in limits:
                    #    print("(DEBUG) limit : " + line)
            print("Done")
            os.system("pause")

        elif choice == 8:
            os.system("cls")
            print("When prompted for episode or shot numbers, only enter the number (119 instead of ep119 or 1 instead of sh0001 for example)")
            print("By default, stat files are located in " + os.environ['USERPROFILE'] + "\\Documents\\")
            print("You can change that with option 4 which will open a window to select a new folder if you want to.")
            print("Options 5 and 6 will look for all the BATCHER/preComp jobs for the episode currently filtered and fix their environment variables.")
            print("\n")
            os.system("pause")
        elif choice == 9:
            os.system("cls")
            break
