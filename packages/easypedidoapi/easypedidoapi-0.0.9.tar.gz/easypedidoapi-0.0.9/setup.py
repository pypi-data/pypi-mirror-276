from setuptools import setup, find_packages

VERSION = '0.0.9'
DESCRIPTION = 'Package which helps to consume EasyPedido API'

setup(
    name='easypedidoapi',
    version=VERSION,
    author='Andrés Palacio',
    author_email='ampamo9@gmail.com',
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests', 'pyodbc'],
    keywords=['python', 'EasyPedido API']
    # classifiers= [
    #     "Development Status :: 1 - Alpha",
    #     "Intended Audience :: EasyPedido Trades",
    #     "Programming Language :: Python :: 2",
    #     "Programming Language :: Python :: 3",
    #     "Operating System :: MacOS :: MacOS X",
    #     "Operating System :: Microsoft :: Windows",
    # ]
)
