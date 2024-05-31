
### Step 5: Update `setup.py`

#Create a `setup.py` file in the root directory:

#```python
# setup.py

from setuptools import setup, find_packages

setup(
    name="text_eval_benchmark",
    version="0.1.0",
    description="A Python package to compute text similarity using Sentence Transformers",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Your Name",
    author_email="evikram@amazon.com",
    url="https://github.com/vikramelango/text_eval_benchmark",
    packages=find_packages(),
    install_requires=[
        "sentence-transformers",
        "torch"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

