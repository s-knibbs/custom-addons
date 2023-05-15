#!/usr/bin/python3
from __future__ import annotations
from aiohttp import web
import os
import asyncio
from traceback import print_exc
from asyncio.subprocess import PIPE, Process

MODEL_FILE = os.environ.get('MODEL_FILE', '/usr/share/piper/en-us-ryan-medium.onnx')
PIPER_EXE = os.environ.get('PIPER_EXE', '/usr/share/piper/piper')
try:
    LENGTH_SCALE = float(os.environ.get("LENGTH_SCALE"))
except ValueError:
    print_exc()
    LENGTH_SCALE = None

async def start_piper(length_scale: float | None = None) -> Process:
    args = ["-m", MODEL_FILE, '--output_dir', '/tmp']
    if length_scale is not None:
        args.extend(['--length-scale', "{:0.3}".format(length_scale)])
    return await asyncio.create_subprocess_exec(
        PIPER_EXE,
        *args,
        stdin=PIPE,
        stdout=PIPE,
        stderr=None,
    )


async def tts(request: web.Request):
    piper: Process = request.app['piper']
    piper_lock: asyncio.Lock = request.app['piper_lock']
    message = request.query.get('message')
    async with piper_lock:
        piper.stdin.write(f"{message}\n".encode())
        await piper.stdin.drain()
        output_path = (await piper.stdout.readline()).decode().strip()
        loop = asyncio.get_event_loop()
        # TODO: Is there a better way to do this?
        loop.call_later(10, os.unlink, output_path)
        return web.FileResponse(output_path, headers={'content-type': 'audio/wav'})



async def init() -> web.Application:
    app = web.Application()
    app.add_routes([web.get('/tts', tts)])
    app['piper'] = await start_piper(LENGTH_SCALE)
    app['piper_lock'] = asyncio.Lock()
    return app


if __name__ == "__main__":
    web.run_app(init(), port=5000)