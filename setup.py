from setuptools import setup, find_packages

setup(
    name='video_concatenator',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'typer[all]',
    ],
    entry_points={
        'console_scripts': [
            'video_concatenator=video_concatenator:app',
        ],
    },
    author='jopi',
    author_email='jopi.adrianto@gmail.com',
    description='A CLI tool to concatenate video segments',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # url='https://github.com/yourusername/video_concatenator',
)