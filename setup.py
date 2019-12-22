from setuptools import find_packages, setup

LONG_DESCRIPTION = """\
Simple API client for Yandex Cloud
=========================
"""

setup(
    name='ycloud',
    version='0.1',
    description='Yandex Cloud API library for Python',
    long_description=LONG_DESCRIPTION,
    license='MIT',
    author='s.rostunov',
    author_email='sergey@rostunov.com',
    url='https://github.com/stdex/ycloud',
    packages=find_packages(),
    install_requires=['requests'],
    keywords='yandex cloud, api',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
    ],
    zip_safe=True,
)
