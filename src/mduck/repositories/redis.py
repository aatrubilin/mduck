import redis.asyncio as redis
from dependency_injector import resources


class RedisResource(resources.AsyncResource[redis.Redis]):
    """A resource for interacting with a Redis server."""

    async def init(
        self,
        host: str,
        port: int,
        db: int,
        password: str | None = None,
    ) -> redis.Redis:
        """
        Initialize the Redis resource.

        Args:
            host: The Redis server host.
            port: The Redis server port.
            db: The Redis database number.
            password: The password for the Redis server.

        Returns:
            An initialized Redis client.

        """
        pool = redis.ConnectionPool(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True,
        )
        client = redis.Redis(connection_pool=pool)
        return client

    async def shutdown(self, client: redis.Redis | None) -> None:
        """
        Shutdown the Redis resource.

        Args:
            client: The Redis client to shutdown.

        """
        if client:
            await client.close()
