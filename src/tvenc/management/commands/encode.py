# encoding=utf-8

import logging
import threading
import traceback
import subprocess
import time
from django.core.management.base import BaseCommand
from django.conf import settings
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
                recorded_program = RecordedProgram.objects.filter(status=RecordedProgram.STATUS_NEW)[0]
            except IndexError:
                self.db_semaphore.release()
                time.sleep(10)
                continue

            recorded_program.status = RecordedProgram.STATUS_ENCODING
            recorded_program.save()
            self.db_semaphore.release()

            self.logger.info("Start Encoding ID:%d %s", recorded_program.id, recorded_program.program.program_id)

            try:
                server = recorded_program.server
                program = recorded_program.program
                input_file = "{0}/{1}".format(server.mountpoint, recorded_program.filename)
                output_file = recorded_program.filename.replace(".m2ts",".mp4")
                cd_cmd = "cd \"{0}\"".format(settings.ENCODED_DIR)
                encode_cmd = "HandBrakeCLI -i \"{0}\" -o \"{1}\"  -t 1 -c 1 -f mp4 --denoise=\"2:1.5:3:2.25\" -w 1280 -l 720 ".format(input_file, output_file)
                encode_cmd += "--crop 0:0:0:0 --modulus 2 -e x264 -r 29.97 --detelecine -q 21 -a 1 -E faac -6 stereo -R Auto -B 128 -D 0 "
                encode_cmd += "-x b-adapt=2:me=umh:merange=64:subq=10:trellis=2:ref=12:bframes=6:analyse=all:b-pyramid=strict:deblock=2,2 --verbose=1"

                cmd = "bash -c '{0}; {1}; exit $?'".format(cd_cmd, encode_cmd)
                result = subprocess.call(cmd, shell=True)
                if result == 0:
                    recorded_program.status = RecordedProgram.STATUS_ENCODED
                    recorded_program.save()
                    self.logger.info("Encoded Successful ID:%d %s", recorded_program.id, recorded_program.program.program_id)
                    continue

            except:
                self.logger.error("Encode Error ID:%d %s", recorded_program.id, recorded_program.program.program_id)
                self.logger.error(traceback.format_exc())
                recorded_program.status = RecordedProgram.STATUS_ENCODE_ERROR
                recorded_program.save()

















