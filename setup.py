from setuptools import setup, find_packages
from apigateway.apigateway import __version__


setup(name='beepbeep-apigateway',
      version=__version__,
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      entry_points="""
      [console_scripts]
      beepbeep-apigateway = apigateway.apigateway.run:main
      """)
