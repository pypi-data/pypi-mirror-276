## 简介

上传图片文件时，不同的场景，对图片的宽高有着不同的需求，而`django`自带的控件`ImageField`，无法对图片进行裁剪处理，导致上传的图片可能不符合需求。因此，为方便开发，我自定义了一个拥有图片裁剪、上传功能的`django`控件`ImageCropField`。

`ImageCropField`继承了`ImageField`的同时，集成了图片裁剪插件[cropper.js](https://fengyuanchen.github.io/cropperjs/)。你仅需进行简单的配置，就可以非常方便的将`ImageCropField`与`ModelForm`、`admin`进行搭配使用。

## 安装

1. 使用以下命令安装django-image-crop：

   ```
   pip install django-image-crop
   ```

2. 安装依赖库pillow（图形处理库）

   ```
   pip install pillow
   ```

## 配置

1. 在配置文件setting.py中引入`django-image-crop`

   *setting.py*
   
   ```python
   INSTALLED_APPS = [
       ...
       'image_crop'
   ]
   ```

2. 配置media路径与路由

   *setting.py*

   ```python
   MEDIA_URL = "/media/"
   MEDIA_ROOT = BASE_DIR / "media"
   ```

   urls.py*

   ```python
   from django.conf import settings
   from django.urls import re_path
   from django.views.static import serve
   
   urlpatterns = [
       ...
       re_path(r'media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT})
   ]
   ```

## 使用

*model.py*

```python
from django.db import models
from image_crop import ImageCropField


class ImageCrop(models.Model):
    image = ImageCropField(blank=True, upload_to="images", verbose_name='上传图片')
```