from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt', 'r') as req:
        content = req.read()
        requirements = [i for i in content.split('\n') if i and '===' not in i]

    return requirements

setup(
    name= "indusmes",
    version = "1.0.1",
    description= "MES Application from IndusWorks",
    author = "Navneet Jain",
    author_email="navneet@indusworks.in",
    packages = find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={
        'indusmes.backend': ['*.json'],
    },
    install_requires = read_requirements(),
    entry_points={
        'gui_scripts': [
            'indusmes=indusmes.main:main',
        ],
    },
)