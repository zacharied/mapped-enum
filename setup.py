import setuptools

with open('README.md', 'r') as desc:
    long_description = desc.read()

setuptools.setup(
    name='mapped-enum',
    version='0.3.1',
    author='Zach Day',
    author_email='z@zach.gdn',
    description='Enums with arbitrary lookup tables',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/zacharied/mapped-enum',
    packages=setuptools.find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ]
)
