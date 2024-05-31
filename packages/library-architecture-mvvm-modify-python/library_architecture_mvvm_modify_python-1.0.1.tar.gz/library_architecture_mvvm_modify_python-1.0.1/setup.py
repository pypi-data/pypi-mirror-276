import io
from setuptools import setup

setup(
    name="library_architecture_mvvm_modify_python",
    version="1.0.1",
    description="MVVM Modify for Python but you can also port to another language",
    long_description=io.open("README.md", "r", encoding="utf-8").read(),
    author="Anton Pichka",
    author_email="antonpichka@gmail.com",
    maintainer="Anton Pichka",
    maintainer_email="antonpichka@gmail.com",
    url="https://github.com/antonpichka/library_architecture_mvvm_modify_python",
    license="MIT",
    packages=["named_test_main"],
    py_modules=[
        "library_architecture_mvvm_modify_python",
    ],
    entry_points={
        "console_scripts": [
            "iterator_test_main = named_test_main.iterator_test_main:main",
            "temp_cache_test_main = named_test_main.temp_cache_test_main:main",
        ]
    }
)