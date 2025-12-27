# Quick Start Guide

## Step 1: Install Java 17+

### Option A: Automated Setup (Recommended)

Run the setup script:

```bash
./setup-java.sh
```

Then add to your `~/.zshrc` (or `~/.bash_profile` if using bash):

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 17)
export PATH="$JAVA_HOME/bin:$PATH"
```

Reload your shell:

```bash
source ~/.zshrc
```

### Option B: Manual Installation

**Via Homebrew:**

```bash
# Install OpenJDK 17
brew install openjdk@17

# Create system symlink (requires sudo password)
sudo ln -sfn /opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk \
  /Library/Java/JavaVirtualMachines/openjdk-17.jdk

# Add to ~/.zshrc
echo 'export JAVA_HOME=$(/usr/libexec/java_home -v 17)' >> ~/.zshrc
echo 'export PATH="$JAVA_HOME/bin:$PATH"' >> ~/.zshrc

# Reload shell
source ~/.zshrc
```

**Via Download:**

Download from [Adoptium](https://adoptium.net/temurin/releases/?version=17) and install the `.pkg` file.

### Verify Installation

```bash
java -version
```

Should output:

```
openjdk version "17.0.x" ...
```

## Step 2: Build the Plugin

```bash
# Build the plugin ZIP
./gradlew buildPlugin

# Output: build/distributions/markdown-fixer-plugin-1.0.0.zip
```

## Step 3: Run Tests

```bash
./gradlew test
```

## Step 4: Test in Sandbox IDE

```bash
./gradlew runIde
```

This launches IntelliJ IDEA with your plugin pre-installed.

## Step 5: Install in Your IDE

### From Build

1. Build: `./gradlew buildPlugin`
2. Open your JetBrains IDE
3. Go to **Settings/Preferences** → **Plugins**
4. Click gear icon ⚙️ → **Install Plugin from Disk...**
5. Select: `build/distributions/markdown-fixer-plugin-1.0.0.zip`
6. Restart IDE

### Test It

1. Create or open a `.md` file
2. Right-click in the editor or project view
3. Select **"Fix Markdown Formatting"**
4. Or press **Ctrl+Alt+M** (Cmd+Alt+M on macOS)

## Troubleshooting

### "Unable to locate a Java Runtime"

Even after installing Java, you need to set `JAVA_HOME`:

```bash
# Check if Java is installed
/usr/libexec/java_home -V

# If Java shows up, add to ~/.zshrc:
export JAVA_HOME=$(/usr/libexec/java_home -v 17)
export PATH="$JAVA_HOME/bin:$PATH"

# Reload
source ~/.zshrc
```

### "JAVA_HOME is set to an invalid directory"

```bash
# Find correct path
/usr/libexec/java_home -v 17

# Update JAVA_HOME in ~/.zshrc to match
```

### Gradle Build Fails

```bash
# Clean and rebuild
./gradlew clean build
```

### Tests Fail

Compare with Python implementation:

```bash
cd ../..
python -m pytest tests/test_core.py -v
```

## Common Commands

```bash
# Build plugin
./gradlew buildPlugin

# Run tests
./gradlew test

# Launch sandbox IDE
./gradlew runIde

# Verify plugin
./gradlew verifyPlugin

# Clean build
./gradlew clean

# Run specific test
./gradlew test --tests "MarkdownFixerTest.testBlankLineBeforeList"

# Build with debug output
./gradlew buildPlugin --info
```

## Next Steps

1. ✅ Install Java 17+
2. ✅ Build the plugin
3. ✅ Run tests
4. ✅ Test in sandbox IDE
5. 📝 Customize vendor info in `plugin.xml`
6. 📝 Update README.md with your GitHub links
7. 🚀 Publish to JetBrains Marketplace (optional)

## Resources

- [README.md](README.md) - Full documentation
- [DEVELOPMENT.md](DEVELOPMENT.md) - Developer guide
- [IntelliJ Platform SDK](https://plugins.jetbrains.com/docs/intellij/)
