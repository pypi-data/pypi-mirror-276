import aio_pika
import aio_pika.exceptions
import asyncio
import importlib.metadata
import logging
import weakref


logger = logging.getLogger(__name__)

_connect_lock = asyncio.Lock()
_connections = weakref.WeakValueDictionary()


async def get_connection(connection_string, service_name="?"):
    connection_url = aio_pika.connection.make_url(connection_string)
    if not connection_url.query.get("name"):
        package_name = __package__.split(".")[0]
        package_name_version = importlib.metadata.version(package_name)

        connection_url %= {
            "name": f"{service_name} ({package_name} v{package_name_version})"
        }

    async with _connect_lock:
        connection = _connections.get(connection_url)
        if connection is None:
            connection = await aio_pika.connect_robust(connection_url)
            _connections[connection_url] = connection

    return connection
