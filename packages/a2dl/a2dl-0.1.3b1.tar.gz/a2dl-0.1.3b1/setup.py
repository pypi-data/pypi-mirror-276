from setuptools import setup, find_packages

long_description = """

## a2dl | (A)sciidoc(2D)rawio(L)ibrary

Generate Draw.io / Diagrams.net libraries out of AsciiDoc-based descriptions and images.  

- AsciiDoc-based descriptions get integrated into HTML tooltips of draw.io icons.
- The icons are bundled into a draw.io / diagrams.net library.
- It allows to update a diagram if a library that it used has been updated.

"""

setup(
    name='a2dl',
    version='0.1.3b1',
    packages=find_packages(),
    zip_safe=False,
    package_data={'a2dl': ['data/**/*']},
    install_requires=['python-pptx', 'Pillow', 'python-docx', 'networkx', 'matplotlib', 'beautifulsoup4', 'chardet'],
    extras_require={
        'extensions': [
            'lxml',
            'XlsxWriter'
        ],
        'ml': [
            'scikit-learn',
            'transformers',
            'torch',
            'sentencepiece',
            'accelerate',
            'diffusers',
            'safetensors',
            'invisible-watermark',
            'rembg[gpu,cli]'
        ],
    },
    url='https://gitlab.com/tigabeatz/a2dl',
    author='tigabeatz',
    author_email='tigabeatz@cccwi.de',
    description='Generate draw.io icon libraries from AsciiDoc-based descriptions.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        # "Development Status :: 5 - Production/Stable",
        "Development Status :: 4 - Beta"
        # "Development Status :: 3 - Alpha"
    ],
    entry_points={
        'console_scripts': [
            'a2dl=a2dl.a2dl:cli'
        ]
    },
)
