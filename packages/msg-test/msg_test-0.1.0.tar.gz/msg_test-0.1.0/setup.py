from setuptools import setup, find_packages

setup(
    name='msg_test',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Harsh Jaiswal',
    author_email='harsh@walkover.in',
    description='A package for utilizing MSG91 service integration',
    # url='https://github.com/yourusername/msg91',  # Replace with your GitHub URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)