import os
import time
from concurrent.futures import ProcessPoolExecutor

from dynatrace_extension import Extension


class Mass(Extension):
    def initialize(self):
        with ProcessPoolExecutor(max_workers=4) as metric_executor:
            f = metric_executor.submit(self.thing)
        print(f.result())

    @staticmethod
    def thing():
        time.sleep(5)
        current_pid = os.getpid()
        with open(r"D:\workspace\repos\github\dt-extensions-python-sdk\test.txt", "w") as f:
            f.write(f"Hello, world! {current_pid}")

if __name__ == "__main__":
    m = Mass()
    m.run()
