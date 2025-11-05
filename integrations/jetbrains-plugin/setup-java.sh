#!/bin/bash
set -e

echo "🔍 Checking for Java installation..."

# Check if Java is installed
if /usr/libexec/java_home -v 17 >/dev/null 2>&1; then
    echo "✅ Java 17+ already installed"
    JAVA_HOME=$(/usr/libexec/java_home -v 17)
    echo "JAVA_HOME: $JAVA_HOME"
    exit 0
fi

echo "❌ Java 17+ not found"
echo ""
echo "📥 Installing Java via Homebrew..."

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew not found. Please install Homebrew first:"
    echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

echo "Installing OpenJDK 17..."
brew install openjdk@17

echo ""
echo "🔗 Creating symlink for system Java..."
sudo ln -sfn /opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-17.jdk

echo ""
echo "✅ Java installation complete!"
echo ""
echo "📝 Add to your shell profile (~/.zshrc or ~/.bash_profile):"
echo ""
echo "    export JAVA_HOME=\$(/usr/libexec/java_home -v 17)"
echo "    export PATH=\"\$JAVA_HOME/bin:\$PATH\""
echo ""
echo "🔄 Then reload your shell:"
echo "    source ~/.zshrc"
echo ""
