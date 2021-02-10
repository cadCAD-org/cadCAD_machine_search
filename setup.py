from setuptools import setup, find_packages

long_description = """
cadCAD tools for preparing & analyzing experiments where large-scale machine search for selecting parameters are involved.
"""

setup(name='cadCAD_machine_search',
      version='0.0.1.2',
      description="Tools for Large-Scale Machine Search for Parameter Optimization on cadCAD",
      long_description=long_description,
      url='https://github.com/cadCAD-org/cadCAD_machine_search',
      author='Danilo Lessa Bernardineli',
      author_email='danilo@block.science, danilo.lessa@gmail.com',
      packages=find_packages(),
      install_requires=['cadCAD']
)
