import subprocess, asyncio, time

def main():
    while True:
        try:
            result = subprocess.run("echo bomba", check=True, shell=True, capture_output=True)
            print(result.stdout.decode("utf-8"))
        except:
            print("something went wrong")
        # time.sleep(0.5)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nProgram terminated by user")