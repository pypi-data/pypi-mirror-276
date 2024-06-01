from setuptools import find_packages, setup


# Read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='llmv',
    packages=find_packages(include=['llmv']),
    version='0.1.0',
    description='command line tool to interact with LLM with vision',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='iris2',
    install_requires=["litellm>=1.35.1", "python-dotenv>=1.0.1" ,"pillow>=10.3.0", "opencv-python"],
)
