from setuptools import setup, find_packages

# Read the dependencies from requirements.txt
with open("requirements.txt") as f:
    install_requires = f.read().strip().split('\n')

setup(
    name="langchain-one",
    version="0.1",
    author="Abhimanyu Singh",
    author_email="abhimanyus1997@gmail.com",
    description="LLM App made using Langchain Framework for Custom Data",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=install_requires,
)
