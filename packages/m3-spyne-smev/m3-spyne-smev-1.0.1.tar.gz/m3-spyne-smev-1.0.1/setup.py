from os.path import dirname
from os.path import join
import os

from setuptools import find_packages
from setuptools import setup
from setuptools.command.install import install


def _read(file_name):
    with open(join(dirname(__file__), file_name)) as f:
        return f.read()


class _CustomInstallCommand(install):
    """Кастомизированная команда setuptools install.

    В версиях cryptography 2.x автоматически загружается пакет openssl 1.1.x,
    в котором нет гост алгоритмов. Указание параметра --no-binary cryptography
    обеспечивает установку пакета cryptography без пакета openssl.
    В этом случае пакет cryptography будет использовать пакет openssl,
    установленный в системе.
    """

    def run(self):
        os.system('pip install "cryptography>=3.4.8,<4" '
                  '--ignore-installed --no-binary cryptography')
        install.run(self)


setup(
    cmdclass={
        'install': _CustomInstallCommand,
    },
    name='m3-spyne-smev',
    url='https://stash.bars-open.ru/projects/M3/repos/spyne-smev/browse',
    license='MIT',
    author='BARS Group',
    author_email='bars@bars-open.ru',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    description=_read('DESCRIPTION'),
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Natural Language :: Russian',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
    ],
    dependency_links=(
        'http://pypi.bars-open.ru/simple/m3-builder',
    ),
    setup_requires=(
        'm3-builder>=1.1',
    ),
    install_requires=(
        "lxml",
        "cryptography>=3.4.8,<4",
        "requests>=2,<3",
        "spyne>=2.11,<3",
    ),
    extras_require={
        ":python_version > '2.7'": ["suds-py3>=1.3.3.0,<2"],
    },
    set_build_info=dirname(__file__),
)
