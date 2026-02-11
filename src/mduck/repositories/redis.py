import logging

import redis.asyncio as redis
from dependency_injector import resources

logger = logging.getLogger(__name__)


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
        logger.info("Connecting to Redis at %s:%s, db=%d", host, port, db)
        try:
            if await client.ping():  # type: ignore[misc]
                logger.info("Redis connected.")
            else:
                logger.error(
                    "Redis PING failed for %s:%s db=%d. "
                    "Connection established but server did not respond.",
                    host,
                    port,
                    db,
                )
        except Exception as exc:
            logger.error(
                "Failed to connect to Redis at %s:%s db=%s. Error: %s",
                host,
                port,
                db,
                exc,
                exc_info=True,
            )
            raise exc
        return client

    async def shutdown(self, client: redis.Redis | None) -> None:
        """
        Shutdown the Redis resource.

        Args:
            client: The Redis client to shutdown.

        """
        if client:
            await client.close()
