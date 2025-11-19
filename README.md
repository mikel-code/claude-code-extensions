# Claude Code Extensions

> A personal AI toolkit: Custom skills, commands, and agents for Claude Code to supercharge productivity across development, analysis, content creation, and daily workflows.

## Overview

This repository is a curated collection of Claude Code extensions designed to enhance and automate various aspects of work and life. Each extension is built to solve specific problems, streamline workflows, or augment capabilities in different domains.

### What's Inside

- **🛠 Skills** - Reusable capabilities Claude can invoke (e.g., image optimization, data analysis)
- **⚡ Commands** - Quick slash commands for common tasks (e.g., `/scaffold-deck`, `/batch-rename`)
- **🤖 Agents** - Autonomous assistants for complex workflows (e.g., research assistant, recipe optimizer)

## Structure

Extensions are organized by domain for easy discovery and maintenance:

```
claude-code-extensions/
├── coding/                        # Development tools & workflows
│   ├── python/                    # Python-specific extensions
│   └── javascript/                # JavaScript/Node.js extensions
├── communication/                 # Writing & communication
├── data/                          # Data analysis & visualization
├── utilities/                     # General-purpose tools
│   └── command-image-downscale/  # Image optimization command
└── shared/                        # Shared libraries & resources
```

### Planned Expansions

As the toolkit grows, additional domains will include:

- **analysis/** - Data analysis, statistical tools, visualization
- **content-creation/** - Presentations, writing, design
- **knowledge-work/** - Research, synthesis, note organization
- **personal/** - Cooking, learning, planning, lifestyle

## Installation

### Prerequisites

- [Claude Code](https://claude.com/claude-code) installed
- Git for cloning the repository

### Quick Start

1. **Clone this repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/claude-code-extensions.git
   cd claude-code-extensions
   ```

2. **Install specific extensions**

   Each extension has its own installation instructions. Generally:

   **For Commands:**
   ```bash
   # Symlink command file to Claude's commands directory
   ln -s $(pwd)/utilities/command-image-downscale/image-downscale.md ~/.claude/commands/
   ```

   **For Skills:**
   ```bash
   # Option 1: Symlink to keep updates synced
   ln -s $(pwd)/path/to/skill ~/.claude/skills/skill-name

   # Option 2: Copy to Claude's skills directory
   cp -r path/to/skill ~/.claude/skills/
   ```

   **For Agents:**
   ```bash
   # Follow agent-specific setup in each agent's README
   ```

3. **Run setup scripts (if applicable)**
   ```bash
   cd utilities/command-image-downscale
   bash setup.sh
   ```

## Available Extensions

### Utilities

#### Image Downscale (Command)
Downscale large images while preserving text readability. Context-aware command for optimizing specific images in your workflow, plus standalone utility for bulk processing.

- **Type:** Command (+ Python utility)
- **Location:** `utilities/command-image-downscale/`
- **Use Cases:**
  - Command: Optimize images as you work (screenshots, diagrams in notes)
  - Utility: Bulk vault maintenance, scheduled optimization
- **Learn More:** [Image Downscale README](utilities/command-image-downscale/README.md)

**Usage:**
```
/image-downscale path/to/image.png
"Optimize the screenshot I just pasted"
"Downscale images in this note"
```

---

*More extensions coming soon! Check back regularly or watch this repository for updates.*

## Extension Types Explained

### Skills
Skills are specialized capabilities that Claude Code can invoke to perform specific tasks. They:
- Live in `~/.claude/skills/`
- Have a `SKILL.md` file defining their purpose and allowed tools
- Can use Python, shell scripts, or other tools
- Are invoked naturally in conversation

**Example:** "Use the data-analysis skill to process this CSV"

### Commands
Commands are quick slash commands for common tasks. They:
- Live in `~/.claude/commands/`
- Are defined in Markdown files
- Provide templated workflows or quick actions
- Are invoked with `/command-name`

**Example:** `/image-downscale screenshot.png`

### Agents
Agents are autonomous assistants for complex, multi-step workflows. They:
- Can maintain context across multiple interactions
- Make decisions and adapt to changing requirements
- Often combine multiple skills and commands
- Handle end-to-end workflows

**Example:** Research assistant that searches, synthesizes, and formats findings

## Creating Your Own Extensions

### Creating a Skill

1. Create a new directory: `category/your-skill-name/`
2. Add a `SKILL.md` file with frontmatter:
   ```markdown
   ---
   name: your-skill-name
   description: Brief description of what it does
   allowed-tools: Read, Write, Bash, Glob
   ---

   # Your Skill Name

   [Documentation here]
   ```
3. Add implementation scripts in `scripts/`
4. Create a README.md with usage examples
5. Add setup.sh if dependencies are needed

### Creating a Command

1. Create a Markdown file: `category/command-name.md`
2. Write the command prompt/template
3. Symlink to `~/.claude/commands/`

### Creating an Agent

1. Create a new directory: `category/agent-name/`
2. Define agent capabilities and workflows
3. Document in README.md
4. Add any required scripts or configurations

## Contributing

This is a personal toolkit, but if you find these extensions useful:

1. **Star** this repository to show support
2. **Fork** to create your own version
3. **Share** your own extensions via PRs (if you'd like to contribute)
4. **Open Issues** for bugs or enhancement ideas

## Best Practices

### Organization
- Keep extensions focused and single-purpose
- Document thoroughly with examples
- Include setup scripts for dependencies
- Use semantic versioning for major changes

### Naming Conventions
- **Skills:** `skill-descriptive-name/` or just `descriptive-name/`
- **Commands:** `command-action.md` or `/action`
- **Agents:** `agent-role-name/`
- Use lowercase with hyphens

### Documentation
Each extension should include:
- Clear description of purpose
- Installation instructions
- Usage examples
- Configuration options
- Troubleshooting guide

## Philosophy

This toolkit is built on several principles:

1. **Modularity** - Each extension does one thing well
2. **Discoverability** - Clear organization and documentation
3. **Reusability** - Extensions work across different contexts
4. **Maintainability** - Simple, well-documented code
5. **Practicality** - Solves real problems, not theoretical ones

## Resources

- [Claude Code Documentation](https://claude.com/claude-code)
- [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk)
- [MCP Servers](https://github.com/anthropics/mcp-servers)

## License

MIT License - Feel free to use, modify, and distribute as you see fit.

---

**Built with ❤️ using [Claude Code](https://claude.com/claude-code)**

*Last Updated: 2025-11-19*
