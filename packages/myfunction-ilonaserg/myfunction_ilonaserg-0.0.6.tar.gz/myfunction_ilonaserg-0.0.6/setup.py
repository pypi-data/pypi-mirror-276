from setuptools import setup, find_packages

setup(
    name='myfunction_ilonaserg',
    version='0.0.6',
    packages=find_packages(),
    install_requires=["os"],
    url='https://github.com/ilonaserg/',
    license='MIT',
    author='Ilona Sergeeva',
    author_email='asteria2009scorp@gmail.com',
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