from setuptools import setup, find_packages

setup(
    name='python-automation',
    version='0.0.0',
    description='window automation package made and maintained by changgwak(tony)',
    author='changgwak',
    author_email='iamtony.ca@gmail.com',
    url='https://github.com/changgwak/',
    install_requires=['python-opencv', 'numpy', 'pillow', 'pywin32'],
    packages=find_packages(exclude=[]),
    keywords=['pyauto', 'rpa', 'python rpa', 'python automation', 'window selenium', 'pyautomation', 'autoclick'],
    python_requires='>=3.10',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
