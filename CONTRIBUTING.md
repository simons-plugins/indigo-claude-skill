# Contributing to Indigo Plugin Skill

Thank you for contributing! This skill helps the entire Indigo development community.

## Types of Contributions

### 1. 📝 Documentation
- Improve existing documentation
- Add missing concepts
- Update for new Indigo versions
- Fix typos and clarify language
- Add diagrams and visual aids

### 2. 💻 Code Examples
- Add new example implementations
- Improve existing examples
- Add comments and explanations
- Show different approaches to same problem

### 3. 🔧 Troubleshooting
- Document common issues
- Share debugging techniques
- Add solutions to known problems
- Include error messages and fixes

### 4. 🎯 Code Snippets
- Reusable code templates
- Common patterns
- Utility functions
- Boilerplate code

### 5. 🏗️ Patterns
- Document design patterns
- Share architectural approaches
- Best practices
- Anti-patterns to avoid

## How to Contribute

### 1. Fork and Clone

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR-USERNAME/indigo-claude-skill.git
cd indigo-claude-skill
git remote add upstream https://github.com/simons-plugins/indigo-claude-skill.git
```

### 2. Create a Branch

```bash
# For documentation
git checkout -b docs/add-device-state-guide

# For examples
git checkout -b example/add-rest-api-plugin

# For fixes
git checkout -b fix/typo-in-lifecycle-docs
```

### 3. Make Changes

Follow the style guides below and make your changes.

### 4. Test Your Changes

- Ensure markdown renders correctly
- Verify all links work
- Test code snippets for syntax errors
- Check spelling and grammar

### 5. Commit

```bash
git add .
git commit -m "docs: add comprehensive device state management guide"
```

Use conventional commit messages:
- `docs:` - Documentation changes
- `example:` - New or updated examples
- `fix:` - Bug fixes or corrections
- `snippet:` - New code snippets
- `chore:` - Maintenance tasks

### 6. Push and Create Pull Request

```bash
git push origin your-branch-name
```

Then create a pull request on GitHub with:
- Clear description of changes
- Reference any related issues
- Screenshots if relevant
- Testing notes

## Documentation Style Guide

### File Structure

```markdown
# Title (H1) - One per document

Brief overview paragraph explaining what this document covers.

## Main Section (H2)

Content with explanations and examples.

### Subsection (H3)

More specific content.

#### Details (H4)

Fine details when needed.
```

### Writing Style

- **Be clear and concise**: Use simple language
- **Be specific**: "Use `self.sleep(60)`" not "wait a bit"
- **Be practical**: Include real-world examples
- **Be complete**: Don't assume prior knowledge
- **Be accurate**: Test all code examples

### Code Examples

Always include:
1. Context about when to use it
2. Complete, working code
3. Comments explaining non-obvious parts
4. Expected output or behavior

```python
def deviceStartComm(self, dev):
    """Called when device communication starts.

    This is called when a device is enabled or when the plugin starts
    with the device already enabled.

    Args:
        dev: The Indigo device object being started
    """
    # ALWAYS call super() first
    super().deviceStartComm(dev)

    # Initialize device-specific resources
    self.logger.info(f"Starting device: {dev.name}")

    # Set initial state
    dev.updateStateOnServer("onOffState", False)
```

### Links

- Use relative links within documentation: `[Device Types](../core-concepts/device-types.md)`
- Use absolute URLs for external resources: `[Indigo Docs](https://www.indigodomo.com/docs/plugin_guide)`
- Always verify links work
- Use descriptive link text, not "click here"

### Images and Diagrams

- Place in `docs/images/` directory
- Use descriptive filenames: `plugin-lifecycle-diagram.png`
- Include alt text for accessibility
- Keep file sizes reasonable (<500KB)

## Code Snippet Standards

### File Naming

- `plugin-base-template.py` - Full plugin templates
- `device-startup.py` - Specific feature snippets
- `validation-example.py` - Example implementations

### Snippet Format

```python
"""
Brief description of what this snippet does.

Usage:
    Explain how to use this snippet in their plugin.

Notes:
    - Any important considerations
    - Version requirements
    - Dependencies
"""

# Imports needed
import indigo

# The actual code snippet
def example_method(self):
    """Clear docstring."""
    # Implementation with comments
    pass
```

## Documentation Standards

### Must Include

- ✅ Clear title and description
- ✅ Code examples where relevant
- ✅ Links to related documentation
- ✅ Version information if specific to a version

### Should Include

- 📝 Common use cases
- ⚠️ Common pitfalls
- 💡 Tips and best practices
- 🔗 Links to official documentation

### Nice to Have

- 📊 Diagrams
- 🎥 Screenshots
- 📚 Further reading
- 🔄 Comparison of approaches

## Review Process

1. **Automated Checks**: Markdown linting, link validation, code syntax
2. **Maintainer Review**: Content accuracy, clarity, completeness
3. **Community Feedback**: Optional discussion period for major changes
4. **Merge**: Usually within 3-7 days

## Example Contributions

### Good Documentation PR

```markdown
# Add: Comprehensive guide to device state management

## Changes
- New document: `docs/core-concepts/state-management.md`
- Covers state types, update patterns, and performance
- Includes 5 code examples
- Links to related API reference docs

## Testing
- Verified all code examples compile
- Tested all internal links
- Spell-checked content
```

### Good Example PR

```markdown
# Add: REST API integration example

## Changes
- New example: `docs/examples/rest-api-integration/`
- Complete working plugin showing REST API patterns
- Demonstrates error handling and rate limiting
- Includes configuration UI example

## Testing
- Tested plugin in Indigo 2023.2
- Verified all API calls work
- Documented setup steps
```

## Questions?

- Open a [Discussion](https://github.com/simons-plugins/indigo-claude-skill/discussions) for general questions
- Open an [Issue](https://github.com/simons-plugins/indigo-claude-skill/issues) for bugs or feature requests
- Tag maintainers with @mention for urgent matters

## Code of Conduct

- Be respectful and welcoming
- Focus on what's best for the community
- Show empathy towards others
- Accept constructive criticism gracefully
- Be patient with new contributors

Thank you for making the Indigo developer community better! 🎉
