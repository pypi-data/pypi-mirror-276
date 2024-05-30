from setuptools import setup, find_packages

setup(
    name='myfunctions_aizhan010',
    version='0.0.5',
    packages=find_packages(),
    install_requires=[],
    url='https://github.com/aizhan010/',
    license='MIT',
    author='Aizhan Maratova',
    author_email='aizhanmaratova6@gmail.com',
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