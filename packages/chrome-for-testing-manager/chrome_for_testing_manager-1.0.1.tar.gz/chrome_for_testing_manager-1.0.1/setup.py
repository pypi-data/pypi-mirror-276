from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()
setup(
    name='chrome_for_testing_manager',
    version='1.0.1',
    description='Automatic download and manage Chrome and Chromedriver, and ensures that their versions match',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='sukaiyi',
    author_email='im.sukaiyi@gmail.com',
    url='https://github.com/sukaiyi/chrome-for-testing-manager-python',
    install_requires=[
        'requests>=2.0.1'
    ],
    license='Apache license 2.0',
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    platforms=["all"],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries'
    ],
)
