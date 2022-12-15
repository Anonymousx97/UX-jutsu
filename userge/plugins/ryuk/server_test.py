async def _init():
    import asyncio
    await asyncio.create_subprocess_shell("python server.py")
