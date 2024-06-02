import pathlib, setuptools

# setuptools.setup(
#     name="dvs_printf",
#     version="1.3",
#     description=
# "Animated Visual appearance for console-based applications, with different animation styles",
#     long_description=pathlib.Path("README.md").read_text(),
#     long_description_content_type="text/markdown",
#     url="https://github.com/dhruvan-vyas/dvs_printf",
#     author="dhruvan_vyas",
#     license="MIT License",
#     project_urls={
#         "Documentation":"https://github.com/dhruvan-vyas/dvs_printf/blob/main/README.md",
#         "":"https://pypi.org/project/dvs-printf",
#     },
#     classifiers=[
#         "Development Status :: 5 - Production/Stable",
#         "Intended Audience :: Developers",
#         "Programming Language :: Python :: 3.10",
#         "Programming Language :: Python :: 3.11",
#         "Programming Language :: Python :: 3.12",
#         "Topic :: Utilities",
#         "Environment :: Console"],
#     python_requires=">=3.10",
#     packages=setuptools.find_packages(),
#     include_package_data=True,
# )


from setuptools import setup, find_packages

setup(
    name='test_dvs_printf',
    version='1.6',
    description=
"Animated Visual appearance for console-based applications, with different animation styles",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Dhruvan Vyas',
    url='https://github.com/dhruvan-vyas/dvs_printf',
    packages=find_packages(),
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Terminals',
        "Environment :: Console"
    ],
    keywords = ["printf", "animation", "console", "terminal"],
    license='MIT',
    project_urls={
        'Source': 'https://github.com/dhruvan-vyas/dvs_printf',
        "Documentation": "https://github.com/dhruvan-vyas/dvs_printf/blob/main/README.md",
        'Tracker': 'https://github.com/dhruvan-vyas/dvs_printf/issues'
    },
    include_package_data=True,
    zip_safe=False
)
