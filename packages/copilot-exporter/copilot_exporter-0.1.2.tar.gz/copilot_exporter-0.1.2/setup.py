from setuptools import setup, find_packages

setup(
    name="copilot-exporter",
    version='0.1.2',
    url='https://github.com/enciyo/gh-copilot-history-export',
    author='Mustafa Kılıç',
    author_email='enciyomk61@gmail.com',
    description='This package exports the history of GitHub Copilot chat history.',
    long_description="This package exports the history of GitHub Copilot chat history.",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "requests",
        "mitmproxy"
    ],
)
