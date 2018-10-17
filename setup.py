from setuptools import setup

setup(
        name='Sallust',
        version='0.13',
        packages=['Sallust', 'Sallust.GUI', 'Sallust.Tools'],
        url='https://github.com/socisomer/Sallust',
        license='GNU General Public License v3.0',
        author='Joan Albert Espinosa',
        author_email='joanalbert.espinosa@gmail.com',
        description='Sallust is a modern, open source testing support application. it helps track tests cases',
        install_requires=['lxml', 'matplotlib', 'Pillow', 'numpy', 'natsort']
)
