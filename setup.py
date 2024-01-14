from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='limited_aiogram',
  version='0.1.1',
  author='chazovtema',
  author_email = 'chazovtema@mail.ru',
  description='This is my first module',
  long_description=readme(),
  long_description_content_type='text/markdown',
  packages=find_packages(),
  install_requires=['requests>=2.25.1', 'aiogram>=3.0.0', 'limiter>=0.3.1'],
  classifiers=[
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords= ['aiogram', 'limit'],
  project_urls={},
  python_requires='>=3.10',
)