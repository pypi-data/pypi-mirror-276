from setuptools import setup, find_packages

setup(
    name='pytest_qanova',
    version='0.0.2dev3',
    author='Davit Amirkhanyan',
    author_email='davit.amirkhanyan95@gmail.com',
    description='A pytest plugin to collect test information',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/davidamirkhanyan/pytest-qanova',  # Your project URL
    packages=find_packages(),
    entry_points={
        'pytest11': [
            'pytest_qanova = pytest_qanova.plugin',
            ],
        },
    install_requires=[
        'pytest',
        ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Framework :: Pytest',
        ],
    python_requires='>=3.6',
    )
