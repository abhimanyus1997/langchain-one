import os

def create_directory_structure(project_name, author, email):
    # Prompt for project description
    description = input("Enter project description: ")

    # Create project directories
    create_project_directories(project_name)

    # Create README.md file
    create_readme_file(project_name, author, email, description)

    # Create requirements.txt file with dependencies
    create_requirements_file()

    # Create setup.py file
    create_setup_file(project_name, author, email, description)

    # Create .gitignore file
    create_gitignore_file()

    # Create placeholder files
    create_placeholder_files(project_name)

    print(f"Project structure created in the current directory for {project_name}")

def create_project_directories(project_name):
    # Define the project's subdirectories
    directories = [
        "src/{}".format(project_name),
        "tests",
        "docs",
        "data",
        "scripts",
        "examples",
        "models"
    ]

    # Create the subdirectories
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

def create_readme_file(project_name, author, email, description):
    # Create README.md file with project information
    readme_path = "README.md"
    if not os.path.exists(readme_path) or os.path.getsize(readme_path) == 0:
        with open(readme_path, "w") as f:
            f.write(f"# {project_name}\n\nAuthor: {author}\nEmail: {email}\n\n{description}")

def create_requirements_file():
    # Create requirements.txt with project dependencies
    requirements_path = "requirements.txt"
    if not os.path.exists(requirements_path) or os.path.getsize(requirements_path) == 0:
        with open(requirements_path, "w") as f:
            f.write(
                "langchain[llm]\n"
                "gpt4all\n"
                "chromadb\n"
                "langchainhub\n"
                "openai\n"
                "python-dotenv\n"
                "streamlit\n"
                "notebook\n"
                "numpy\n"
                "scipy\n"
                "scikit-learn\n"
                "pandas\n"
                "matplotlib\n"
                "seaborn\n"
                "jupyter\n"
                "-e ."
            )

def create_setup_file(project_name, author, email, description):
    # Create setup.py with project metadata and dependencies
    setup_path = "setup.py"
    if not os.path.exists(setup_path) or os.path.getsize(setup_path) == 0:
        with open(setup_path, "w") as f:
            f.write(f"from setuptools import setup, find_packages\n\n"
                    f"setup(\n"
                    f"    name=\"{project_name}\",\n"
                    f"    version=\"0.1\",\n"
                    f"    author=\"{author}\",\n"
                    f"    author_email=\"{email}\",\n"
                    f"    description=\"{description}\",\n"
                    f"    packages=find_packages(\"src\"),\n"
                    f"    package_dir={{\"\": \"src\"}},\n"
                    f"    install_requires=[\"langchain[llm]\", \"streamlit\"],\n"
                    f")")

def create_gitignore_file():
    # Create .gitignore file or append to an existing one
    gitignore_path = ".gitignore"

    # List of files or patterns to add to .gitignore in the models directory
    models_gitignore_entries = [
        "models/*"
    ]

    gitignore_content = ""

    # If the .gitignore file already exists, read its contents and append the new entries
    if os.path.exists(gitignore_path) and os.path.getsize(gitignore_path) > 0:
        with open(gitignore_path, "r") as f:
            gitignore_content = f.read()

    with open(gitignore_path, "w") as f:
        # Write existing .gitignore content
        f.write(gitignore_content)

        # Append entries specific to the 'models' directory
        for entry in models_gitignore_entries:
            if entry not in gitignore_content:
                f.write("\n" + entry)


def create_placeholder_files(project_name):
    # Create placeholder __init__.py and module.py files
    init_path = f"src/{project_name}/__init__.py"
    if not os.path.exists(init_path) or os.path.getsize(init_path) == 0:
        with open(init_path, "w") as f:
            pass

    module_path = f"src/{project_name}/module.py"
    if not os.path.exists(module_path) or os.path.getsize(module_path) == 0:
        with open(module_path, "w") as f:
            pass

    # Create an empty test_module.py file
    test_module_path = "tests/test_module.py"
    if not os.path.exists(test_module_path) or os.path.getsize(test_module_path) == 0:
        with open(test_module_path, "w") as f:
            pass

if __name__ == "__main__":
    project_name = input("Enter project name: ")
    author = input("Enter author name: ")
    email = input("Enter author email: ")
    create_directory_structure(project_name, author, email)
