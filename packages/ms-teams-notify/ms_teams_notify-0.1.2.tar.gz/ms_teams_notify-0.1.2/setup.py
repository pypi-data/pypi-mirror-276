import logging

from setuptools import find_packages, setup

with open('README.md', encoding="utf-8") as fp:
    distribution = setup(
        name='ms_teams_notify',
        version='0.1.2',
        description='Notify to Microsoft Teams with Adaptive Card.',
        long_description=fp.read(),
        long_description_content_type='text/markdown',
        author='rue1-suzuki',
        author_email='suzuki.ryuichi.1998@gmail.com',
        url='https://github.com/rue1-suzuki?tab=packages',
        packages=find_packages(),
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
        ],
        python_requires='>=3.6',
    )

logging.debug(distribution)
