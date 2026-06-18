import asyncio


class AgentScheduler:

    def __init__(self):

        self.active_tasks = []

    async def schedule(self, coro):

        task = asyncio.create_task(coro)

        self.active_tasks.append(task)

        return await task

    async def wait_all(self):

        if self.active_tasks:

            await asyncio.gather(*self.active_tasks)