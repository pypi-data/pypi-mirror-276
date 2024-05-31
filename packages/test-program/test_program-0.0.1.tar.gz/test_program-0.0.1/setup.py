from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Lnaguage :: Python :: 3'
]

setup(
    name='test_program',
    version='0.0.1',
    description='A test package',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='HSM',
    author_email='hsm@gmail.com',
    license='MIT',
    classfiers = classifiers,
    keywords='test',
    packages=find_packages(),
    install_requires= ['']
)