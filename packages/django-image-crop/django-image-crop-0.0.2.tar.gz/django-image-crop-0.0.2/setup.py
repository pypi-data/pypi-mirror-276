import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-image-crop",
    version="0.0.2",
    author="bj.tr",
    author_email="bj.t@foxmail.com",
    description="Image cropping plugin, can be directly applied to django admin.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    keyword=["django-image-crop", "django", "image", "crop", "cropper"],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 5.0",
    ],
)