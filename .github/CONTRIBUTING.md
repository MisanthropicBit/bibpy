# Contributing Guidelines

Please ensure the following when contributing:

1. Check that a similar issue has not already been submitted.
2. [Your commit messages do not
  suck](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html).
3. All commits have been squashed into one commit (when your PR is accepted).
4. You follow the existing coding style.
5. Specify the version of your operating system and Python.
6. Specify if your problem is related to bibtex or biblatex, if applicable.
7. Steps to reproduce a bug, if applicable.

# Creating A Pull Request

1. Fork the repository.
2. Install the [test requirements](/test-requirements.txt).
3. Use flake8 and pydocstyle for formatting and in general follow.
   the existing coding style.
4. Tests can be run with tox or using pytest:
   ```bash
   python3 -m venv my-venv
   source my-venv/bin/activate  # Or 'my-venv/Scripts/activate.bat' on Windows
   pytest tests
   ```
5. Commit your changes, push and create a pull request.

Read more about pull requests
[here](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests).
