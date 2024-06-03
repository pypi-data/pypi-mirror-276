from django.db import models
from .widgets import ImageCropInput


class ImageCropField(models.ImageField):
    def __init__(
            self,
            verbose_name=None,
            name=None,
            aspect_ratio=None,
            max_size=None,
            **kwargs,
    ):
        self.aspect_ratio = aspect_ratio
        self.max_size = max_size
        super().__init__(verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = ImageCropInput(aspect_ratio=self.aspect_ratio, max_size=self.max_size)
        return super().formfield(**kwargs)
