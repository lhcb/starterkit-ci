# PyPI Trusted Publishing Setup

This repository uses GitHub Actions and PyPI trusted publishing to automatically publish packages.

## How It Works

The workflow in `.github/workflows/publish.yml` will:

1. **On every PR and push to main**: Build the package to ensure it builds correctly
2. **On tag pushes**: Build and automatically publish to PyPI using trusted publishing

## Setting Up PyPI Trusted Publishing

To enable trusted publishing for this package on PyPI, a PyPI maintainer needs to:

1. Go to https://pypi.org/manage/project/starterkit-ci/settings/publishing/
   (Note: PyPI normalizes package names, so `starterkit-ci` and `starterkit_ci` refer to the same project)
2. Add a new "pending publisher" with the following details:
   - **PyPI Project Name**: `starterkit_ci` (as defined in pyproject.toml)
   - **Owner**: `lhcb`
   - **Repository name**: `starterkit-ci`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi`

3. Once configured, simply push a tag to trigger a release:
   ```bash
   git tag v0.3.0
   git push origin v0.3.0
   ```

## Benefits of Trusted Publishing

- No API tokens needed - more secure
- Automatic token rotation
- Scoped to specific workflows
- GitHub verifies identity through OIDC

## References

- [PyPI Trusted Publishing Documentation](https://docs.pypi.org/trusted-publishers/)
- [GitHub Actions OIDC Documentation](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
