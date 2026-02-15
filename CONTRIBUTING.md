# Contributing Guide

Thank you for your interest in contributing to the Nuki Web API integration for Home Assistant! 🎉

## How to Contribute

### Report Bugs

If you find a bug:

1. **Check** if it hasn't been reported already in Issues
2. **Create a new Issue** with:
   - Descriptive title
   - Detailed problem description
   - Steps to reproduce
   - Expected vs actual behavior
   - Relevant logs (enable debug logging)
   - Home Assistant version
   - Nuki lock model

### Request Features

Have an idea to improve the integration?

1. **Check** if it hasn't been suggested already
2. **Create an Issue** with:
   - Descriptive title
   - Feature description
   - Use cases
   - Implementation proposal (if you have one)

### Contribute Code

#### Preparation

1. **Fork** the repository
2. **Clone** your fork:
   ```bash
   git clone https://github.com/your-username/nuki-webapi-ha.git
   cd nuki-webapi-ha
   ```
3. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/descriptive-name
   ```

#### Development

1. **Make your changes** following existing code style
2. **Test** your changes in an HA installation
3. **Verify** you don't introduce errors
4. **Document** any relevant changes

#### Code Style

- Follow [PEP 8](https://pep8.org/)
- Use type hints in Python
- Document functions and classes with docstrings
- Variable/function names in English
- Comments can be in English

#### Commits

- Use descriptive messages in English
- Recommended format:
  ```
  type: brief description

  More detailed description if needed.
  ```

**Commit types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting, spaces, etc.
- `refactor`: Code refactoring
- `test`: Add or modify tests
- `chore`: Maintenance tasks

#### Pull Request

1. **Push** your changes
2. **Create a Pull Request** on GitHub
3. **Describe** your changes clearly
4. **Wait** for review and feedback

## Code of Conduct

- Be respectful and constructive
- Accept constructive criticism
- Focus on what's best for the project
- We don't tolerate harassment or inappropriate behavior

## Questions

Have questions about contributing?

- Open an Issue with the `question` label
- Review existing documentation
- Search in closed Issues

## Acknowledgments

All contributors will be recognized in README and/or CHANGELOG.

Thank you for making this integration better! 🙌
