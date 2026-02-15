# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-13

### Added
- ✨ Initial Nuki Web API integration for Home Assistant
- 🔐 Support for API Token authentication
- 🚪 Lock entity with complete states
- 🔓 Action: Unlock
- 🔒 Action: Lock
- 🚪 Action: Open/Unlatch
- 🔋 Critical battery detection
- 🌐 UI-based configuration (Config Flow)
- 🌍 Multi-language support (EN/ES)
- 📊 Automatic state updates (polling every 30s)
- 🔄 DataUpdateCoordinator for efficient update handling
- 📱 Support for multiple locks in one account
- 📝 Complete documentation (README, EXAMPLES, FAQ)
- 🛠️ Automatic installation script
- 🎨 Additional attributes (Nuki state, state name)
- ⚙️ Detailed device information

### Supported States
- `locked` - Locked
- `unlocked` - Unlocked
- `unlocking` - Unlocking
- `locking` - Locking
- `unlatched` - Opened
- `jammed` - Jammed
- `unknown` - Unknown

### Supported Platforms
- Home Assistant OS
- Home Assistant Supervised
- Home Assistant Container
- Home Assistant Core

### Supported Lock Models
- Nuki Smart Lock 1.0 (with Bridge)
- Nuki Smart Lock 2.0 (with Bridge)
- Nuki Smart Lock 3.0 Pro
- Nuki Smart Lock 4.0 Pro
- Nuki Smart Lock Go
- Nuki Smart Lock Ultra

### Known Limitations
- Polling every 30 seconds (not real-time)
- Requires Nuki Smart Hosting subscription for some actions
- No webhook support (requires Advanced API)
- Battery percentage not available (only critical/not critical)
