# -*- coding: UTF-8 -*-
"""
@Project  : admin_ckeditor
@File     : widgets.py
@IDE      : PyCharm
@Author   : Tan Jianbin
@Email    : bj.t@foxmail.com
@Date     : 2024/5/23 8:56
@Function :
"""
from django.template import loader
from django.forms import ClearableFileInput
from django.utils.safestring import mark_safe


class ImageCropInput(ClearableFileInput):
    template_name = "image_crop.html"

    def __init__(self, aspect_ratio=None, max_size=None, *args):
        self.aspect_ratio = aspect_ratio
        self.max_size = max_size
        super().__init__(*args)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['aspect_ratio'] = self.aspect_ratio
        context['max_size'] = self.max_size
        return context

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)
