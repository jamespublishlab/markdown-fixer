# Claude Desktop Setup - Simple Guide for Non-Technical Users

**No coding required!** Just copy, paste, and click.

## What This Does

After setup, you can ask Claude in Claude Desktop to fix badly formatted markdown, and it will do it automatically.

**Example:**
```
You: "Fix this markdown:
**Name:** John
**Age:** 30
- Item"

Claude: [Uses markdown-fixer tool]
"Here's the fixed version:
- **Name:** John
- **Age:** 30

- Item"
```

---

## ⚠️ Before You Start

**You need:**

- ✅ A Mac (macOS) or Windows computer
- ✅ Claude Desktop installed
- ✅ 5 minutes

**You do NOT need:**

- ❌ Programming knowledge
- ❌ Terminal skills
- ❌ To understand what Python is

---

## 📋 Step-by-Step Instructions

### Step 1: Download the Files

**Option A: Simple Download (Recommended)**

1. Click this link: [Download markdown-fixer](https://github.com/jamespublishlab/markdown-fixer/archive/refs/heads/main.zip)
2. Your browser will download a ZIP file
3. **Double-click** the ZIP file to unzip it
4. You'll see a folder called `markdown-fixer-main`
5. **Drag this folder** to your Desktop (so it's easy to find)

**Option B: If the Link Doesn't Work**

1. Go to: https://github.com/jamespublishlab/markdown-fixer
2. Click the green **Code** button
3. Click **Download ZIP**
4. Double-click to unzip
5. Drag folder to Desktop

### Step 2: Install Python (If You Don't Have It)

**Check if you already have Python:**

1. Open **Spotlight** (press `Command + Space` on Mac, or Windows key on Windows)
2. Type: `terminal` (Mac) or `cmd` (Windows)
3. Press Enter
4. Type: `python3 --version` and press Enter
5. If you see something like `Python 3.11.5`, **skip to Step 3**

**If you see an error, install Python:**

**On Mac:**

1. Go to: https://www.python.org/downloads/
2. Click the big yellow **Download Python** button
3. Open the downloaded file
4. Click through the installer (just keep clicking "Continue" and "Install")
5. Done!

**On Windows:**

1. Go to: https://www.python.org/downloads/
2. Click **Download Python**
3. Open the downloaded file
4. ⚠️ **IMPORTANT**: Check the box "Add Python to PATH"
5. Click **Install Now**
6. Done!

### Step 3: Install markdown-fixer

**Copy and paste these commands:**

1. Open **Terminal** (Mac) or **Command Prompt** (Windows)
   - Mac: Press `Command + Space`, type `terminal`, press Enter
   - Windows: Press Windows key, type `cmd`, press Enter

2. **For Mac**, copy this command:
   ```bash
   pip3 install --user markdown-fixer
   ```

   **For Windows**, copy this command:
   ```bash
   pip install --user markdown-fixer
   ```

3. **Paste** it into the Terminal window (right-click → Paste, or Cmd+V / Ctrl+V)

4. Press **Enter**

5. Wait for it to finish (you'll see lots of text scroll by - this is normal, usually takes 10-30 seconds)

6. When it's done, you'll see your prompt again (might say something like `~ %` or `C:\Users\YourName>`)

7. **Don't close the Terminal yet!** We need it for one more step.

**Note:** The `--user` flag installs markdown-fixer for your user account only (safer than system-wide install).

### Step 4: Find Your Claude Desktop Config File

**On Mac:**

1. Open **Finder**
2. Click **Go** in the menu bar at the top
3. Hold down the **Option key** (you'll see "Library" appear in the menu)
4. Click **Library**
5. Open the **Application Support** folder
6. Look for a **Claude** folder
   - If you **don't see it**, create it: Right-click → New Folder → Name it "Claude"
7. Open the **Claude** folder
8. Look for a file called `claude_desktop_config.json`
   - If you **don't see it**, you'll create it in the next step

**On Windows:**

1. Press **Windows key + R**
2. Type: `%APPDATA%`
3. Press Enter
4. Look for a **Claude** folder
   - If you **don't see it**, create it: Right-click → New → Folder → Name it "Claude"
5. Open the **Claude** folder
6. Look for a file called `claude_desktop_config.json`
   - If you **don't see it**, you'll create it in the next step

### Step 5: Edit the Config File

**If the file EXISTS (you found it in Step 4):**

1. **Right-click** the file `claude_desktop_config.json`
2. Choose **Open With** → **TextEdit** (Mac) or **Notepad** (Windows)
3. You'll see something like this:
   ```json
   {
     "mcpServers": {
       ...existing stuff...
     }
   }
   ```
4. **Keep the existing stuff!** We're just adding to it
5. **Skip to "Adding the Configuration" below**

**If the file DOESN'T EXIST (you need to create it):**

1. Open **TextEdit** (Mac) or **Notepad** (Windows)
2. Click **Format** → **Make Plain Text** (Mac only - very important!)
3. **Skip to "Adding the Configuration" below**

### Step 6: Adding the Configuration

**Copy this entire block:**

**For Mac**, copy this:
```json
{
  "mcpServers": {
    "markdown-fixer": {
      "command": "python3",
      "args": [
        "-m",
        "markdown_fixer.mcp_server"
      ]
    }
  }
}
```

**For Windows**, copy this:
```json
{
  "mcpServers": {
    "markdown-fixer": {
      "command": "python",
      "args": [
        "-m",
        "markdown_fixer.mcp_server"
      ]
    }
  }
}
```

**Now paste it:**

**If this is a NEW file (you just created it):**

1. Just paste the text you copied
2. Save the file as `claude_desktop_config.json` in the Claude folder
   - **Make sure** it ends with `.json` NOT `.txt`!

**If the file ALREADY EXISTS:**

1. You'll see existing content
2. Find the `"mcpServers": {` line
3. **Inside** the `{` after `mcpServers`, add a comma after the last item
4. Add the `"markdown-fixer"` section
5. It should look like:
   ```json
   {
     "mcpServers": {
       "existing-server": {
         ...
       },
       "markdown-fixer": {
         "command": "python3",
         "args": ["-m", "markdown_fixer.mcp_server"]
       }
     }
   }
   ```

**Save the file!**

### Step 7: Restart Claude Desktop

1. **Quit Claude Desktop completely**
   - Mac: Press `Command + Q` or Right-click icon → Quit
   - Windows: Right-click icon → Exit
2. **Open Claude Desktop again**
3. Wait for it to fully load

### Step 8: Test It!

Ask Claude:

```
Can you fix this markdown for me?

**Name:** John Doe
**Age:** 30
- List item
More text
```

If it works, Claude will respond with properly formatted markdown!

If Claude says it can't find the tool, see **Troubleshooting** below.

---

## 🆘 Troubleshooting

### "I can't find the Claude folder!"

**On Mac:**

- Make sure you're holding the **Option key** when clicking the Go menu
- If Library still doesn't show: Open Finder → Press `Command + Shift + G` → Type `~/Library` → Press Enter

**On Windows:**

- Make sure you typed `%APPDATA%` correctly (with the percent signs)
- Try: `C:\Users\YourUsername\AppData\Roaming\Claude`

### "Claude says it can't find markdown-fixer"

**Check if it's installed:**

1. Open Terminal/Command Prompt
2. Type: `pip3 show markdown-fixer` (or `pip show markdown-fixer` on Windows)
3. If you see "not found", run: `pip3 install markdown-fixer` again

**Try the full path method:**

Instead of the config above, try this (find your exact path first):

1. Open Terminal/Command Prompt
2. Type: `which markdown-fixer` (Mac) or `where markdown-fixer` (Windows)
3. Copy the path it shows
4. Use that full path in the config:

```json
{
  "mcpServers": {
    "markdown-fixer": {
      "command": "/full/path/to/markdown-fixer",
      "args": []
    }
  }
}
```

### "The file is called claude_desktop_config.json.txt"

Your computer is hiding the real extension!

**On Mac:**

1. Right-click the file → Get Info
2. Delete `.txt` from the name
3. Click "Use .json"

**On Windows:**

1. Open File Explorer
2. Click **View** → Check **File name extensions**
3. Rename the file to remove `.txt`

### "I'm getting JSON errors"

**Common mistakes:**

- ❌ Missing commas between items
- ❌ Extra comma after the last item
- ❌ Missing quotes around text
- ❌ Missing curly braces `{}`

**Easy fix:**

1. Delete everything in the file
2. Copy the template again (from Step 6)
3. Paste fresh
4. Save

### "It's still not working!"

**Reset everything:**

1. Delete the `claude_desktop_config.json` file
2. Quit Claude Desktop
3. Follow Steps 4-7 again from scratch
4. Create a fresh config file

**Still stuck?**

Open an issue with screenshots: https://github.com/jamespublishlab/markdown-fixer/issues

Include:

- Your operating system (Mac or Windows, which version)
- A screenshot of your claude_desktop_config.json file
- What happens when you ask Claude to fix markdown

---

## ❓ Common Questions

**Q: Do I need to keep Terminal/Command Prompt open?**
A: No! Close it after Step 3. You're done with it.

**Q: Will this break my Claude Desktop?**
A: No. If something goes wrong, just delete the config file and restart.

**Q: Do I need to do this again after updating Claude?**
A: No. Once set up, it stays set up.

**Q: Can I undo this?**
A: Yes! Just delete the `markdown-fixer` section from the config file.

**Q: What if I use Linux?**
A: See the [full MCP guide](integrations/mcp-server/README.md) - it's more technical.

**Q: This is too complicated! Is there an easier way?**
A: Not yet, but we're working on it! For now, this is the simplest method.

---

## ✅ Success! What Now?

Now you can ask Claude in Claude Desktop to:

- "Fix this markdown: [paste your content]"
- "Clean up this markdown file"
- "Format this markdown properly"

Claude will automatically use markdown-fixer to clean it up!

**Enjoy!** 🎉

---

## 💡 What Happened?

In simple terms:

1. You installed a tool (markdown-fixer) that fixes markdown
2. You told Claude Desktop where to find that tool
3. Now Claude can use it whenever you ask

That's it! No magic, just connecting two programs together.

---

## 📚 Want to Learn More?

- [What markdown-fixer fixes](README.md#what-it-fixes)
- [Other ways to use it](GETTING_STARTED.md)
- [Technical details](integrations/mcp-server/README.md) (for developers)

---

**Made with ❤️ for non-technical users**

If this guide helped you, star the project: https://github.com/jamespublishlab/markdown-fixer
