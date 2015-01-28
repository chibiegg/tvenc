# encoding=utf-8

from django.contrib import admin
from tvenc.models import ChinachuServer, Channel, Program, RecordedProgram

class ChinachuServerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "api_url")

admin.site.register(ChinachuServer, ChinachuServerAdmin)

class ChannelAdmin(admin.ModelAdmin):
    list_display = ("id", "region", "type", "channel", "name")

admin.site.register(Channel, ChannelAdmin)


class ProgramAdmin(admin.ModelAdmin):
    list_display = ("id", "start", "channel", "title")

admin.site.register(Program, ProgramAdmin)


class RecordedProgramAdmin(admin.ModelAdmin):
    list_display = ("id", "server", "program", "status")

admin.site.register(RecordedProgram, RecordedProgramAdmin)

