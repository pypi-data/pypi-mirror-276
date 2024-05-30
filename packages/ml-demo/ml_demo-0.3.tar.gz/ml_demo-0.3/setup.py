from setuptools import setup, find_packages
packages = ['ml_demo']
with open('README.md', 'r', encoding='UTF-8') as f:
    long_description = f.read()
setup(
    name="ml_demo",
    version="0.3",
    author="ming lin",
    author_email="ml@ml.com",
    description="ml_demo package",
    packages=find_packages(),
    install_requires=[
        # 列出第三方库依赖
        'asyncio',
    ],
    package_data={'': ['*/txt']},
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',  # 指定Python版本
)