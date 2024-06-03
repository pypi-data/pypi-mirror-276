## 一、简介

上传图片时，不同的场景，对图片的宽高有着不同的需求，而django自带的控件ImageField，无法对图片进行裁剪处理，导致上传的图片可能不符合需求。为此，我开发了一个拥有图片、裁剪上传功能的django控件**ImageCropField**。

**ImageCropField**继承了ImageField的同时，集成了图片裁剪插件[cropper.js](https://fengyuanchen.github.io/cropperjs/)。你仅需进行简单的配置，就可以非常方便的将**ImageCropField**与ModelForm、admin进行搭配使用。

## 二、安装
1. 环境配置
	| 名称   | 要求版本 | 建议版本 |
	| ------ | -------- | -------- |
	| python | ≥ 3.6    | 3.9      |
	| django | ≥ 3.0.0  | 4.2.13   |

2. 使用以下命令安装**django-image-crop**：

	```
	pip install django-image-crop
	```

3. 安装依赖库pillow（图形处理库）

	```
	pip install pillow
	```

## 三、配置

 - 在配置文件setting.py中引入**image-crop**
	```python
	# setting.py
	
	INSTALLED_APPS = [
	    ...
	    'image_crop'
	]
	```

 - 配置media路径与路由
	```python
	# setting.py
	
	MEDIA_URL = "/media/"
	MEDIA_ROOT = BASE_DIR / "media"
	```
	```python
	# urls.py
	
	from django.conf import settings
	from django.urls import re_path
	from django.views.static import serve
	
	urlpatterns = [
	    ...
	    re_path(r'media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT})
	]
	```
## 四、使用
 1. 应用到django admin当中
	```python
	# app/model.py
	
	from django.db import models
	from image_crop import ImageCropField
	
	
	class ImageCrop(models.Model):
	    image = ImageCropField(blank=True, upload_to="images", verbose_name='上传图片')
	    
	    class Meta:
	        verbose_name = "图片列表"
	        verbose_name_plural = verbose_name
	```
	```python
	# app/admin.py
	
	from django.contrib import admin
	from .models import ImageCrop
	
	
	@admin.register(ImageCrop)
	class ImageCropModelAdmin(admin.ModelAdmin):
	    list_display = ["id", "image"]
	```

2. 应用到ModelForm
	```python
	# app/forms.py

	from django import forms
	from .models import ImageCrop
	
	
	class ImageCropModelForm(forms.ModelForm):
	    class Meta:
	        model = ImageCrop
	        fields = "__all__"
	```
	```python
	# app/views.py

	from django.shortcuts import render
	from .forms import ImageCropModelForm
	
	
	def test(request):
	    objs = ImageCropModelForm()
	
	    if request.method == "POST":
	        print(request.FILES)
	        form = ImageCropModelForm(request.POST, request.FILES)
	        if form.is_valid():
	            form.save()
	
	    return render(request, "ImageCrop.html", {"objs": objs})
	```
	```html
	<!-- app/templates/ImageCrop.html -->
	
	<!DOCTYPE html>
	<html lang="en">
	  <head>
	    <meta charset="UTF-8">
	    <title>ImageCrop</title>
	  </head>
	  <body>
	    <form method="post" enctype="multipart/form-data">
	      {% csrf_token %}
	      {{ objs.as_div }}
	      <div>
	        <input type="submit" class="btn btn-success" value="提交">
	      </div>
	    </form>
	  </body>
	</html>
	```
	```python
	# urls.py

	from django.urls import path
	from app import views
	
	urlpatterns = [
		...
	    path("image_crop/", views.test),
	]
	```

 3. ImageCropField内置参数

    - aspect_ratio（裁剪横纵比）

      ```python
      ImageCropField(blank=True, upload_to="images", verbose_name='上传图片',
      				   aspect_ratio=[(1, 1), (2, 1)])
      ```

      

    - max_size（裁剪大小限制）

      ```python
      ImageCropField(blank=True, upload_to="images", verbose_name='上传图片',
      					   aspect_ratio=[(1, 1), (2, 1)], max_size=2000)
      ```

4. 图片格式的选择
		**ImageCropField**提供了JPG、PNG两种图片格式的选择。若选择JPG格式，裁剪超出图片区域的部分会以黑色背景代替；若选择PNG格式，裁剪超出图片区域的部分会以透明背景代替，但裁剪出图片大小会比原图大出不少，请安需求选择。