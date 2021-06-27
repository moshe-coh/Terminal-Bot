import asyncio


class Terminal:
    def __init__(self, process: asyncio.subprocess.Process) -> None:
        self._process = process
        self._stdout = b''
        self._stderr = b''
        self._stdout_line = b''
        self._stderr_line = b''
        self._finished = False

    def cancel(self) -> None:
        self._process.kill()

    @property
    def finished(self) -> bool:
        return self._finished

    @property
    def read_line(self) -> str:
        return (self._stdout_line + self._stderr_line).decode('utf-8').strip()

    @property
    def get_output(self) -> str:
        return (self._stdout + self._stderr).decode('utf-8').strip()

    async def _read_stdout(self) -> None:
        while True:
            line = await self._process.stdout.readline()
            if line:
                self._stdout_line = line
                self._stdout += line
            else:
                break

    async def _read_stderr(self) -> None:
        while True:
            line = await self._process.stderr.readline()
            if line:
                self._stderr_line = line
                self._stderr += line
            else:
                break

    async def worker(self) -> None:
        await asyncio.wait([self._read_stdout(), self._read_stderr()])
        await self._process.wait()
        self._finished = True

    @classmethod
    async def execute(cls, cmd: str):
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        t_obj = cls(process)
        asyncio.get_event_loop().create_task(t_obj.worker())
        return t_obj
