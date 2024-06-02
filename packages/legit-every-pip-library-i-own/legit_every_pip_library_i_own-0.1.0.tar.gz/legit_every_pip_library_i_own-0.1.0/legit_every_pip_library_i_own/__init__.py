import pkgutil
import importlib

def everything():
    packages = {package.name for package in pkgutil.iter_modules()}
    for package in packages:
        importlib.import_module(package)

# from legit_every_pip_library_i_own import everything
