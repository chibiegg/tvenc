# encoding=utf-8

import logging
import traceback
from django.core.management.base import BaseCommand
from tvenc.models import ChinachuServer, RecordedProgram, Channel, Program

import chinachu

class Command(BaseCommand):

    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)

        logger.info("Start fetch chinachu servers")

        for server in ChinachuServer.objects.filter(enabled=True):
            logger.info("Fetch ChinachuServer: %s", server.name)
            client = chinachu.Client(server.api_url, server.username, server.password)

            try:

                for program_data in client.get_recorded():
                    if RecordedProgram.objects.filter(program__program_id=program_data["id"]).exists():
                        # 登録済みなら無視する
                        continue

                    # 新規登録
                    logger.debug("New program %s", program_data["id"])
                    program = Program.from_chinachu(program_data)
                    recorded_program = RecordedProgram(program=program, server=server)
                    recorded_program.save()

            except Exception as e:
                logger.error(traceback.format_exc())








