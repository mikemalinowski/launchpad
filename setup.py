import os
import setuptools

short_description = 'Launchpad represents a small factory and a distinct abstract for defining actionable items'
if os.path.exists('README.md'):
    with open('README.md', 'r') as fh:
        long_description = fh.read()

else:
    long_description = short_description

setuptools.setup(
    name='launchpad',
    version='1.0.0',
    author='Mike Malinowski',
    author_email='mike@twisted.space',
    description=short_description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mikemalinowski/launchpad',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=['qute', 'scribble', 'factories'],
    keywords="launch launchpad pad action actions",
)
