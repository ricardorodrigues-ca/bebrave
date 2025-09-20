![](bebrave.png)

# BeBrave for macOS

BeBrave is a powerful Python script designed for macOS users to streamline their Brave Browser experience by toggling and configuring unwanted features. With BeBrave, you can easily disable or enable various Brave functionalities, customize settings, and improve privacy.

## Features

### Privacy & Security Controls
- **Telemetry & Reporting**: Disable metrics reporting, safe browsing data collection, URL data collection, and feedback surveys
- **Privacy Settings**: Configure autofill, password manager, browser sign-in, WebRTC IP leak protection
- **Security Options**: Block third-party cookies, enable Do Not Track, force Google SafeSearch
- **Network Protection**: Disable QUIC protocol, configure DNS over HTTPS

### Brave-Specific Features
- **Brave Rewards**: Toggle rewards system
- **Brave Wallet**: Enable/disable cryptocurrency wallet
- **Brave VPN**: Control VPN functionality
- **Brave AI Chat**: Toggle AI chat features
- **Brave Shields**: Configure ad/tracker blocking
- **Tor Integration**: Enable/disable Tor functionality
- **Sync Services**: Control data synchronization

### Performance & Bloat Removal
- **Background Processes**: Disable background mode and unnecessary services
- **Media & Shopping**: Turn off recommendations and shopping lists
- **Browser Features**: Disable translate, spellcheck, promotions, search suggestions
- **Developer Tools**: Optionally disable developer tools access

### Configuration Management
- **Bulk Operations**: Select all/none options for quick configuration
- **Export/Import**: Save and restore configuration sets as JSON files
- **DNS Configuration**: Configure DNS over HTTPS modes (automatic, off, custom)

## Requirements

- macOS
- Python 3.x (with tkinter support)
- Administrator privileges (sudo) for applying changes

## Installation

1. Clone or download this repository
2. No additional dependencies required - uses only Python standard library

## Usage

### Running the Application

```bash
# For viewing current settings (read-only)
python3 bebrave_macos.py

# For making changes (requires sudo)
sudo python3 bebrave_macos.py
```

### Using the GUI

1. **Permission Banner**: The top banner indicates whether you have sufficient privileges
   - Red banner: Read-only mode (run with sudo to make changes)
   - Green banner: Administrator mode (can apply changes)

2. **Select Features**: Choose from organized categories:
   - Telemetry & Reporting
   - Privacy & Security
   - Brave Features
   - Performance & Bloat

3. **Bulk Selection**: Use "Select All" checkbox for quick configuration

4. **DNS Configuration**: Choose DNS over HTTPS mode from dropdown

5. **Apply Changes**: Click "Apply Settings" to write configuration to Brave

6. **Export/Import**: Save your configuration or load previously saved settings

### Configuration Storage

Settings are stored in `/Library/Managed Preferences/com.brave.Browser.plist` using macOS defaults system.

## Important Notes

- **Restart Required**: Restart Brave Browser after applying changes
- **Administrator Access**: Sudo privileges required to modify browser policies
- **Backup Recommended**: Consider exporting current settings before major changes
- **Reset Option**: "Reset All" button removes all custom policies and restores defaults

## Safety

- All changes use official Brave/Chromium policy keys
- Settings can be easily reverted using the "Reset All" function
- Export/import functionality allows for configuration backup and restoration
- No modification of Brave application files - only policy preferences

## Troubleshooting

- **Permission Denied**: Ensure you're running with `sudo python3 bebrave_macos.py`
- **Changes Not Applied**: Restart Brave Browser completely
- **Restore Defaults**: Use "Reset All" button or manually delete the plist file

## Copyright Notice

**Brave**, **Brave Browser**, and the **Brave lion head logo** are trademarks and copyrights of Brave Software, Inc. This project is an independent, unofficial tool and is not affiliated with, endorsed by, or sponsored by Brave Software, Inc.

This tool interacts with Brave Browser through official policy mechanisms and does not modify the browser application itself.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

This project is provided as-is for educational and privacy configuration purposes.