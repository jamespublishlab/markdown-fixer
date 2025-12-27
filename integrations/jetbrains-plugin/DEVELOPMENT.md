# Development Guide

## Prerequisites

### Required

- **JDK 17 or later**: Required for building the plugin
  - Check version: `java -version`
  - Download from: https://adoptium.net/ or https://www.oracle.com/java/technologies/downloads/

- **Gradle 8.2+**: Included via wrapper (`./gradlew`)

### Recommended

- **IntelliJ IDEA**: For best development experience
  - Download Community Edition (free): https://www.jetbrains.com/idea/download/

## Quick Start

### 1. Verify Java Installation

```bash
java -version
```

Should output Java 17 or later.

### 2. Build the Plugin

```bash
./gradlew buildPlugin
```

The built plugin ZIP will be in `build/distributions/markdown-fixer-plugin-1.0.0.zip`.

### 3. Run Tests

```bash
./gradlew test
```

### 4. Test in Sandbox IDE

```bash
./gradlew runIde
```

This launches a new IDE instance with your plugin pre-installed.

## Development Workflow

### Making Changes

1. **Edit Kotlin code** in `src/main/kotlin/`
2. **Run tests**: `./gradlew test`
3. **Test in IDE**: `./gradlew runIde`
4. **Build distribution**: `./gradlew buildPlugin`

### Testing the Plugin

#### Option 1: Sandbox IDE (Recommended)

```bash
./gradlew runIde
```

The sandbox IDE runs with:
- Your plugin pre-installed
- Isolated settings and caches
- Full debugging support

#### Option 2: Manual Installation

```bash
# Build the plugin
./gradlew buildPlugin

# Install in your IDE
# Settings → Plugins → Gear Icon → Install Plugin from Disk
# Select: build/distributions/markdown-fixer-plugin-1.0.0.zip
```

### Debugging

```bash
# Run IDE with debug port open
./gradlew runIde --debug-jvm

# Then attach debugger to port 5005
```

Or use IntelliJ IDEA's built-in "Run Plugin" configuration.

## Project Structure

```
src/
├── main/
│   ├── kotlin/com/markdownfixer/
│   │   ├── MarkdownFixer.kt              # Core formatting logic
│   │   └── actions/
│   │       └── FixMarkdownAction.kt      # IDE action
│   └── resources/META-INF/
│       └── plugin.xml                    # Plugin configuration
└── test/
    └── kotlin/com/markdownfixer/
        └── MarkdownFixerTest.kt          # Unit tests
```

## Gradle Tasks

| Task | Description |
|------|-------------|
| `./gradlew test` | Run unit tests |
| `./gradlew buildPlugin` | Build plugin ZIP distribution |
| `./gradlew runIde` | Launch sandbox IDE with plugin |
| `./gradlew verifyPlugin` | Verify plugin structure and compatibility |
| `./gradlew clean` | Clean build artifacts |
| `./gradlew publishPlugin` | Publish to JetBrains Marketplace (requires token) |

## Maintaining Feature Parity with Python

The Kotlin implementation should mirror the Python implementation in `src/markdown_fixer/core.py`.

When making changes:

1. **Update both implementations**:
   - Kotlin: `src/main/kotlin/com/markdownfixer/MarkdownFixer.kt`
   - Python: `../../src/markdown_fixer/core.py`

2. **Update tests in both**:
   - Kotlin: `src/test/kotlin/com/markdownfixer/MarkdownFixerTest.kt`
   - Python: `../../tests/test_core.py`

3. **Run both test suites**:
   ```bash
   # Kotlin tests
   ./gradlew test

   # Python tests (from project root)
   cd ../..
   python -m pytest tests/test_core.py -v
   ```

## Code Style

### Kotlin

- Follow [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html)
- Use 4 spaces for indentation
- Maximum line length: 120 characters

### Documentation

- Add KDoc comments to public APIs
- Keep comments up-to-date with code changes

## Troubleshooting

### Build Fails with "Could not find tools.jar"

You're using a JRE instead of a JDK. Install a full JDK:
- https://adoptium.net/

### "Cannot resolve symbol" in IDE

1. File → Invalidate Caches → Invalidate and Restart
2. Reimport Gradle project

### Tests Pass But Plugin Doesn't Work in IDE

1. Check `plugin.xml` configuration
2. Verify action is registered correctly
3. Check IDE logs: Help → Show Log in Finder
4. Look for errors in `idea.log`

### Sandbox IDE Won't Start

1. Clean build: `./gradlew clean`
2. Delete sandbox: `rm -rf build/idea-sandbox`
3. Rebuild: `./gradlew buildPlugin`
4. Try again: `./gradlew runIde`

## Publishing

### Prerequisites

1. **JetBrains Marketplace Account**: https://plugins.jetbrains.com/
2. **Personal Access Token**: Generate from your account profile
3. **Plugin Signing Certificate**: Generate key pair for signing

### First Publication

1. Upload manually to JetBrains Marketplace
2. Fill in marketplace listing (description, screenshots, etc.)
3. Wait for approval (usually 1-3 days)

### Subsequent Releases

```bash
# Set environment variables
export PUBLISH_TOKEN="your-token"
export CERTIFICATE_CHAIN="$(cat chain.crt)"
export PRIVATE_KEY="$(cat private.key)"
export PRIVATE_KEY_PASSWORD="your-password"

# Publish
./gradlew publishPlugin
```

Or use GitHub Actions (see `.github/workflows/` in project root).

## Resources

- [IntelliJ Platform SDK Docs](https://plugins.jetbrains.com/docs/intellij/)
- [Kotlin Language Guide](https://kotlinlang.org/docs/home.html)
- [JetBrains Marketplace](https://plugins.jetbrains.com/)
- [Plugin DevKit](https://plugins.jetbrains.com/docs/intellij/plugin-development.html)
- [Platform UI Guidelines](https://jetbrains.design/intellij/)

## Getting Help

- Open an issue on GitHub
- Check existing Python implementation for reference
- Review IntelliJ Platform SDK documentation
- Ask in JetBrains Platform Slack
