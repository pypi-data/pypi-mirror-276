from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='freedom_pay',
    version='0.0.4',
    author='erllan.000',
    author_email='erlan.kubanychbekov.000@gmail.com',
    description='wqewqewqewq',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/erlan.kubanychbekov.000/freedompay_lib',
    packages=find_packages(),
    install_requires=['requests>=2.25.1'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='files speedfiles ',
    project_urls={
        'GitLab': 'https://gitlab.com/erlan.kubanychbekov.000/freedompay_lib'
    },
    python_requires='>=3.6'
)
