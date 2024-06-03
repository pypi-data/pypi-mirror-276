from pathlib import Path # > 3.6
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '0.0.5'
DESCRIPTION = 'Permite consumir el API de Telematel'
PACKAGE_NAME = 'dbTelematelAPI'
AUTHOR = 'José María Sánchez González'
EMAIL = 'miotroyo1970@gmail.com'
GITHUB_URL = 'https://github.com/jmsanchez-ibiza/dbTelematelAPI'

setup(
    name = PACKAGE_NAME,
    packages = [PACKAGE_NAME],
    # entry_points={
    #     "console_scripts":
    #         ["pycody=codigofacilito.__main__:main"]
    # },
    version = VERSION,
    license='MIT',
    description = DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    author = AUTHOR,
    author_email = EMAIL,
    url = GITHUB_URL,
    keywords = [
        'jmsanchez-ibiza'
    ],
    install_requires=[ 
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)