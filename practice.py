
# from contextlib import asynccontextmanager


# First Step:

# with open("data.txt", "r") as file:
#     lines = file.readlines()
#     print(lines)


# with open("data.txt", "w") as file:
#     lines = file.write("I am learning Python.\n") 
#     print(lines)


# with open("output.txt", "w") as file:
#     lines = file.write("I am learning Python.\n")
#     print(lines)


# with open("data.txt", "r") as file, open("output.txt", "w") as output_file:
#     lines = file.read()
#     output_file.write(lines.upper())
#     print(lines, "data written in out.txt")  # Print each line without extra newline characters





# ---------------------------------Second Step:




# we are doing this for context management

# @asynccontextmanager
# async def make_connection(name):
#     print(f"Making connection...{name}")
#     yield name  
#     print(f"Connection made! {name}")

# async def main():
#     async with make_connection("A") as a:
#         print(f"Using connection: {a}")
#     print("Connection closed.")    

# asyncio.run(main())    




# ----------------------------- Third Step:



import asyncio
from contextlib import AsyncExitStack


async def get_connection(name):
    class ctx:
        async def __aenter__(self):
            print(f"ENTER...{name}")
            return name
        async def __aexit__(self, exc_type, exc_value, traceback):
            print(f"EXIT! {name}")
    return ctx()        


#  First Step:

# async def main():
#     async with await get_connection("A") as a:
#         async with await get_connection("B") as b:
#             print(f"Using connection: {a} and {b}")
#     print("Connection closed.")



# second Step:


# async def main():
#     async with AsyncExitStack() as stack:
#         a = await stack.enter_async_context(await get_connection("A"))
#         b = await stack.enter_async_context(await get_connection("B"))
#         print(f"Using connection: {a} and {b}")
#     print("Connection closed.")

# asyncio.run(main())    


# --------------------------------- Fourth Step:

async def main():
    async with AsyncExitStack() as stack:
        a = await stack.enter_async_context(await get_connection("A"))
        if a == "A":
          b = await stack.enter_async_context(await get_connection("B"))
          print(f"Using connection: {a} and {b}")


        async def custom_cleanup():
             print("Custom cleanup logic here.")
             
        stack.push_async_callback(custom_cleanup)
        print(f"Doing with {a} and {b if 'b' in locals() else 'no B'}" )


asyncio.run(main())    