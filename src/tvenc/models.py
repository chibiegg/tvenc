# encoding=utf-8
from django.db import models

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
    channel = models.IntegerField("チャンネル")
    sid = models.IntegerField("SID")
    name = models.CharField("名称", max_length=200, blank=True)
    region = models.CharField("地域", max_length=20, blank=True)

    def __str__(self):
        return "[{0}{1}] {2}".format(self.type, self.channel, self.name)


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
    start = models.DateTimeField("開始日時", blank=True, null=True)
    end = models.DateTimeField("終了日時", blank=True, null=True)
    seconds = models.IntegerField("放送時間(秒)", blank=True, null=True)

    def __str__(self):
        return "{0} {1}".format(self.channel.name, self.title)


class RecordedProgram(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = "録画済番組"

    program = models.ForeignKey(Program)
    server = models.ForeignKey(ChinachuServer)

    STATUS_NEW = 101
    STATUS_ENCODING = 102
    STATUS_ENCODED = 400
    STATUS_DELETED = 500
    STATUS_CHOICES = (
                     ("新規", STATUS_NEW),
                     ("エンコード中", STATUS_ENCODING),
                     ("エンコード完了", STATUS_ENCODED),
                     ("削除済み", STATUS_DELETED)
                     )

    status = models.IntegerField("ステータス", choices=STATUS_CHOICES, default=STATUS_NEW)

    start_encode = models.DateTimeField("エンコード開始時刻", blank=True, null=True)
    end_encode = models.DateTimeField("エンコード完了時刻", blank=True, null=True)
    encoded_file = models.FilePathField("エンコード済みファイル", max_length=255, blank=True)

    def __str__(self):
        return self.program.__str__()



