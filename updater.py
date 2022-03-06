import os
import requests


LIBV86_URL = 'https://github.com/copy/v86/releases/download/latest/libv86.js'
WASM_URL = 'https://github.com/copy/v86/releases/download/latest/v86.wasm'
WASM_FALLBACK_URL = 'https://github.com/copy/v86/releases/download/latest/v86-fallback.wasm'
BUILD_DIR = os.path.join(
    os.getcwd(),
    'build'
)
BUILD_DIR_EXISTS = os.path.isdir(BUILD_DIR)


def update(need_update: bool) -> None:
    if not need_update and BUILD_DIR_EXISTS:
        return
    if not BUILD_DIR_EXISTS:
        os.mkdir(BUILD_DIR)
    for url in [LIBV86_URL, WASM_URL, WASM_FALLBACK_URL]:
        fn = url.split('/')[-1]
        file_path = os.path.join(
            BUILD_DIR,
            fn
        )
        resp = requests.get(url)
        f = open(file_path, 'wb')
        if url == LIBV86_URL:
            f.write(b'const ImageData = require(\'canvas\').ImageData')
        f.write(resp.content)
        f.close()
