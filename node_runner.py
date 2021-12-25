import os
import subprocess
import atexit
from args import AUTO_RUN_NODE


ENTRY_PATH = os.path.join(
    os.getcwd(),
    'index.js'
)
NODE_SETS = {
    'PID': 0,
    'POLL': (lambda: print('ERROR: nodejs not started'))
}


def kill_node() -> None:
    if bool(NODE_SETS['POLL']()) or NODE_SETS['PID'] == 0:
        return
    os.kill(
        NODE_SETS['PID'],
        0
    )
    NODE_SETS['PID'] = 0


def run_node(auto_run_node: bool = AUTO_RUN_NODE) -> None:
    if not auto_run_node:
        return
    process = subprocess.Popen([
        'node',
        ENTRY_PATH
    ])
    NODE_SETS['PID'] = process.pid
    NODE_SETS['POLL'] = process.poll
    atexit.register(kill_node)
