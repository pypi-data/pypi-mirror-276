from setuptools import setup, find_packages

setup(
    name='prjit',
    version='0.0.6',
    packages=find_packages(include=['prjitter', 'prjitter.*']),
    url='https://github.com/archiba/prjit',
    license='',
    author='archiba',
    author_email='yuki-chiba@outlook.jp',
    description='Define a project workspace and switch files and applications',
    python_requirems='>=3.9',
    install_requires=[
        'pydantic>=2.0.0',
        'fire',
        'PyYAML',
        'pyobjc',
        'prompt-toolkit',
        'atomacos',
        'psutil',
        'inquirer'
    ],
    scripts=['bin/prjit']
)
