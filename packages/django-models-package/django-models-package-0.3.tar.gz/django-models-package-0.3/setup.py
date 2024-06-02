from setuptools import find_packages, setup

setup(
    name='django-models-package',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'Django>=3.0',
    ],
    include_package_data=True,
    description='A reusable Django models package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Sayrex',
    author_email='reshetneff2013@gmail.com',
    url='https://github.com/yourusername/django-models-package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
