from setuptools import setup, find_packages

runtime = set([
    'insights-core',
])


develop = set([
    'flake8',
    'pytest<4.1.0',
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


if __name__ == "__main__":
    setup(
        name="insights-core-tutorials",
        version="0.0.1",
        description="Insights Core Rule, Parser and Combiner Tutorials",
#        url="https://gitlab.cee.redhat.com/support-insights/support-rules",
        author="Red Hat, Inc.",
        packages=find_packages(),
        install_requires=list(runtime),
        extras_require={
            'develop': list(runtime | develop | docs),
            'docs': list(docs)
        },
        include_package_data=True
    )
