from django.db import models

from .fields import ImageCropField


class ImageCrop(models.Model):
    image = ImageCropField(blank=True, upload_to="images",
                           verbose_name='上传图片', max_size=2000,
                           aspect_ratio=[(1, 1), (35, 24), (34, 21)])

    class Meta:
        db_table = "images"
        verbose_name = "图片列表"
        verbose_name_plural = verbose_name
