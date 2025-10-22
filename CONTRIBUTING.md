# Contributing to LoL Discord Bot

Thanks for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/yourusername/lol-discord-bot.git
   cd lol-discord-bot
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up your `.env` file** with your Discord and Riot API tokens

## Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions
- Comment complex logic

### Testing
- Test all commands before submitting PR
- Ensure the bot starts without errors
- Check that monitoring system works properly

### Commit Messages
Use clear, descriptive commit messages:
```
feat: Add new champion rotation cache
fix: Resolve thread creation error in forums
docs: Update installation instructions
```

## What We're Looking For

### High Priority
- Bug fixes for existing features
- Performance improvements
- Better error handling
- Documentation improvements

### Features We'd Love
- Support for more Riot APIs (TFT, Valorant)
- Advanced statistics and analytics
- Custom alerts and notifications
- Web dashboard integration

### Please Avoid
- Breaking changes without discussion
- Removing existing features
- Adding dependencies without justification

## Pull Request Process

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the guidelines above

3. **Test thoroughly:**
   - Run the bot locally
   - Test affected commands
   - Check for any errors

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: your feature description"
   ```

5. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request:**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your feature branch
   - Fill out the PR template

## Pull Request Template

```markdown
## Description
Brief description of what this PR does

## Changes Made
- List of specific changes
- Another change
- Etc.

## Testing Done
- Tested on Python 3.10
- Tested commands: /summoner, /track, etc.
- No errors in console

## Screenshots (if applicable)
Add screenshots of the bot in action

## Checklist
- [ ] Code follows style guidelines
- [ ] Added/updated docstrings
- [ ] Tested locally
- [ ] Updated documentation (if needed)
```

## Reporting Issues

When reporting issues, please include:
- Bot version
- Python version
- Error messages (full traceback)
- Steps to reproduce
- Expected vs actual behavior

## Code of Conduct

- Be respectful and constructive
- Help others learn and grow
- Focus on what's best for the community
- Be patient with new contributors

## Questions?

Feel free to:
- Open an issue for discussion
- Ask in pull request comments
- Reach out to maintainers

---

**Thank you for contributing!** Every contribution, no matter how small, helps make this project better! 🎮✨

