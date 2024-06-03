from setuptools import setup, find_packages
 
 
setup(
    name='cube-recognizer-for-agv',
    version="1.0.3",
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        "requests","numpy","imutils"
    ],
    license='GNU General Public License v3.0',
    author='Anonymous',
    author_email='anonymous@tsstudio.top',
    description='Cube recognition',
)