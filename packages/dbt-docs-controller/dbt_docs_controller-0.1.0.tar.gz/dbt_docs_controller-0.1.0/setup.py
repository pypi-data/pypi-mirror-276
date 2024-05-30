# from setuptools import setup, find_packages
# import codecs

# with codecs.open('README.md', 'r', 'utf-8') as f:
#     long_description = f.read()

# setup(
#     name='dbt-docs-controller',
#     version='0.2.0',
#     packages=find_packages(),
#     package_dir={},
#     entry_points={
#         'console_scripts': [
#             'dbt-docs-controller=main:main',
#         ],
#     },
#     install_requires=[],
#     author='Govarthanan S',
#     description='dbt-docs-controller streamlines dbt documentation by generating only the relevant models, sources, and components for concise, targeted user information.',
#     long_description=long_description,
#     long_description_content_type='text/markdown',
#     url='https://github.com/Govarthanans8/dbt-docs-controller/tree/main',
#     classifiers=[
#         'Programming Language :: Python :: 3',
#         'License :: OSI Approved :: MIT License',
#         'Operating System :: OS Independent',
#     ],
#     python_requires='>=3.7',
# )


from setuptools import setup, find_packages
import codecs

with codecs.open('README.md', 'r', 'utf-8') as f:
    long_description = f.read()

setup(
    name='dbt-docs-controller',
    version='0.1.0',
    packages=find_packages(),
    package_dir={},
    entry_points={
        'console_scripts': [
            'dbt-docs-controller=SRC.__main__:main_wrapper',
        ],
    },
    install_requires=[],
    author='Govarthanan S',
    description='dbt-docs-controller streamlines dbt documentation by generating only the relevant models, sources, and components for concise, targeted user information.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Govarthanans8/dbt-docs-controller/tree/main',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
