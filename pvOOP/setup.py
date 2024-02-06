from setuptools import setup
# Con este módulo instalamos la app en el sistema
setup(
    name='pv',
    version='0.1',
    py_modules=['pv'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        pv=pv:cli
    ''',
)

## instalamos todo el pauqete con 
# 'pip install --editable .'

"""
Luego de instalado ya podemos
which pv
pv --help
pv clients --help"""