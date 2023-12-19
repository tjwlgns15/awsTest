from django.db import models

class Data(models.Model):
    id = models.AutoField(primary_key=True)
    temp = models.FloatField()
    sound = models.FloatField()
    light = models.FloatField()
    time_stamp = models.DateTimeField()

    class Meta:
        managed = False  # 데이터베이스 테이블은 Django에서 관리되지 않음
        db_table = 'TESTtb'  # 데이터베이스 테이블의 이름
