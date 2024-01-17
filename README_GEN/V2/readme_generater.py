import click
from rich.console import Console
import sys
import os
from datetime import datetime
import validators

console = Console()

def get_multiline_input(prompt, allow_empty=False):
    """Prompt user for multiline input until 'END' is entered."""
    console.print(f"{prompt} (Type 'END' on a new line to finish input):")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        lines.append(line)
    input_text = "\n".join(lines)
    if not input_text.strip() and not allow_empty:
        console.print("Input cannot be empty. If you want to leave it empty, press Enter.", style="bold red")
        return get_multiline_input(prompt, allow_empty)  # Recursively call the function if input is empty
    return input_text

def is_valid_url(url):
    """Check if the given URL is valid."""
    return validators.url(url)

def get_valid_url(prompt, default_url=None, allow_empty=False, is_testing=False):
    """Prompt user for a valid URL."""
    if is_testing:
        return default_url if default_url else None

    while True:
        url = input(prompt).strip() if default_url is None else default_url
        if allow_empty and not url:
            return None  # Return None if allow_empty is True and the user leaves the input empty
        if url and is_valid_url(url):
            return url
        else:
            console.print("Invalid URL. Please enter a valid URL.", style="bold red")

def generate_readme(answers, dependencies, homepage_url=None, doc_url=None):
    """Customize this function to format and structure your README.md."""
    readme_content = f"# {answers['project_name']}\n\n" \
                     f"## Description\n{answers['project_description']}\n\n" \
                     f"## Project Links\n" \
                     f"- [Homepage]({homepage_url})\n" \
                     f"- [Documentation]({doc_url})\n\n" \
                     f"## Author\n{answers['author']}\n\n" \
                     f"## License\n{answers['license_name']}\n\n" \
                     f"## Installation\n```bash\n{answers['install_command']}\n```\n\n" \
                     f"## Usage\n```bash\n{answers['usage_instructions']}\n```\n\n" \
                     f"## Testing\n```bash\n{answers['test_command']}\n``"

    # Include Dependencies section only if there are dependencies
    if dependencies:
        readme_content += "\n## Dependencies\n" + "\n".join(f"- {dep}" for dep in dependencies)

    return readme_content

def write_readme(answers, dependencies, homepage_url=None, doc_url=None, create_new_readme=False):
    """Generate README content and write it to a file."""
    readme_content = generate_readme(answers, dependencies, homepage_url, doc_url)

    if create_new_readme:
        readme_file_path = f"README_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
    else:
        readme_file_path = 'README.md'
        if os.path.exists(readme_file_path):
            user_input = input("A README.md file already exists. Do you want to (o)verwrite, (c)reate a new one, or (e)xit? ").strip().lower()
            if user_input == 'o':
                pass  # Overwrite existing README.md
            elif user_input == 'c':
                readme_file_path = f"README_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"  # Create a new README.md
            elif user_input == 'e':
                console.print("Exiting without generating README.", style="bold red")
                return
            else:
                console.print("Invalid choice. Exiting without generating README.", style="bold red")
                return

    with open(readme_file_path, 'w') as readme_file:
        readme_file.write(readme_content)

    console.print(f"{readme_file_path} generated successfully!", style="bold green")

def get_dependencies():
    """Get user input for project dependencies."""
    while True:
        dependencies = input("Enter project dependencies (comma-separated, or 'END' to finish): ").strip()
        if dependencies.upper() == 'END':
            return []  # Return an empty list if the user enters 'END'
        elif not dependencies:
            return []  # Return an empty list if the user leaves it empty
        else:
            return dependencies.split(",")
        
def get_user_input(prompt, allow_empty=False):
    """Get user input and ensure it is not empty unless specified."""
    while True:
        user_input = input(prompt).strip()
        if user_input or allow_empty:
            return user_input
        else:
            console.print("Input cannot be empty. If you want to leave it empty, press Enter.", style="bold red")


def run_tests_function():
    # Test generate_readme function
    test_answers = {
        'project_name': 'README.md Generator',
        'project_description': 'Certainly! The provided Python script is a command-line tool for generating README.md files for software projects...',
        'project_homepage': 'https://github.com/smritibangera/README.md-Generator',
        'project_doc_url': 'https://github.com/smritibangera/README.md-Generator',
        'author': 'Smriti Bangera',
        'license_name': 'MIT',
        'install_command': 'pip install click rich validators',
        'usage_instructions': 'Certainly! Here are usage instructions for running the provided Python script:...',
        'test_command': 'python script_name.py --run-tests',
        'dependencies': ['click', 'rich', 'validators']
    }

    homepage_url = 'https://github.com/smritibangera/README.md-Generator'

    generated_readme = generate_readme(test_answers, test_answers['dependencies'], homepage_url=homepage_url)

    # Call write_readme to generate the README file
    write_readme(test_answers, test_answers['dependencies'], homepage_url=homepage_url)

    assert 'README.md Generator' in generated_readme
    assert 'Certainly! The provided Python script is a command-line tool for generating README.md files for software projects.' in generated_readme
    assert homepage_url in generated_readme

    console.print("All tests passed successfully!", style="bold green")

def run_additional_tests():
    # Test empty dependencies
    test_answers_empty_deps = {
        'project_name': 'Empty Dependencies Project',
        'project_description': 'Project with empty dependencies.',
        'project_homepage': 'https://github.com/testuser/emptydepsproject',
        'project_doc_url': 'https://emptydepsproject.readthedocs.io/',
        'author': 'John Doe',
        'license_name': 'Apache 2.0',
        'install_command': 'pip install emptydepsproject',
        'usage_instructions': 'python emptydepsproject.py',
        'test_command': 'pytest',
        'dependencies': []
    }

    generated_readme_empty_deps = generate_readme(test_answers_empty_deps, test_answers_empty_deps['dependencies'])
    assert 'Empty Dependencies Project' in generated_readme_empty_deps

    if test_answers_empty_deps['dependencies']:
        assert '## Dependencies\n' in generated_readme_empty_deps  # should include Dependencies section
        assert '- ' not in generated_readme_empty_deps  # should not include any dependencies
    else:
        assert '## Dependencies\n' not in generated_readme_empty_deps  # should not include Dependencies section

    # Test special characters in project description
    test_answers_special_chars = {
        'project_name': 'Special Characters Project',
        'project_description': 'Project with special characters: & < > " \'',
        'project_homepage': 'https://github.com/testuser/specialcharsproject',
        'project_doc_url': 'https://specialcharsproject.readthedocs.io/',
        'author': 'Alice',
        'license_name': 'MIT',
        'install_command': 'pip install specialcharsproject',
        'usage_instructions': 'python specialcharsproject.py',
        'test_command': 'pytest',
        'dependencies': ['dep1', 'dep2']
    }

    generated_readme_special_chars = generate_readme(test_answers_special_chars, test_answers_special_chars['dependencies'])
    assert 'Special Characters Project' in generated_readme_special_chars
    assert '&' in generated_readme_special_chars  # Check for the actual ampersand character
    assert '<' in generated_readme_special_chars  # Check for the actual "<" character
    assert '>' in generated_readme_special_chars  # Check for the actual ">" character
    assert '"' in generated_readme_special_chars  # Check for the actual `"` character
    assert "'" in generated_readme_special_chars  # Check for the actual "'" character

    console.print("Additional tests passed successfully!")



@click.command()
@click.option('--run-tests', is_flag=True, help='Run tests')
@click.option('--create-new-readme', is_flag=True, help='Create a new README.md file')
def cli(run_tests, create_new_readme):
    if run_tests:
        run_tests_function()
        run_additional_tests()
    else:
        main(run_tests, create_new_readme)

def main(run_tests, create_new_readme=False):
    console.print("ENTER PROJECT INFORMATION:")

    answers = {
        'project_name': get_user_input("Enter the project name:", allow_empty=True),
        'project_description': get_multiline_input("Describe your project:", allow_empty=True),
        'project_homepage': '',
        'project_doc_url': '',
        'author': get_user_input("Enter the author's name:", allow_empty=True),
        'license_name': get_user_input("Enter the license name:", allow_empty=True),
        'install_command': get_multiline_input("Enter the installation command:", allow_empty=True),
        'usage_instructions': get_multiline_input("Enter usage instructions:", allow_empty=True),
        'test_command': get_user_input("Enter the test command:", allow_empty=True),
        'dependencies': get_dependencies()
    }

    if not answers['project_name']:
        console.print("Exiting without generating README.", style="bold red")
        return

    if not run_tests:
        answers['project_homepage'] = get_valid_url("Enter the project homepage URL:", allow_empty=True)
        answers['project_doc_url'] = get_valid_url("Enter the project documentation URL:", allow_empty=True)

    # Generate and write README
    write_readme(answers, answers['dependencies'], create_new_readme)

    console.print("README.md generated successfully!")
    for dependency in answers['dependencies']:
        console.print(f"- {dependency}", style="bold green")

# ... (rest of the script remains unchanged)

if __name__ == "__main__":
    cli()



## notes for future self
#   should i get rid of the dependencies question and get the info needed from the 
#   installation instructions? 

#   could turn the tests into a class or a dedicated test file 
#   this could let me expand my testing suite!
#   could also use a testing framework like pytest or unitest
#  could also use a linter like pylint or flake8
#   make sure the readme generator has the right information for this Version 
#   could make the prompts more user friendly 
#   could make the readme more user friendly
#   could make the readme more visually appealing
#   could make the readme more standardized
#   could make the readme more structured
#   When handling special characters in the project description, ensure that the 
#   README is generated with proper markdown escaping.


# Long term
#   create a app that pulls information from a link submitted to generate readme

