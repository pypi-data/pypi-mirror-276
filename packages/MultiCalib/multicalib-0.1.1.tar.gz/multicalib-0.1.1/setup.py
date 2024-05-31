from setuptools import setup, find_packages

setup(
    name='MultiCalib',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'matplotlib==3.7.5',
        'networkx==3.1',
        'numpy==1.23.5',
        'opencv-python==4.7.0.72',
        'scikit-learn==1.3.0',
        'scipy==1.10.1',
        'PyYAML==6.0',
    ],
    author='Obumneme Dukor',
    author_email='stanleydukor@gmail.com',
    description='A Python library for multi-camera system calibration with high accuracy.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/stanleydukor/MultiCalib',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
