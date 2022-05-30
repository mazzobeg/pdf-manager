from setuptools import setup

setup(
    name = "pdfmanager",
    version = "0.0.1",
    author = "Giovanni Mazzobel",
    packages = ["pdfmanager"],
    entry_points = {
        'console_scripts' : {
            'cli-name' : 'cli.py'
        }
    },
    install_requires = [
        "nltk==3.7","pdfminer==20191125",
        "regex==2022.4.24",
        "python-dotenv==0.20.0"]
)