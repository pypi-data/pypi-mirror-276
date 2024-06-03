from setuptools import setup, find_packages

setup(
    name='hello_auz2',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi"
    ],
    author='Augustine',
    author_email='auzuha@example.com',
    description='Description of your package',
    long_description='Longer description of your package',
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/yourpackage',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
