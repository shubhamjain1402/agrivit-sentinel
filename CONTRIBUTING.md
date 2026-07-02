# Contributing to AgriVit-Sentinel

First off, thank you for considering contributing to AgriVit-Sentinel! It's people like you that make this agricultural intelligence platform better for farmers worldwide.

## 🌟 Ways to Contribute

- 🐛 Report bugs and issues
- 💡 Suggest new features or enhancements
- 📝 Improve documentation
- 🔧 Submit bug fixes
- ✨ Add new features
- 🧪 Write tests
- 🎨 Improve UI/UX

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Git
- Basic understanding of Flask and TensorFlow

### Setup Development Environment

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/shubhamjain1402/agrivit-sentinel.git
   cd agrivit-sentinel
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📋 Development Guidelines

### Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and modular
- Comment complex logic

### Commit Messages

Use clear and descriptive commit messages:

```
feat: Add weather API integration
fix: Resolve pest detection image preprocessing bug
docs: Update installation instructions
style: Format code according to PEP 8
refactor: Optimize crop recommendation algorithm
test: Add unit tests for fertilizer module
```

### Pull Request Process

1. **Update Documentation**: If you add features, update README.md
2. **Test Your Changes**: Ensure all tests pass
3. **Follow Code Style**: Run linting checks
4. **Describe Changes**: Provide clear PR description
5. **Link Issues**: Reference related issues using `#issue-number`

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
Describe testing performed

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests pass
```

## 🐛 Reporting Bugs

### Before Submitting

- Check existing issues to avoid duplicates
- Ensure you're using the latest version
- Verify the bug is reproducible

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What should happen

**Screenshots**
If applicable

**Environment**
- OS: [e.g., Windows 10]
- Python Version: [e.g., 3.8.5]
- Browser: [e.g., Chrome 90]

**Additional Context**
Any other relevant information
```

## 💡 Suggesting Enhancements

### Enhancement Template

```markdown
**Problem Statement**
Describe the problem or limitation

**Proposed Solution**
Your suggested enhancement

**Alternatives Considered**
Other approaches you've thought about

**Additional Context**
Mockups, examples, or references
```

## 🧪 Testing

- Write unit tests for new functionality
- Ensure existing tests pass before submitting PR
- Test on multiple platforms if possible
- Include edge cases in testing

## 📚 Documentation

- Update README.md for user-facing changes
- Add inline comments for complex logic
- Update API documentation if applicable
- Include examples for new features

## 🏗️ Project Structure

```
agrivit-sentinel/
├── app.py              # Main Flask application
├── cnn_model.py        # Pest detection model
├── crop_model.py       # Crop recommendation model
├── utils/              # Utility modules
├── templates/          # HTML templates
├── static/             # CSS, JS, images
└── Data/               # Datasets
```

## 🎯 Priority Areas

We're especially interested in contributions for:

1. **Model Improvements**: Enhance accuracy and performance
2. **UI/UX**: Make the interface more intuitive
3. **Mobile Support**: Responsive design improvements
4. **API Development**: RESTful API for external integrations
5. **Internationalization**: Multi-language support
6. **Documentation**: Tutorials and guides

## 📧 Communication

- **Questions**: Open a GitHub issue with `[Question]` prefix
- **Discussions**: Use GitHub Discussions for general topics
- **Security**: Report vulnerabilities privately to maintainers

## 🙌 Recognition

Contributors will be:
- Listed in README.md acknowledgments
- Credited in release notes
- Recognized in our community

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity, experience level, nationality, personal appearance, race, religion, or sexual identity.

### Our Standards

**Positive Behavior:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what's best for the community
- Showing empathy towards others

**Unacceptable Behavior:**
- Trolling, insulting/derogatory comments
- Public or private harassment
- Publishing others' private information
- Other unprofessional conduct

### Enforcement

Violations may result in temporary or permanent ban from the project.

## ❓ Questions?

Don't hesitate to ask! Open an issue or reach out to maintainers.

---

**Thank you for contributing to AgriVit-Sentinel! Together, we're building better tools for agriculture.** 🌾
