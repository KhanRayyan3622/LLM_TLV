# Claude Code Container

## Overview

This directory provides a setup process for code conversion of a Verilog project. It provides a Docker safe-ish environment to run Claude Code in "dangerously skip permissions" mode. "Setup agent" instructions establish project-specific instructions for "conversion agents". This directory is copied to the project directory to prepare the project for conversion.

See `../README.md` for a description of the overall conversion process.

## Security Features

### Container Security
- **Non-root execution**: Runs as user `claude` (UID 1001)
- **Capability dropping**: Minimal Linux capabilities
- **Process limits**: Resource constraints for safety (max 100 PIDs)
- **Tmpfs mounts**: Isolated temporary storage for /tmp and /workspace/temp
- **Network isolation**: Bridge network with no host access
- **Security options**: No new privileges allowed

### Jailfree Mode
- **Dangerous executions allowed**: Pre-configured for full automation
- **Auto-trusted workspace**: No trust prompts during analysis
- **Comprehensive tool permissions**: Access to all tools via wildcard allowlist
