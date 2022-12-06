from setuptools import setup, find_packages

runtime = set([
    'insights-core',
])


develop = set([
    'flake8',
    'pytest>=3.6',
    'jinja2',
    'ipython',
    'jupyter',
    'pytest-cov'
])

docs = set([
    'Sphinx',
    'nbsphinx',
    'sphinx_rtd_theme',
    'recommonmark',
    'ipython',
])

testing = set([
    'coverage==4.4',
    'pytest==3.6',
    'pytest-cov==2.4.0',
    'mock==2.0.0',
])

linting = set([
    'flake8==2.6.2',
])


if __name__ == "__main__":
    setup(
        name="insights-core-tutorials",
        version="0.0.2",
        description="Insights Core Rule, Parser and Combiner Tutorials",
        author="Red Hat, Inc.",
        packages=find_packages(),
        install_requires=list(runtime),
        extras_require={
            'develop': list(runtime | develop | docs | linting | testing),
            'docs': list(docs),
            'linting': list(linting),
            'testing': list(testing)
        },
        include_package_data=True
    )
