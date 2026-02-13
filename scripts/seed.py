from backend.scripts.seed import seed

if __name__ == "__main__":
    import asyncio

    asyncio.run(seed())
