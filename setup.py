from setuptools import setup, find_packages

long_description = """
Automated cadCAD system models diagram through GraphViz
"""

setup(name='cadCAD_machine_search',
      version='0.0.1.0',
      description="Tools for Large-Scale Machine Search for Parameter Optimization on cadCAD",
      long_description=long_description,
      url='https://github.com/danlessa/cadCAD_machine_search',
      author='Danilo Lessa Bernardineli',
      author_email='danilo@block.science, danilo.lessa@gmail.com',
      packages=find_packages(),
      install_requires=['cadCAD']
)
