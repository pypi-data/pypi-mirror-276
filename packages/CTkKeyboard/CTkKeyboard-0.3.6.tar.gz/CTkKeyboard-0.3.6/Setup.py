from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='CTkKeyboard',
    version='0.3.6',
    author='Cadam',
    description='A virtual keyboard for CustomTkinter, making it easy to enter text on a Raspberry Pi with a touch display.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/CadamTechnology/CTkKeyboard',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'customtkinter',
    ],
)


