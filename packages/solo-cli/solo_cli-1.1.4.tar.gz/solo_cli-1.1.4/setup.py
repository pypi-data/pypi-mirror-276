from setuptools import setup, find_packages

setup(
    name='solo-cli',
    version='1.1.4',
    py_modules=['solo_cli'],
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        solo=solo_cli:cli
    ''',
    author="Dhruv Diddi",
    author_email="your.email@example.com",
    description="A CLI to install and manage Ollama, and serve OpenUI with ngrok",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/solo-cli",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

