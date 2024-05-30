from setuptools import setup, find_packages

VERSION = '0.0.4' 
DESCRIPTION = "Joe's Synthetic Data Generator"
LONG_DESCRIPTION = "AI Package to generate synthetic data using Google's gemini AI"
REQUIRED_PACKAGES = [
  "langchain",
"python-dotenv",
"langchain_google_genai"
]
setup(
        name="jmock", 
        version=VERSION,
        author="Joepeter Francis",
        author_email="jose4.peter42@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=REQUIRED_PACKAGES,
        keywords=['python', 'JSDG'],
)