from setuptools import setup, find_packages

setup(
    name='bees-challenge',
    version='0.11.0',
    author='yuiti',
    author_email='yuiti.usp@gmail.com',
    description='challenge submission for the bees ml path challenge',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yuiti-ara/yuiti-bees-ml-path-challenge',
    packages=find_packages(),
    python_requires='>=3.10',
    install_requires=[],
    entry_points={
        'console_scripts': [],
    },
    include_package_data=False,
    zip_safe=True,
)
