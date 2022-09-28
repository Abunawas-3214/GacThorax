import concurrent.futures
from threading import Thread

from ProgramUtama import GAC

class Process():
    def __init__(self, filename):
        self.filename = filename

        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()


    def run(self):
        self.segproc()

class MyWorker():

  def __init__(self, message):
    self.message = message

    thread = Thread(target=self.run, args=())
    thread.daemon = True
    thread.start()

  def run(self):
    print(f'run MyWorker with parameter {self.message}')


MyWorker('param value')
# t = Thread(target=Process('JPCLN001.jpg').run())
# t.start()