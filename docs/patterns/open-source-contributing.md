# Contributing to Indigo Open Source Plugins

The [IndigoDomotics GitHub organization](https://github.com/IndigoDomotics) hosts curated open-source Indigo plugins. This guide covers the contribution workflow for submitting changes or new plugins.

## Contribution Workflow

### 1. Create an Issue

Open an issue in the relevant repository to discuss planned changes before starting work. This prevents conflicts with other developers and helps flesh out the approach. Skip this step only when addressing an existing issue.

### 2. Fork the Repository

Fork the repository on GitHub. Keep the fork updated using GitHub's "Fetch & Merge" button before starting new work.

### 3. Make Changes

Implement modifications in the fork. Use unit testing where available and add new tests for changes. Follow the coding and style guide from the [.github repository](https://github.com/IndigoDomotics/.github).

### 4. Comment Changes

Add comments explaining major modifications to help reviewers understand the intent behind changes.

### 5. Commit and Push

Push regularly to the fork as a backup. Use clear, descriptive commit messages.

### 6. Create Beta Releases (Optional)

Create beta releases in the fork for testing with beta testers when possible. This helps catch environment-specific issues before the official review.

### 7. Submit Pull Request

Create a pull request linking to the issue(s) the changes address. Include a clear description of what changed and why.

### 8. Review Process

An open source manager reviews the submission and provides feedback. Address any requested changes and update the PR.

### 9. Approval and Merge

Once approved, managers merge the changes, generate official releases, and update the Indigo Plugin Store.

### 10. Issue Closure

Linked issues are closed with the release version number noted.

## Key Guidelines

- **Discuss first**: Always create an issue before significant work to avoid conflicts
- **Test thoroughly**: Use and add unit tests where available
- **Follow style guides**: Check the [.github repository](https://github.com/IndigoDomotics/.github) for coding standards
- **Keep PRs focused**: Address one issue or feature per pull request
- **Document changes**: Comment code and describe PR changes clearly

## Resources

- **Organization**: https://github.com/IndigoDomotics
- **Style Guide**: https://github.com/IndigoDomotics/.github
- **Developer Forum**: https://forums.indigodomo.com/viewforum.php?f=18
