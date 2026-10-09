from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="ชื่องาน")
    description = models.TextField(blank=True, null=True, verbose_name="รายละเอียด")
    start_time = models.DateTimeField(verbose_name="เวลาเริ่ม")
    end_time = models.DateTimeField(verbose_name="เวลาสิ้นสุด")

    def __str__(self):
        return self.title
