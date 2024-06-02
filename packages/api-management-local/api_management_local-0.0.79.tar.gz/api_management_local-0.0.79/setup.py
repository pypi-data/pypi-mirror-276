import setuptools

PACKAGE_NAME = "api-management-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.79',  # https://pypi.org/project/api-management-local/
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles api-management-local-python-package",
    long_description="PyPI Package for Circles api-management-local-python-package",
    long_description_content_type='text/markdown',
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    # packages=setuptools.find_packages(),
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests>=2.31.0",
        "database-mysql-local>=0.0.306",
        "logger-local>=0.0.135",
        "python-sdk-remote>=0.0.93",
        "star-local>=0.0.16",
        "url-remote>=0.0.91"
    ],
)
