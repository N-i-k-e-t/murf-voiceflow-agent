# Contributing to VoiceFlow

Thank you for your interest in contributing to VoiceFlow! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on constructive feedback
- Report inappropriate behavior professionally

## Getting Started

### Prerequisites
- Python 3.8+
- Git
- API keys for Murf, Deepgram, and OpenAI

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/<your-username>/murf-voiceflow-agent.git
cd murf-voiceflow-agent

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install black flake8 mypy pytest pytest-cov

# Copy environment template
cp .env.example .env
# Edit .env with your API keys
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` for new features
- `fix/` for bug fixes
- `docs/` for documentation
- `test/` for tests
- `refactor/` for code cleanup

### 2. Code Quality Standards

Run quality checks before committing:

```bash
# Format code
black app/ tests/

# Check style and errors
flake8 app/ tests/

# Type checking
mypy app/

# Run tests
pytest tests/ -v --cov=app/
```

### 3. Commit Messages

Follow conventional commits:

```
feat: add audio preprocessing features
fix: handle timeout errors in Deepgram client
docs: update API key setup instructions
test: add tests for voice agent
refactor: simplify TTS stream handling
```

### 4. Testing

- Write tests for new features
- Ensure all tests pass: `pytest tests/ -v`
- Aim for >80% code coverage: `pytest --cov=app/`
- Test error cases and edge conditions

### 5. Documentation

- Update README for significant changes
- Add docstrings to new functions/classes
- Include usage examples
- Document configuration changes in .env.example

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request with:
- Clear description of changes
- Link to related issues
- Screenshots/demos if applicable
- Checklist of testing performed

## Pull Request Guidelines

- Keep PRs focused on single feature/fix
- Provide clear description and context
- Link to issue tracker when relevant
- Respond to review comments professionally
- Keep PR up-to-date with main branch

## Reporting Issues

When reporting bugs:
- Describe expected vs actual behavior
- Include error messages/logs
- Specify Python version and OS
- Provide steps to reproduce
- Attach relevant config/environment info

## Performance Considerations

- Monitor API call latencies
- Optimize audio processing
- Reduce memory footprint
- Test with various hardware

## Security Guidelines

- Never commit API keys or secrets
- Validate all user input
- Handle errors gracefully
- Report security issues privately to maintainers

## Project Structure

```
murf-voiceflow-agent/
├── app/              # Main application code
├── tests/            # Unit and integration tests
├── docs/             # Documentation
├── .env.example      # Environment template
├── requirements.txt  # Python dependencies
└── README.md         # Project overview
```

## Questions?

- Open an issue for questions
- Check existing documentation
- Review similar code for patterns
- Ask in pull request comments

Thank you for contributing! 🎉
