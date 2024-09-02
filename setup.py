from setuptools import setup, find_packages

setup(
    name="TempMail",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "fake_useragent",
        "stem",
    ],
    entry_points={
        'console_scripts': [
            'TempMail = TempMail.core:TempMail',
        ],
    },
    description="Biblioteca para gerar emails temporários usando Tor e TempMail.",
    author="lalaio'",
    url="https://github.com/lalaio1/TempMail",
)
