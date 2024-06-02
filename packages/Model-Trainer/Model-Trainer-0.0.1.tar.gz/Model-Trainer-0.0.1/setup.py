from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Simplify YOLO model training and data splitting for object detection tasks.'
LONG_DESCRIPTION = 'Model_Trainer is a Python package designed to simplify the process of training YOLO (You Only Look Once) models for object detection tasks. With Model_Trainer, users can easily train YOLO models using custom datasets and split their data into training, validation, and testing sets. The package provides classes for both model training and data splitting, allowing users to efficiently manage their training pipeline. Additionally, Model_Trainer includes functionality for saving the best-performing model weights, making it easy to deploy trained models for inference tasks.'
# Setting up
setup(
    name="Model-Trainer",
    version=VERSION,
    author="Atri Rathore",
    author_email="<rathoreatri@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/Rathoreatri03/Model_Trainer",
    packages=find_packages(),
    install_requires=['torch', 'ultralytics'],
    keywords=['python', 'model training', 'YOLO', 'data splitting', 'deep learning'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)