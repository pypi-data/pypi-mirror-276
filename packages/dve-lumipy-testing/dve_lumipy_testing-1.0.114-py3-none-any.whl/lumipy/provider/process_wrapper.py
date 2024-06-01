import subprocess as sp
from threading import Thread
import sys


class ProcessWrapper:
    def __init__(self, cmd):
        self.process_thread = None
        self.cmd = cmd
        self.process = None
        self.stdout_thread = None
        self.stderr_thread = None
        self.starting = True
        self.expired_certificates = False

        self.ssl_expiry = 'Client side SSL Certificate is PAST its expiry'
        self.providers_running = 'Running! Hit Ctrl+C to shut down services'
        self.kafka_warning = 'kafka'

    def start_process(self):
        self.process_thread = Thread(target=self._run_process)
        self.process_thread.start()

    def _run_process(self):
        self.process = sp.Popen(self.cmd.split(), shell=False, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True, bufsize=1)

        self.stdout_thread = Thread(target=self.__print_stdout)
        self.stderr_thread = Thread(target=self.__print_stderr)

        self.stdout_thread.start()
        self.stderr_thread.start()

        self.stdout_thread.join()
        self.stderr_thread.join()

    def __print_stdout(self):
        for line in iter(self.process.stdout.readline, ''):
            if line:
                print(line.rstrip())
                if self.providers_running in line:
                    self.starting = False

                if self.ssl_expiry in line:
                    self.starting = False
                    self.expired_certificates = True

    def __print_stderr(self):
        for line in iter(self.process.stderr.readline, ''):
            if line:
                if self.kafka_warning in line:
                    continue
                print(line.rstrip(), file=sys.stderr)
