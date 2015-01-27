# encoding=utf-8

import logging
import threading
import traceback
import subprocess
import time
from django.core.management.base import BaseCommand

import chinachu
from optparse import make_option
from tvenc.models import RecordedProgram

class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        self.option_list = BaseCommand.option_list + (
                                                      make_option('--threads', help='Number of threads', type='int', default=1),
                                                      )
        super(Command, self).__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)
        self.db_semaphore = threading.Semaphore()


    def handle(self, *args, **options):

        self.threads = []
        for i in range(options["threads"]):
            thread = threading.Thread(target=self.encode_job, name="Encode Thread:{0}".format(i))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

        while True:
            time.sleep(10)

    def encode_job(self):
        """ エンコードスレッド """
        while True:
            self.db_semaphore.acquire()
            try:
                recored_program = RecordedProgram.objects.filter(status=RecordedProgram.STATUS_NEW)[0]
            except IndexError:
                self.db_semaphore.release()
                time.sleep(10)
                continue

            recored_program.status = RecordedProgram.STATUS_ENCODING
            recored_program.save()
            self.db_semaphore.release()

            self.logger.info("Start Encoding ID:%d %s", recored_program.id, recored_program.program.program_id)








            time.sleep(10)



















