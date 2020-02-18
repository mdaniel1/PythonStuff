#v1.03, by Daniel Martin
#in collaboration with Raphael Jouretz

from Deadline.Scripting import *
import os

def __main__(*args):
    deadlinePlugin = args[0]
    deadlinePlugin.LogInfo("---[STARTING PRE-TASK SCRIPT]---")
    deadlinePlugin.LogStdout("OS is " + os.name)
    deadlinePlugin.LogStdout("DEBUG : Current task ID is {}".format(deadlinePlugin.GetCurrentTaskId()))
    
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
