from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name='subspy',
    version='2.2.3',
    description='SubSpy: A tool for subdomain enumeration.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://mrfidal.in/cyber-security/subspy',
    author='Fidal',
    author_email='mrfidal@proton.me',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Topic :: Security',
    ],
    keywords='subspy, subdomain, enumeration, scanning, mrfidal, cyber security',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'subspy': ['default_subdomains.txt'],
    },
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'subspy=subspy.cli:main',
        ],
    },
)
