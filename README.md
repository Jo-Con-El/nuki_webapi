# Nuki Web API for Home Assistant

Custom integration to control Nuki Smart Locks via the Nuki Web API (no Bridge or Matter required).

## Features

✅ Control Nuki locks via Web API  
✅ Support for multiple locks  
✅ Real-time status (locked/unlocked)  
✅ Actions: lock, unlock, open (unlatch)  
✅ Battery critical information  
✅ UI-based configuration  

## Requirements

1. A Nuki Smart Lock connected to the Internet (via built-in Wi-Fi in Pro/Go/Ultra models or via Nuki Bridge)
2. Active Nuki Web account
3. Nuki Web API Token

## Getting the API Token

1. Go to [Nuki Web](https://web.nuki.io)
2. Sign in with your account
3. Go to **MENU > API**
4. In the "API Token" section, click **"Generate new token"**
5. Copy the generated token (it's only shown once, so save it securely)

## Installation

### Option 1: HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three-dot menu (⋮) and select "Custom repositories"
4. Add this repository URL and select category "Integration"
5. Search for "Nuki Web API" and install
6. Restart Home Assistant

### Option 2: Manual

1. Download this `nuki_webapi` folder
2. Copy the entire folder to `custom_components/nuki_webapi` in your Home Assistant installation
3. The structure should look like this:
   ```
   custom_components/
   └── nuki_webapi/
       ├── __init__.py
       ├── api.py
       ├── config_flow.py
       ├── const.py
       ├── lock.py
       ├── manifest.json
       ├── strings.json
       └── translations/
           └── en.json
   ```
4. Restart Home Assistant

## Configuration

1. Go to **Settings > Devices & Services**
2. Click **+ ADD INTEGRATION**
3. Search for **"Nuki Web API"**
4. Enter your API token
5. Click **SUBMIT**

The integration will automatically detect all locks associated with your account.

## Usage

### Created Entities

For each lock, an entity `lock.nuki_lock_XXXXXX` will be created with:

**States:**
- `locked` - Locked
- `unlocked` - Unlocked
- `unlocking` - Unlocking
- `locking` - Locking
- `jammed` - Jammed

**Attributes:**
- `battery_critical` - Indicates if battery is critical
- `nuki_state` - Numeric Nuki state code
- `nuki_state_name` - Nuki state name

### Available Services

```yaml
# Lock
service: lock.lock
target:
  entity_id: lock.nuki_lock_12345678

# Unlock
service: lock.unlock
target:
  entity_id: lock.nuki_lock_12345678

# Open (unlatch) - fully opens the door
service: lock.open
target:
  entity_id: lock.nuki_lock_12345678
```

### Automation Example

```yaml
automation:
  - alias: "Unlock door when arriving home"
    trigger:
      - platform: zone
        entity_id: person.user
        zone: zone.home
        event: enter
    action:
      - service: lock.unlock
        target:
          entity_id: lock.nuki_lock_12345678
      - service: notify.mobile_app
        data:
          message: "Door unlocked automatically"
```

### Lovelace Card

```yaml
type: entities
entities:
  - entity: lock.nuki_lock_12345678
    name: Front Door
    secondary_info: last-changed
```

Or using a custom card:

```yaml
type: custom:mushroom-lock-card
entity: lock.nuki_lock_12345678
name: Front Door
fill_container: false
```

## Limitations

- **Polling:** The integration updates state every 30 seconds. It's not real-time (for real-time you'd need webhooks or the advanced API)
- **Battery:** Only reports if battery is critical, not the exact percentage
- **Advanced actions:** Lock'n'Go is available in code but not exposed as a service (can be added)

## Troubleshooting

### Error: "Invalid API token"
- Verify the token is copied correctly
- Make sure the token hasn't expired
- Generate a new token from Nuki Web

### Error: "No smartlocks found"
- Verify your lock is connected to Nuki Web
- In the Nuki app, go to lock settings > "Features & Configuration" > "Activate Nuki Web"

### Lock doesn't respond
- Verify the lock has Internet connection
- Check Home Assistant logs: `Settings > System > Logs`
- Check the lock's battery status

### States don't update
- Updates occur every 30 seconds by default
- If you need faster updates, edit `SCAN_INTERVAL` in `__init__.py`

## Important Notes

⚠️ **Smart Hosting Requirement**: Some API actions (especially lock/unlock) require an active **Nuki Smart Hosting** subscription. If you get errors about "No active Smart Hosting subscription", you'll need to activate this service in your Nuki account.

⚠️ **Security**: The API token provides full access to your locks. Store it securely and don't share it.

## Credits

Based on the [official Nuki Web API documentation](https://developer.nuki.io/)

## License

MIT License
