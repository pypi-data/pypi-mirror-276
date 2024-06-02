import shutil
import pathlib
import os
import subprocess
import sys
from datetime import datetime
import logging

logging.basicConfig(
    format="%(asctime)s %(message)s",
    filename="/tmp/jsoniq-language-server-entrypoint.log",
    level=logging.INFO,
)
cwd = os.getcwd()

NODE_LOCATION = (
    shutil.which("node") or shutil.which("node.exe") or shutil.which("node.cmd")
)
NODE = str(pathlib.Path(NODE_LOCATION).resolve())
PATH_TO_BIN_JS = str(
    (
        pathlib.Path(__file__).parent
        / "node_modules"
        / "jsoniq-language-server"
        / "dest"
        / "server.js"
    ).resolve()
)


def main():
    # Run the language server
    logging.info(f"Starting language server...")
    server_proc = subprocess.Popen(
        [NODE, PATH_TO_BIN_JS, "--stdio", *sys.argv[1:]],
        stdin=sys.stdin,
        stdout=sys.stdout,
    )
    logging.info(f"Running language server...")
    logging.info(f"Process pid: {server_proc.pid}")
    sys.exit(server_proc.wait())


if __name__ == "__main__":
    main()
