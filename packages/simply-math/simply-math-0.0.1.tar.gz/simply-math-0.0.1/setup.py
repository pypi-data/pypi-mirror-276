from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='simply-math',
  version='0.0.1',
  description='A very simple math module',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='AlexDEV',
  author_email='',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator, math', 
  packages=find_packages(),
  install_requires=['random'] 
)