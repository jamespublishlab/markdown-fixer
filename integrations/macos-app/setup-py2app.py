"""
Build Mac app using py2app (more professional, proper code signing support).

Usage:
    python3 setup-py2app.py py2app
"""

from setuptools import setup

APP = ['app_wrapper.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,  # We handle file drops manually
    # 'iconfile': 'icon.icns',  # Optional - comment out if icon doesn't exist
    'packages': ['markdown_fixer', 'click'],
    'excludes': ['test', 'tests', 'pytest'],
    'plist': {
        'CFBundleName': 'Markdown Fixer',
        'CFBundleDisplayName': 'Markdown Fixer',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'CFBundleIdentifier': 'com.publishlab.markdown-fixer',
        'NSHumanReadableCopyright': 'Copyright © 2025 James. All rights reserved.',
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeName': 'Markdown File',
                'CFBundleTypeRole': 'Editor',
                'LSItemContentTypes': ['net.daringfireball.markdown', 'public.plain-text'],
                'LSHandlerRank': 'Default',
                'CFBundleTypeExtensions': ['md', 'markdown'],
            }
        ],
        'LSMinimumSystemVersion': '10.15.0',
    },
}

setup(
    name='Markdown Fixer',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
