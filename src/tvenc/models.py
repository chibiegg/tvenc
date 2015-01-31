# encoding=utf-8
from django.db import models
import datetime
import logging

class ChinachuServer(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = "ちなちゅサーバ"

    name = models.CharField("名称", max_length=100)
    description = models.TextField("説明", blank=True)

    api_url = models.CharField("API URL", max_length=100)
    username = models.CharField("ユーザー名", max_length=100)
    password = models.CharField("パスワード", max_length=100)
    mountpoint = models.CharField("録画ファイルディレクトリ", max_length=200)

    enabled = models.BooleanField("有効", blank=True, default=True)
    encode_enabled = models.BooleanField("エンコード有効", blank=True, default=True)

    created_at = models.DateTimeField("登録日時", auto_now_add=True)
    updated_at = models.DateTimeField("最終更新日時", auto_now=True)

    def __str__(self):
        return self.name

class Channel(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = "チャンネル"

    channel_id = models.CharField("チャンネルID", max_length=20, unique=True)
    type = models.CharField("種別", max_length=10)
    channel = models.CharField("チャンネル", max_length=20)
    sid = models.IntegerField("SID")
    name = models.CharField("名称", max_length=200, blank=True)
    region = models.CharField("地域", max_length=20, blank=True)

    def __str__(self):
        return "[{0}{1}] {2}".format(self.type, self.channel, self.name)

    @classmethod
    def from_chinachu(cls, data):
        model_data = {
                      "channel_id":data["id"],
                      "type":data["type"],
                      "channel":data["channel"],
                      "sid":int(data["sid"]),
                      "name":data["name"]
                      }
        instance, created = cls.objects.get_or_create(channel_id=data["id"], defaults=model_data)
        if not created:
            instance.__dict__.update(model_data)
            instance.save()
        else:
            logging.getLogger(__name__).debug("Create Channel ID:%d %s", instance.id , instance.channel_id)
        return instance


class Program(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = "番組情報"

    program_id = models.CharField("プログラムID", max_length=20, unique=True)
    channel = models.ForeignKey(Channel)
    category = models.CharField("カテゴリ", max_length=20, blank=True)
    title = models.CharField("タイトル", max_length=100, blank=True)
    sub_title = models.CharField("サブタイトル", max_length=100, blank=True)
    full_title = models.CharField("フルタイトル", max_length=100, blank=True)
    detail = models.TextField("詳細", blank=True)
    episode = models.IntegerField("話数", blank=True, null=True)
    start = models.DateTimeField("開始日時", blank=True, null=True)
    end = models.DateTimeField("終了日時", blank=True, null=True)
    seconds = models.IntegerField("放送時間(秒)", blank=True, null=True)

    def __str__(self):
        return "{0} {1}".format(self.channel.name, self.title)

    @classmethod
    def from_chinachu(cls, data):
        channel = Channel.from_chinachu(data["channel"])
        model_data = {
                      "program_id":data["id"],
                      "channel":channel,
                      "category":data["category"],
                      "title":data["title"],
                      "sub_title":data["subTitle"],
                      "full_title":data["fullTitle"],
                      "detail":data["detail"],
                      "episode":int(data["episode"]) if data["episode"] else None,
                      "start":datetime.datetime.fromtimestamp(int(data["start"]) / 1000),
                      "end":datetime.datetime.fromtimestamp(int(data["end"]) / 1000),
                      "seconds":int(data["seconds"])
                      }
        instance, created = cls.objects.get_or_create(program_id=data["id"], defaults=model_data)
        if not created:
            instance.__dict__.update(model_data)
            instance.save()
        else:
            logging.getLogger(__name__).debug("Create Program ID:%d %s", instance.id , instance.program_id)
        return instance

class RecordedProgram(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = "録画済番組"

    program = models.ForeignKey(Program)
    server = models.ForeignKey(ChinachuServer)

    STATUS_NEW = 101
    STATUS_ENCODING = 102
    STATUS_ENCODE_ERROR = 200
    STATUS_ENCODED = 400
    STATUS_DELETED = 500
    STATUS_CHOICES = (
                     (STATUS_NEW, "新規"),
                     (STATUS_ENCODING, "エンコード中"),
                     (STATUS_ENCODED, "エンコード完了"),
                     (STATUS_ENCODE_ERROR, "エンコード失敗"),
                     (STATUS_DELETED, "削除済み")
                     )

    worker = models.CharField("エンコーダ", max_length=100, blank=True)
    status = models.IntegerField("ステータス", choices=STATUS_CHOICES, default=STATUS_NEW)
    filename = models.CharField("ファイル名", max_length=200)

    start_encode = models.DateTimeField("エンコード開始時刻", blank=True, null=True)
    end_encode = models.DateTimeField("エンコード完了時刻", blank=True, null=True)
    encoded_file = models.FilePathField("エンコード済みファイル", max_length=255, blank=True)

    def __str__(self):
        return self.program.__str__()

