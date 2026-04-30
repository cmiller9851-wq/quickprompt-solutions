import asyncio
import random
from datetime import datetime

class Wormhole:
    """A class simulating a data wormhole between endpoints."""
    def __init__(self):
        self.queue = asyncio.Queue()

    async def produce(self):
        """Producer generates tasks."""
        for i in range(10):
            task = {
                "id": i,
                "timestamp": datetime.utcnow().isoformat(),
                "value": random.randint(1, 100),
            }
            await self.queue.put(task)
            print(f"Produced: {task}")
            await asyncio.sleep(random.uniform(0.1, 0.5))

    async def consume(self):
        """Consumer processes tasks."""
        while True:
            task = await self.queue.get()
            print(f"Consumed: {task}")
            await asyncio.sleep(random.uniform(0.2, 0.6))

async def main():
    wormhole = Wormhole()
    producer = asyncio.create_task(wormhole.produce())
    consumer = asyncio.create_task(wormhole.consume())
    await asyncio.gather(producer, consumer)

if __name__ == "__main__":
    asyncio.run(main())
