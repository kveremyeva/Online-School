import re
from rest_framework.serializers import ValidationError


class YouTubeURLValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile(r'^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$')
        tmp_val = dict(value).get(self.field)
        if tmp_val and not reg.match(tmp_val):
            raise ValidationError("Разрешены только ссылки на YouTube (youtube.com или youtu.be)")
