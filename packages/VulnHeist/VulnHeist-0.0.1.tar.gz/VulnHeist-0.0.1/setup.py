from setuptools import setup, find_packages

# Read the contents of the README file
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='VulnHeist',
    version='0.0.1',
    author='Team VulnHeist',
    author_email='vulnheist@gmail.com',
    description='Automated Penetration Testing Suite leveraging Nmap and Metasploit Framework.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Organisation-404/VulnHeist',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Security',
    ],
    python_requires='>=3.6',

    install_requires=[
        "rich",
        "pyfiglet",
        "art",
        "pymetasploit3",
        "colorama",
        "python-libnmap",
        "matplotlib"
    ],
    
    entry_points={
        'console_scripts': [
           'VulnHeist=VulnHeist.VulnHeist:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/Organisation-404/VulnHeist/issues',
        'Source': 'https://github.com/Organisation-404/VulnHeist',
    },
)
