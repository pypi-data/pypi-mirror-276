from logging.handlers import MemoryHandler
import requests
from .const import WorkflowTokenHeader


class ActivityLogHandler(MemoryHandler):
    def __init__(self, endpoint, token, *args, **kwargs):
        MemoryHandler.__init__(self, *args, **kwargs)
        self.token = token
        self.endpoint = endpoint

    def flush(self) -> None:
        self.acquire()
        try:
            if len(self.buffer) > 0:
                buf = [self.format(record) for record in self.buffer]
                resp = requests.post(self.endpoint, headers={
                    WorkflowTokenHeader: self.token,
                }, data='\n'.join(buf), timeout=5)

                if resp.status_code != 200:
                    print(f"Failed to send logs to {self.endpoint}, status code: {resp.status_code}, response: {resp.text}")
                self.buffer.clear()
        except Exception as e:
            print(f"Failed to send logs to {self.endpoint}, exception: {e}")
        finally:
            self.release()
