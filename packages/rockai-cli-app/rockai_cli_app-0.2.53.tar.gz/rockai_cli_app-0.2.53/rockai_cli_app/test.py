import asyncio
from rockai_cli_app import Client


# Run a image generation model using asyncio
async def main():
    input = {"prompt": "a cartoon of a IRONMAN fighting with HULK, wall painting"}
    client = Client(api_token="<API_TOKEN_HERE>")
    result = await client.run_async(
        version="001bb81139b01780380407b4106ac681df46108e002eafbeb9ccb2d8faca42e1",
        input=input,
    )
    print("Result:", result)


# Run the main function using asyncio.run
if __name__ == "__main__":
    asyncio.run(main())
