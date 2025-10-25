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
    'iconfile': 'icon.icns',
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
    'packages': ['markdown_fixer'],
}

setup(
    name='Markdown Fixer',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
