# Markdown Fixer - JetBrains Plugin

A native JetBrains IDE plugin that automatically fixes common markdown formatting issues.

## Features

- **Proper List Spacing**: Adds blank lines before and after lists for better readability
- **Field Metadata Conversion**: Converts consecutive field-style metadata (`**Key:** value`) to bulleted lists
- **Newline Collapsing**: Collapses 3+ consecutive blank lines to exactly 2
- **Table Formatting**: Automatically formats markdown tables with proper alignment and column widths
- **Unicode Support**: Handles CJK characters (中文, 日本語), emoji (😀, ✅), and other wide characters in tables
- **Code Block Preservation**: Never modifies content inside code blocks

## Supported IDEs

This plugin works with all JetBrains IDEs version 2024.3 and later:

- IntelliJ IDEA (Community & Ultimate)
- PyCharm
- WebStorm
- PhpStorm
- GoLand
- RubyMine
- CLion
- DataGrip
- Rider
- And more...

## Installation

### Method 1: From ZIP File (Manual Installation)

1. Download the latest plugin ZIP from the releases
2. Open your JetBrains IDE
3. Go to **Settings/Preferences** → **Plugins**
4. Click the gear icon (⚙️) → **Install Plugin from Disk...**
5. Select the downloaded ZIP file
6. Restart the IDE

### Method 2: From JetBrains Marketplace (Coming Soon)

Once published to the marketplace:

1. Open your JetBrains IDE
2. Go to **Settings/Preferences** → **Plugins**
3. Search for "Markdown Fixer"
4. Click **Install**
5. Restart the IDE

## Usage

### Right-Click Menu

1. Right-click on any markdown file (`.md` or `.markdown`) in:
   - **Project View** (file tree)
   - **Editor** (while editing)
2. Select **"Fix Markdown Formatting"**
3. The file will be formatted automatically

### Keyboard Shortcut

Press **Ctrl+Alt+M** (or **Cmd+Alt+M** on macOS) while viewing a markdown file.

### Tools Menu

Go to **Tools** → **Fix Markdown Formatting**

## Examples

### Before
```markdown
**Author:** James **Status:** Complete
- Item 1
- Item 2
Text after list


Multiple blank lines above
```

### After
```markdown
- **Author:** James
- **Status:** Complete

- Item 1
- Item 2

Text after list

Multiple blank lines above
```

## Building from Source

### Prerequisites

- JDK 17 or later
- Gradle 8.2+ (wrapper included)

### Build Steps

```bash
cd integrations/jetbrains-plugin

# Build the plugin
./gradlew buildPlugin

# Run tests
./gradlew test

# Run in sandbox IDE (for testing)
./gradlew runIde

# Verify plugin
./gradlew verifyPlugin
```

The built plugin ZIP will be in `build/distributions/`.

## Development

### Project Structure

```
jetbrains-plugin/
├── src/main/
│   ├── kotlin/com/markdownfixer/
│   │   ├── MarkdownFixer.kt              # Core logic
│   │   └── actions/
│   │       └── FixMarkdownAction.kt      # IDE action
│   └── resources/META-INF/
│       └── plugin.xml                    # Plugin configuration
├── src/test/
│   └── kotlin/com/markdownfixer/
│       └── MarkdownFixerTest.kt          # Unit tests
├── build.gradle.kts                       # Gradle build config
└── gradle.properties                      # Plugin metadata
```

### Running Tests

```bash
./gradlew test
```

Tests mirror the Python CLI tests to ensure feature parity between implementations.

### Testing in Sandbox

```bash
./gradlew runIde
```

This launches a new IDE instance with your plugin installed in an isolated sandbox environment.

## Relationship to Python CLI

This plugin is part of the larger [markdown-fixer](../../README.md) project, which includes:

- **Python CLI**: Command-line tool and library
- **macOS App**: Drag-and-drop application
- **macOS Quick Action**: Finder right-click integration
- **JetBrains External Tool**: External tool configuration (legacy)
- **JetBrains Plugin**: This native plugin (recommended for JetBrains users)
- **MCP Server**: Claude Desktop integration
- **Claude Code Integration**: Slash commands and hooks

The Kotlin implementation in this plugin maintains feature parity with the Python core logic.

## Troubleshooting

### Plugin Doesn't Appear in Menu

- Check that you're right-clicking on a `.md` or `.markdown` file
- Verify the plugin is enabled in **Settings** → **Plugins**
- Try restarting the IDE

### "No Changes" Notification

The file is already properly formatted! The plugin only modifies files that need fixes.

### Build Errors

- Ensure you're using JDK 17 or later: `java -version`
- Clean and rebuild: `./gradlew clean build`
- Check that you have internet access (Gradle needs to download dependencies)

### Tests Failing

If tests fail, please compare with the Python implementation to ensure logic parity:

```bash
cd ../..  # Return to project root
python -m pytest tests/test_core.py -v
```

## Contributing

When making changes to the core logic:

1. Update both the Kotlin implementation here AND the Python implementation in `src/markdown_fixer/core.py`
2. Run tests in both implementations to ensure parity
3. Update test cases in both `src/test/kotlin/` and `tests/` if needed

## License

MIT License - See [LICENSE](../../LICENSE) in the project root.

## Links

- [Main Project Documentation](../../README.md)
- [Python CLI Documentation](../../GETTING_STARTED.md)
- [JetBrains Plugin Development Docs](https://plugins.jetbrains.com/docs/intellij/)
- [Report Issues](https://github.com/yourrepo/markdown-fixer/issues)
