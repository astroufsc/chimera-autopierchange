from distutils.core import setup

setup(
    name='chimera_autopierchange',
    version='0.0.1',
    packages=['chimera_autopierchange', 'chimera_autopierchange.controllers'],
    scripts=[],
    url='http://github.com/astroufsc/chimera-autopierchange',
    license='GPL v2',
    author='William Schoenell',
    author_email='william@astro.ufsc.br',
    description='Chimera plugin to automatically flip pier side for German Equatorial mounts'
)
