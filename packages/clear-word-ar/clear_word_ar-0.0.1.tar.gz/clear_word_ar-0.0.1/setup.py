from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "/home/slver/Bots/Clear-Word-Ar/README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Arabic text filtering for inappropriate words | تصفية النصوص العربية من الكلمات غير اللائقة'
LONG_DESCRIPTION = 'A package that helps filter out inappropriate words, emojis, and repeated characters from Arabic text. | حزمة تساعد على تصفية الكلمات غير اللائقة، الإيموجيات، والحروف المتكررة من النصوص العربية.'

# Setting up
setup(
    name="clear_word_ar",
    version=VERSION,
    author="Saleh",
    author_email="<your_email@example.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'text', 'filter', 'arabic', 'text filter', 'bad words', 'emoji removal', 'بايثون', 'نص', 'تصفية', 'عربي', 'تصفية النصوص', 'كلمات سيئة', 'إزالة الإيموجيات', 'تنظيف النصوص', 'تطبيق', 'تحليل نصوص', 'بيانات نصية'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ]
)
