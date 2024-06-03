from setuptools import setup, find_packages

setup(
    name='validation_framework',
    version='0.1.1',
    description='A framework for validating LLM responses on various criteria.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/validation_framework',  # Update with your URL
    author='Your Name',
    author_email='your.email@example.com',
    license='MIT',  # Or any license you choose
    packages=find_packages(),
    install_requires=[
        # 'some_dependency>=1.0.0',
        # 'another_dependency>=2.0.0',
        # Add other dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)