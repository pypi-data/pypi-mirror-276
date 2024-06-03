## Overview
`readme-ation` automates the generation of a `README.md` file with setup and run instructions tailored for your Python project. By analyzing your project’s Python files, it identifies imported packages, determines their versions, and updates your README with precise environment setup instructions. Additionally, it allows you to seamlessly add comprehensive project descriptions.

## Features
- **Automated README Generation**: Scans Python files to identify imported packages and their versions, generating environment setup instructions for a Mamba environment.
- **Project Description Section**: Enhances your README with detailed project information, including an overview, motivation, technologies used, approach, challenges, key takeaways, and acknowledgments.

## Functions
- **`find_all_py_files(directory)`**: Recursively finds all Python files in the specified directory and its subdirectories.
- **`open_or_create_readme(readme_path)`**: Opens an existing README file or prompts the creation of a new one if it doesn’t exist.
- **`add_setup_with_versions(file_paths, readme_path)`**: Analyzes the specified Python files, identifies package dependencies and their versions, and updates the README with setup and run instructions.
- **`add_project_description(readme_path, project_details)`**: Appends a detailed project description to the README file, including sections such as overview, motivation, technologies used, approach, challenges, key takeaways, and acknowledgments.

## Installation
To install `readme-ation`, use pip:
```shell
pip install readme-ation
```

## Usage
1. **Generate Setup Instructions**:
    ```python
    from readme_ation import find_all_py_files, add_setup_with_versions

    file_paths = find_all_py_files('your_project_directory')
    add_setup_with_versions(file_paths, 'README.md')
    ```

2. **Add Project Description**:
    ```python
    from readme_ation import add_project_description

    project_details = {
        'overview': 'Your project overview here.',
        'motivation': 'The motivation behind your project.',
        'technologies': 'Technologies and tools used in your project.',
        'approach': 'Your approach to solving the problem.',
        'challenges': 'Challenges faced during the project.',
        'key_takeaways': 'Key takeaways and learnings from the project.',
        'acknowledgments': 'Acknowledgments and credits.'
    }

    add_project_description('README.md', project_details)
    ```

## Example
Here is a sample usage demonstrating how to automate the README generation process:

```python
from readme_ation import find_all_py_files, open_or_create_readme, add_setup_with_versions, add_project_description

directory = 'your_project_directory'
readme_path = 'README.md'
file_paths = find_all_py_files(directory)

open_or_create_readme(readme_path)
add_setup_with_versions(file_paths, readme_path)

project_details = {
    'overview': 'This is an example project that demonstrates the usage of readme-ation.',
    'motivation': 'Automating README generation saves time and ensures consistency.',
    'technologies': 'Python, Mamba, and other dependencies.',
    'approach': 'Scanning files for imports and creating setup instructions automatically.',
    'challenges': 'Handling various edge cases in dependency detection.',
    'key_takeaways': 'Using readme-ation can significantly improve your project documentation workflow.',
    'acknowledgments': 'Thanks to all contributors and the open-source community.'
}

add_project_description(readme_path, project_details)
```

## Contributing
Please email me at chuckfinca@gmail.com if you would like to contribute.

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/chuckfinca/readme-ation/blob/main/LICENSE.txt) file for details.
