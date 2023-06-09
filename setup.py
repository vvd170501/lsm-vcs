from setuptools import setup  # type: ignore
from ngit import __version__


with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='ngit',
    description='Not git',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Vadim Dudkin, Eugene Kogan',
    url='https://github.com/vvd170501/lsm-vcs',
    version=__version__,
    packages=['ngit'],
    include_package_data=True,
    install_requires=[
        'Click',
        'grpcio',
        'protobuf',
        'sortedcontainers',
    ],
    extras_require={
        'dev': [
            'grpcio-tools',
            'mypy',
            'grpc-stubs',
            'pre-commit',
            'pytest',
            'types-protobuf',
        ]
    },
    python_requires='>=3.10',
    entry_points='''
        [console_scripts]
        ngit=ngit.cli.main:main
    ''',
)
