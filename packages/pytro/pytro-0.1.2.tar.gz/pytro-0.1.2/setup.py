import setuptools

setuptools.setup(
    name='pytro',
    version='0.1.2',
    description='Symbios of eel and pywebview',
    author='NoSleepForTonight',
    install_requires=['eel', 'pywebview', 'pygobject'],
    dependency_links=['http://github.com/bottlepy/bottle.git@3fdb8b2a2e0d1641374b53ef2b051fe7f54508b5#egg=package-1.0']
)