import setuptools

DESC = 'Libreria que matará vuestro sufrimiento por la PARCA'

setuptools.setup(
    name='guadania',
    description=DESC,
    version='1.9.3',
    packages=[
        'guadania',
        'guadania.prisma'
    ],
    python_requires='>=3.7',
    install_requires=[
        'numpy',
        'openpyxl',
        'pandas',
        'requests'
    ],
)