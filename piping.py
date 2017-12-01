
import asyncio

from util import async_pipe, PipeClosed


class PipeManager:

    def __init__(self, loop=None):
        self._loop = loop or asyncio.get_event_loop()

    @property
    def loop(self):
        return self._loop

    @staticmethod
    def run_future(func, futr, *args, **kwargs):
        return futr.set_result(func(*args, **kwargs))

    @staticmethod
    async def _stdout(inpipe, callback, out):
        try:
            while 1:
                x = await inpipe.recv()
                out.append(x)
                if callback is not None:
                    callback(x)
        except PipeClosed:
            pass  # print("pipe ended")
        finally:
            inpipe.close()

    async def run_pipe(self, cmds_args, callback=None, collector=lambda x: x, err_callback=None, timeout=15, loop=None):
        tasks = []
        out = []

        next, first = async_pipe()
        for func, args in cmds_args:
            next3, next2 = async_pipe(loop=loop)
            tasks.append(asyncio.ensure_future(func(args, next, next2),loop=loop if loop is not None else self.loop))
            next = next3

        tasks.append(self._stdout(next, callback, out))
        first.close()

        _= asyncio.gather(*tasks, loop=loop if loop is not None else self.loop, return_exceptions=True)

        try:
            x = await asyncio.wait_for(_, timeout=timeout, loop=loop if loop is not None else self.loop)
            return out, x
        except asyncio.TimeoutError:
            _.cancel()
            raise TimeoutError()


class PipeError(Exception):
    def __init__(self, exs):
        self.exs = exs
