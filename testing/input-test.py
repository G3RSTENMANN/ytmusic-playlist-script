import sys, asyncio

async def read_stdin():
    reader = asyncio.StreamReader(sys.stdin)

    while True:
        try:
            line = await reader.readline()
            if not line:
                break
            line = line.decode().rstrip()
            print(f"Received {line}")
        except Exception as e:
            print(f"Error reading stdin: {e}")
            break

async def main():
    await read_stdin()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nProgram terminated by user")
