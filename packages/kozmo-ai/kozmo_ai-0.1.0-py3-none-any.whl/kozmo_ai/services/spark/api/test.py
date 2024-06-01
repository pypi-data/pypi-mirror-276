import asyncio

from kozmo_ai.services.spark.api.local import LocalAPI

if __name__ == '__main__':
    print(
        asyncio.run(LocalAPI().applications()),
    )
