from setuptools import setup, find_packages

setup(
    name='myfunction_vikmin2022',
    version='0.03',
    packages=find_packages(),
    install_requires=[],
    url='https://github.com/vikmin2022',
    license='MIT',
    author='Viktoriia Minosian',
    author_email='viktoriia.minosian@gmail.com',
    description='A description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)