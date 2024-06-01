from setuptools import setup, find_packages

setup(
    name='pycmitool',
    version='0.1.0',
    author='Munish Shah',
    author_email='munish.shah04@gmail.com',
    scripts=['SheetParser.py', 'SheetModelMapping.py', 'cmi.py'],
    packages=find_packages(),
)