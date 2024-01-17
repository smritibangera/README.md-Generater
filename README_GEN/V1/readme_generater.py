def generate_readme(answers, dependencies):
    # Customize this function to format and structure your README.md
    readme_content = f"# {answers['project_name']}\n\n" \
                     f"## Description\n{answers['project_description']}\n\n" \
                     f"## Project Links\n" \
                     f"- [Homepage]({answers['project_homepage']})\n" \
                     f"- [Documentation]({answers['project_doc_url']})\n\n" \
                     f"## Author\n{answers['author']}\n\n" \
                     f"## License\n{answers['license_name']}\n\n" \
                     f"## Installation\n```bash\n{answers['install_command']}\n```\n\n" \
                     f"## Usage\n```bash\n{answers['usage_instructions']}\n```\n\n" \
                     f"## Testing\n```bash\n{answers['test_command']}\n```\n"

    # Include Dependencies section only if there are dependencies
    if dependencies:
        readme_content += "\n## Dependencies\n" + "\n".join(f"- {dep}" for dep in dependencies)

    return readme_content

def write_readme(answers, dependencies):
    # Generate README content
    readme_content = generate_readme(answers, dependencies)

    # Write README content to a file
    with open('README.md', 'w') as readme_file:
        readme_file.write(readme_content)

    # Write dependencies to requirements.txt
    with open('requirements.txt', 'w') as requirements_file:
        for dep in dependencies:
            requirements_file.write(dep + '\n')

    print("README.md and requirements.txt generated successfully!")

    
def get_dependencies():
    """
    Get user input for project dependencies.

    Returns:
        str: Formatted string of project dependencies.
    """
    while True:
        dependencies = input("Enter project dependencies (comma-separated): ").strip()
        if dependencies:
            return dependencies.split(",")
        else:
            print("Dependency list cannot be empty. Please try again.")

def get_user_input(prompt, allow_empty=False):
    """
    Get user input and ensure it is not empty unless specified.

    Args:
        prompt (str): The prompt to display to the user.
        allow_empty (bool): If True, allows empty input.

    Returns:
        str: User input.
    """
    while True:
        user_input = input(prompt).strip()
        if user_input or allow_empty:
            return user_input
        else:
            print("Input cannot be empty. Please try again.")

def main():
    print("ENTER PROJECT INFORMATION:")
    answers = {
        'project_name': get_user_input("Enter the project name:"),
        'project_description': get_user_input("Describe your project:"),
        'project_homepage': get_user_input("Enter the project homepage URL:"),
        'project_doc_url': get_user_input("Enter the project documentation URL:"),
        'author': get_user_input("Enter the author's name:"),
        'license_name': get_user_input("Enter the license name:"),
        'install_command': get_user_input("Enter the installation command:"),
        'usage_instructions': get_user_input("Enter usage instructions:"),
        'test_command': get_user_input("Enter the test command:"),
        'dependencies': get_dependencies()
    }

    if not answers['project_name']:
        print("Exiting without generating README.")
        return
    
    # Generate and write README
    write_readme(answers, answers['dependencies'])
    
    print("README.md generated successfully!")
    
    for dependency in answers['dependencies']:
        print(f"- {dependency}")

def run_tests():
    # Test generate_readme function
    test_answers = {
        'project_name': 'README.md Generator',
        'project_description': 'Description of test project.',
        'project_homepage': 'https://github.com/testuser/testproject',
        'project_doc_url': 'https://testproject.readthedocs.io/',
        'author': 'Jane Doe',
        'license_name': 'MIT',
        'install_command': 'pip install testproject',
        'usage_instructions': 'python testproject.py',
        'test_command': 'pytest',
        'dependencies': ['dependency1', 'dependency2']
    }

    generated_readme = generate_readme(test_answers, test_answers['dependencies'])
    
    # Call write_readme to generate the README file
    write_readme(test_answers, test_answers['dependencies'])

    assert 'Test Project' in generated_readme
    assert 'Description of test project.' in generated_readme
    assert 'https://github.com/testuser/testproject' in generated_readme

    print("All tests passed successfully!")
 
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

    print("Additional tests passed successfully!")


if __name__ == "__main__":
    # Check if the script is run with a command-line argument
    if len(__import__("sys").argv) > 1:
        option = __import__("sys").argv[1].lower()

        if option == 'test':
            run_tests()
            run_additional_tests()
        elif option == 'main':
            print("ENTER PROJECT INFORMATION:")
            answers = {
                'project_name': get_user_input("Enter the project name:"),
                'project_description': get_user_input("Describe your project:"),
                'project_homepage': get_user_input("Enter the project homepage URL:"),
                'project_doc_url': get_user_input("Enter the project documentation URL:"),
                'author': get_user_input("Enter the author's name:"),
                'license_name': get_user_input("Enter the license name:"),
                'install_command': get_user_input("Enter the installation command:"),
                'usage_instructions': get_user_input("Enter usage instructions:"),
                'test_command': get_user_input("Enter the test command:")
            }

            dependencies = get_dependencies()
            # Generate and write README
            
            write_readme(answers, dependencies)

        else:
            print("Invalid option. Use 'test' or 'main'.")
    else:
        print("Usage: python your_script_name.py <option>")
        print("Options:")
        print("  - test: Run tests")
        print("  - main: Run main function") 
   