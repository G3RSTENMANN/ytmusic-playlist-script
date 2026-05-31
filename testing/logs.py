import sys, os

path = "testing/log.txt"
os.remove(path)

def log(txt):
    with open(path, "a") as f:
        print(txt, file=f)
    print(txt)


log(f"Completed Download of song with index 003!")
log("------------------------------------------")
log(f"Number of current errors: 1.")
log("\nSOMETHING WENT WRONG WITH EXECUTING THE COMMAND!!!\n")
log(f"Beginning download of next song...\n")
log("\n-------------------------------------------------------\n")
log(f"Process finished with a total of 1 errors.\n")
log("-------------------------------------------------------\n\n")
log("\nFinished Backup!")
