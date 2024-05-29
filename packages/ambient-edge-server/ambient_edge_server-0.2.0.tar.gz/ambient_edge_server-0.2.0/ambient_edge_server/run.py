import os
import sys

import uvicorn


def run():
    print(f"sys.path: {sys.path}    os.getcwd(): {os.getcwd()}")
    try:
        from ambient_edge_server.app import app
        from ambient_edge_server.utils import logger

        logger.debug("running server ...")
        logger.debug("running app: %s ...", app)
        uvicorn.run(app, host="0.0.0.0", port=7417)
    except Exception as e:
        print("error running server: %s", e)


if __name__ == "__main__":
    run()
