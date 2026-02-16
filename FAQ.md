# Frequently Asked Questions (FAQ)

## Installation & Configuration

### Do I need a Nuki Bridge?

Not necessarily. This integration works with:
- ✅ Nuki Pro/Go/Ultra locks (have built-in Wi-Fi)
- ✅ Older Nuki locks WITH Nuki Bridge
- ❌ Older Nuki locks WITHOUT Nuki Bridge or Internet connection

### How do I get the API token?

1. Go to [web.nuki.io](https://web.nuki.io)
2. Sign in
3. MENU > API
4. "Generate new token"
5. Copy the token (shown only once)

### Does the token expire?

No, Nuki API tokens don't expire automatically. However:
- You can manually revoke it from Nuki Web
- If you change your account password, you may need to generate a new one
- It's recommended to regenerate periodically for security

### Can I have multiple integrations?

Yes, but usually not necessary. One integration can handle all your Nuki locks. You'd only need multiple integrations if you have separate Nuki accounts.

## Functionality

### What actions can I perform?

- ✅ Lock
- ✅ Unlock
- ✅ Open/Unlatch (fully opens the door)
- ⚠️  Lock'n'Go (available in code, not exposed as service by default)

### What sensors are available?

- 🔒 **Lock entity**: Shows lock state (locked/unlocked/locking/unlocking)
- 🔋 **Battery sensor**: Shows battery percentage (0-100%)
  - Includes `battery_critical` and `battery_charging` attributes
  - Works with all Nuki lock models
  - Newer models (Pro/Go/Ultra) show exact percentage
  - Older models show estimated percentage based on critical flag

### Are states real-time?

Not exactly, but much faster than before. The integration works in two ways:

1. **Regular polling**: Updates every 30 seconds automatically
2. **Action-triggered updates**: When you lock/unlock/open:
   - Immediate refresh (0s) - UI responds instantly
   - Delayed refresh (3s) - Captures the final lock state

This means after performing an action, you'll see the state update within 3-4 seconds instead of waiting up to 30 seconds.

For true real-time updates you'd need webhooks (Advanced Nuki API).

### Can I change the update frequency?

Yes, edit the `__init__.py` file:

```python
SCAN_INTERVAL = timedelta(seconds=30)  # Change 30 to your value
```

⚠️  Very low values (less than 10 seconds) can cause:
- Higher battery drain on the lock
- Possible API rate limiting

### Does it work without Internet?

No. This integration requires:
- Home Assistant with Internet access
- Nuki lock connected to Internet
- Nuki API available

If your Internet goes down, the integration stops working. For local control you'd need the Bridge with local HTTP API.

## Common Errors

### Error: "No active Smart Hosting subscription"

Some API actions require **Nuki Smart Hosting** (Nuki's paid service).

**Solution:**
1. Go to web.nuki.io
2. Activate Nuki Smart Hosting in your account
3. It's a monthly subscription service from Nuki

**Alternative:**
- Use the Nuki Bridge with its local HTTP API (doesn't require subscription)

### Error: "Invalid API token"

**Common causes:**
- Token copied incorrectly (extra spaces, missing characters)
- Token revoked in Nuki Web
- Wrong Nuki account

**Solution:**
1. Generate a new token
2. Copy the entire token exactly
3. Remove the integration in HA
4. Re-add it with the new token

### Error: "No smartlocks found"

**Causes:**
- Lock not linked to Nuki Web
- Lock doesn't have Internet connection

**Solution:**
1. Open the Nuki app
2. Go to lock settings
3. "Features & Configuration"
4. "Activate Nuki Web"
5. Follow the activation process
6. Verify in web.nuki.io that the lock appears

### Lock doesn't respond to commands

**Checks:**
1. Does the lock have battery?
2. Is the lock connected to Internet? (check in app)
3. Do you have Smart Hosting active?
4. Do commands work from web.nuki.io?

### State shows "unknown" or "unavailable"

**Causes:**
- Lock connection lost
- Nuki API down
- Temporary communication error

**Solution:**
- Wait a few minutes
- Verify lock connection
- Restart integration if it persists

### Why does my battery sensor show an estimate instead of exact percentage?

The battery sensor behavior depends on your Nuki lock model:

**Newer models (Pro/Go/Ultra with Wi-Fi):**
- Report exact battery percentage via `batteryChargeState`
- Shows accurate 0-100% reading
- Updates with each polling cycle

**Older models (1.0/2.0 with Bridge):**
- Only report `batteryCritical` boolean (true/false)
- Integration estimates percentage:
  - If critical: ~15%
  - If not critical: ~80%
- This is a limitation of the Nuki API for older models

**All models provide:**
- `battery_critical` attribute (boolean)
- `battery_charging` attribute (for rechargeable battery models)

### My battery sensor shows 80% but I just changed batteries

This is normal for older Nuki models. Since they only report "critical" or "not critical," the integration estimates 80% when not critical. The percentage will update to ~15% only when the battery becomes actually critical.

If you want to track battery changes more precisely, consider upgrading to a newer Nuki model (Pro/Go/Ultra) which reports exact percentages.

## Security

### Is it safe to use this integration?

Yes, but keep in mind:

✅ **Safe:**
- Uses HTTPS for API communication
- Token stored encrypted in HA
- No direct communication with lock (goes through Nuki servers)

⚠️  **Considerations:**
- Token gives FULL access to your locks
- Depends on Nuki servers (if they're down, it doesn't work)
- Requires Internet (additional point of failure)

### What if someone gets my token?

If someone gets your token they can:
- Lock/unlock your locks
- See your lock states
- Manage configurations

**If you think your token is compromised:**
1. Go to web.nuki.io
2. MENU > API
3. Revoke the compromised token
4. Generate a new one
5. Update the configuration in HA

### Can I log who locked/unlocked?

Home Assistant logs state changes, but the Nuki API doesn't provide information about who performed the action at the basic level. For that you'd need:
- Webhooks (Advanced API)
- Review Nuki Web logs directly

**You can create a log with automations:**

```yaml
automation:
  - alias: "Log lock changes"
    trigger:
      - platform: state
        entity_id: lock.nuki_lock_12345678
    action:
      - service: logbook.log
        data:
          name: "Nuki Lock"
          message: "State changed from {{ trigger.from_state.state }} to {{ trigger.to_state.state }}"
```

## Performance

### Does it drain lock battery?

Battery consumption depends on:
- Update frequency (30 seconds by default)
- Number of actions performed
- Wi-Fi/Bridge connection quality

**State update strategy:**
- Regular polling: Every 30 seconds
- After actions: Immediate + 3 second delayed refresh
- The delayed refresh doesn't significantly impact battery life

**Compared to local Bridge:** May consume slightly more battery because the lock must maintain Wi-Fi or Bluetooth connection with Bridge that then connects to Internet.

### Why does the state update twice after an action?

This is intentional for better user experience:

1. **Immediate refresh (0 s)**:
   - Shows intermediate states like "locking" or "unlocking"
   - UI responds instantly
   - User knows the action was received

2. **Delayed refresh (3 s)**:
   - Captures the final state ("locked" or "unlocked")
   - Nuki locks take 1-3 seconds to complete physical actions
   - Ensures accurate final state display

This double-refresh strategy provides the best balance between responsiveness and accuracy.

### Are there API limits?

Nuki doesn't publish exact limits, but:
- Don't poll faster than every 10 seconds
- Don't make hundreds of calls per minute
- Normal usage (30 second polling) is fine

If you experience 429 errors (Too Many Requests):
- Increase update interval
- Reduce number of automations making calls

## Compatibility

### Does it work with Home Assistant OS?
✅ Yes

### Does it work with Home Assistant Supervised?
✅ Yes

### Does it work with Home Assistant Container?
✅ Yes

### Does it work with Home Assistant Core?
✅ Yes

### What's the minimum HA version needed?
Home Assistant 2023.7.0 or higher (for modern config_flow support)

### Does it work with all Nuki models?

✅ Nuki Smart Lock 1.0 (with Bridge) - Estimated battery %
✅ Nuki Smart Lock 2.0 (with Bridge) - Estimated battery %
✅ Nuki Smart Lock 3.0 Pro (built-in Wi-Fi) - Exact battery %
✅ Nuki Smart Lock 4.0 Pro (built-in Wi-Fi) - Exact battery %
✅ Nuki Smart Lock Go (built-in Wi-Fi) - Exact battery %
✅ Nuki Smart Lock Ultra (built-in Wi-Fi) - Exact battery %
⚠️  Nuki Opener (not tested, should work) - Battery status varies

## Comparison with Other Integrations

### What's the difference with the official Nuki integration?

**Official Integration (core):**
- ✅ Requires Bridge
- ✅ Local control (faster - instant updates)
- ✅ Doesn't require subscription
- ✅ Webhooks support (real-time)
- ❌ Doesn't work without Bridge
- ❌ Doesn't work if Bridge loses connection

**This integration (Web API):**
- ✅ Doesn't require Bridge (on Pro/Go/Ultra models)
- ✅ Works from anywhere with Internet
- ✅ Fast state updates (immediate + 3s delayed)
- ✅ Battery percentage sensor
- ❌ Requires Smart Hosting (paid)
- ❌ Polling-based (30s + action-triggered updates)
- ❌ Depends on Internet

### Can I use both integrations?

Technically yes, but generally not recommended because:
- You can have conflicts
- You'll duplicate entities
- Can be confusing

Better use one or the other based on your needs.
