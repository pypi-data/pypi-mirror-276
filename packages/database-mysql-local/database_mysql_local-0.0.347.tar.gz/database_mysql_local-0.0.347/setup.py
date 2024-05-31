import setuptools

PACKAGE_NAME = "database-mysql-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,  # https://pypi.org/project/database-mysql-local
    version='0.0.347',
    author="Circles",
    author_email="info@circles.ai",
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    long_description="Database MySQL Local",
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "mysql-connector-python>=8.3.0",  # https://pypi.org/project/mysql-connector-python/
        "url-remote>=0.0.80",  # https://pypi.org/project/url-remote/
        "logger-local>=0.0.102",  # https://pypi.org/project/logger-local/
        "database-infrastructure-local>=0.0.19",  # https://pypi.org/project/database-infrastructure-local/
        "language-remote>=0.0.8",  # https://pypi.org/project/language-remote/
        "sql-to-code-local>=0.0.2",  # https://pypi.org/project/sql-to-code-local/
        "python-sdk-remote>=0.0.75"
    ]
)
