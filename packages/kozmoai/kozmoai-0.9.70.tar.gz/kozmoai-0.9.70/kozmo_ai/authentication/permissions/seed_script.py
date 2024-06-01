import asyncio

from kozmo_ai.authentication.permissions.seed import bootstrap_permissions
from kozmo_ai.orchestration.db import db_connection

if __name__ == '__main__':
    db_connection.start_session()

    asyncio.run(bootstrap_permissions())
