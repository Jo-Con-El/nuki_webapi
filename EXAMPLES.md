# Advanced Usage Examples - Nuki Web API

## Automations

### 1. Auto-lock at night

```yaml
automation:
  - alias: "Lock door at 11 PM"
    trigger:
      - platform: time
        at: "23:00:00"
    condition:
      - condition: state
        entity_id: lock.nuki_lock_12345678
        state: "unlocked"
    action:
      - service: lock.lock
        target:
          entity_id: lock.nuki_lock_12345678
      - service: notify.mobile_app_iphone
        data:
          title: "🔒 Security"
          message: "Door locked automatically"
```

### 2. Unlock when arriving home (with confirmation)

```yaml
automation:
  - alias: "Unlock on arrival"
    trigger:
      - platform: zone
        entity_id: person.john
        zone: zone.home
        event: enter
    action:
      - service: notify.mobile_app_iphone
        data:
          title: "🏠 Welcome home"
          message: "Unlock the door?"
          data:
            actions:
              - action: "UNLOCK_DOOR"
                title: "Unlock"
              - action: "DISMISS"
                title: "No"

  - alias: "Unlock confirmation"
    trigger:
      - platform: event
        event_type: mobile_app_notification_action
        event_data:
          action: UNLOCK_DOOR
    action:
      - service: lock.unlock
        target:
          entity_id: lock.nuki_lock_12345678
```

### 3. Alert if door left unlocked for 5 minutes

```yaml
automation:
  - alias: "Alert unlocked door"
    trigger:
      - platform: state
        entity_id: lock.nuki_lock_12345678
        to: "unlocked"
        for:
          minutes: 5
    action:
      - service: notify.mobile_app_iphone
        data:
          title: "⚠️ Security"
          message: "Door has been unlocked for 5 minutes"
          data:
            actions:
              - action: "LOCK_NOW"
                title: "Lock now"

  - alias: "Lock from notification"
    trigger:
      - platform: event
        event_type: mobile_app_notification_action
        event_data:
          action: LOCK_NOW
    action:
      - service: lock.lock
        target:
          entity_id: lock.nuki_lock_12345678
```

### 4. Open door when Ring detects known person (using Lock'n'Go)

```yaml
automation:
  - alias: "Open for known visitor"
    trigger:
      - platform: state
        entity_id: binary_sensor.ring_front_person_detected
        to: "on"
    condition:
      - condition: state
        entity_id: input_boolean.auto_unlock_visitors
        state: "on"
    action:
      - service: nuki_webapi.lock_n_go
        target:
          entity_id: lock.nuki_lock_12345678
        data:
          unlatch: true  # Fully opens the door
      - service: notify.mobile_app
        data:
          message: "Door opened for visitor"
```

### 5. Lock when everyone leaves

```yaml
automation:
  - alias: "Lock when everyone leaves"
    trigger:
      - platform: state
        entity_id: group.all_persons
        to: "not_home"
    condition:
      - condition: state
        entity_id: lock.nuki_lock_12345678
        state: "unlocked"
    action:
      - service: lock.lock
        target:
          entity_id: lock.nuki_lock_12345678
```

### 6. Delivery person access with Lock'n'Go

```yaml
automation:
  - alias: "Allow delivery person with code"
    trigger:
      - platform: state
        entity_id: input_text.delivery_code
        to: "1234"
    action:
      - service: nuki_webapi.lock_n_go
        target:
          entity_id: lock.nuki_lock_12345678
        data:
          unlatch: false
      - service: notify.mobile_app
        data:
          title: "📦 Delivery Access"
          message: "Door unlocked for delivery person. Will auto-lock."
      - delay:
          seconds: 2
      - service: input_text.set_value
        target:
          entity_id: input_text.delivery_code
        data:
          value: ""
```

### 7. Low battery alert

```yaml
automation:
  - alias: "Nuki low battery alert"
    trigger:
      - platform: state
        entity_id: lock.nuki_lock_12345678
        attribute: battery_critical
        to: true
    action:
      - service: notify.all_devices
        data:
          title: "🔋 Low Battery"
          message: "Nuki lock battery is critical. Replace soon."
```

## Scripts

### Party Mode Script (disable auto-lock)

```yaml
script:
  party_mode:
    alias: "Party Mode"
    sequence:
      - service: input_boolean.turn_on
        target:
          entity_id: input_boolean.party_mode
      - service: lock.unlock
        target:
          entity_id: lock.nuki_lock_12345678
      - service: notify.mobile_app
        data:
          message: "Party mode activated - Auto-lock disabled"

  party_mode_off:
    alias: "Disable Party Mode"
    sequence:
      - service: input_boolean.turn_off
        target:
          entity_id: input_boolean.party_mode
      - service: lock.lock
        target:
          entity_id: lock.nuki_lock_12345678
      - service: notify.mobile_app
        data:
          message: "Party mode disabled - Auto-lock restored"
```

### Vacation Mode Script

```yaml
script:
  vacation_mode:
    alias: "Vacation Mode"
    sequence:
      - service: lock.lock
        target:
          entity_id: lock.nuki_lock_12345678
      - service: automation.turn_off
        target:
          entity_id:
            - automation.unlock_on_arrival
            - automation.open_for_known_visitor
      - service: notify.mobile_app
        data:
          message: "🏖️ Vacation mode activated - Home secured"
```

## Lovelace Dashboards

### Simple Card

```yaml
type: entities
title: Access Control
entities:
  - entity: lock.nuki_lock_12345678
    name: Front Door
    secondary_info: last-changed
```

### Detailed Information Card

```yaml
type: vertical-stack
cards:
  - type: entities
    title: Nuki Lock
    entities:
      - entity: lock.nuki_lock_12345678
        name: Front Door
      - type: attribute
        entity: lock.nuki_lock_12345678
        attribute: nuki_state_name
        name: Nuki State
      - type: attribute
        entity: lock.nuki_lock_12345678
        attribute: battery_critical
        name: Battery Critical
        
  - type: glance
    entities:
      - entity: lock.nuki_lock_12345678
        name: Status
```

### Action Buttons Card

```yaml
type: custom:mushroom-lock-card
entity: lock.nuki_lock_12345678
name: Front Door
icon: mdi:door
tap_action:
  action: more-info
hold_action:
  action: toggle
double_tap_action:
  action: call-service
  service: lock.open
  service_data:
    entity_id: lock.nuki_lock_12345678
```

### Complete Control Panel

```yaml
type: vertical-stack
cards:
  - type: markdown
    content: |
      # 🔐 Access Control

  - type: horizontal-stack
    cards:
      - type: button
        entity: lock.nuki_lock_12345678
        name: Lock
        icon: mdi:lock
        tap_action:
          action: call-service
          service: lock.lock
          service_data:
            entity_id: lock.nuki_lock_12345678

      - type: button
        entity: lock.nuki_lock_12345678
        name: Unlock
        icon: mdi:lock-open
        tap_action:
          action: call-service
          service: lock.unlock
          service_data:
            entity_id: lock.nuki_lock_12345678

      - type: button
        entity: lock.nuki_lock_12345678
        name: Open
        icon: mdi:door-open
        tap_action:
          action: call-service
          service: lock.open
          service_data:
            entity_id: lock.nuki_lock_12345678

  - type: horizontal-stack
    cards:
      - type: button
        entity: lock.nuki_lock_12345678
        name: Lock'n'Go
        icon: mdi:lock-clock
        tap_action:
          action: call-service
          service: nuki_webapi.lock_n_go
          service_data:
            entity_id: lock.nuki_lock_12345678
            unlatch: false

      - type: button
        entity: lock.nuki_lock_12345678
        name: Lock'n'Go + Unlatch
        icon: mdi:door-open
        tap_action:
          action: call-service
          service: nuki_webapi.lock_n_go
          service_data:
            entity_id: lock.nuki_lock_12345678
            unlatch: true

  - type: entities
    entities:
      - entity: lock.nuki_lock_12345678
        secondary_info: last-changed
```

## Useful Helpers

### Input Boolean for Party Mode

```yaml
input_boolean:
  party_mode:
    name: Party Mode
    icon: mdi:party-popper
```

### Input Boolean for Auto-unlock

```yaml
input_boolean:
  auto_unlock_on_arrival:
    name: Auto-unlock on arrival
    icon: mdi:home-import-outline
```

### Timer for Auto-lock

```yaml
timer:
  lock_delay:
    name: Auto-lock Timer
    duration: "00:05:00"
    icon: mdi:timer-lock
```

## Advanced Notifications

### With camera snapshot on unlock

```yaml
automation:
  - alias: "Photo on unlock"
    trigger:
      - platform: state
        entity_id: lock.nuki_lock_12345678
        to: "unlocked"
    action:
      - service: camera.snapshot
        target:
          entity_id: camera.front_door
        data:
          filename: /config/www/snapshots/door_unlock_{{ now().strftime('%Y%m%d_%H%M%S') }}.jpg
      - delay:
          seconds: 2
      - service: notify.mobile_app
        data:
          title: "🔓 Door Unlocked"
          message: "{{ now().strftime('%H:%M:%S') }}"
          data:
            image: "/local/snapshots/door_unlock_{{ now().strftime('%Y%m%d_%H%M%S') }}.jpg"
```

## Alexa Integration

```yaml
# Add to configuration.yaml
alexa:
  smart_home:
    filter:
      include_entities:
        - lock.nuki_lock_12345678
    entity_config:
      lock.nuki_lock_12345678:
        name: "Front door"
        description: "Nuki lock at the entrance"
```

Now you can say:
- "Alexa, lock the front door"
- "Alexa, unlock the front door"
- "Alexa, is the front door locked?"

## Google Home Integration

```yaml
# Add to configuration.yaml
google_assistant:
  project_id: your-project-id
  service_account: !include SERVICE_ACCOUNT.JSON
  report_state: true
  exposed_domains:
    - lock
  entity_config:
    lock.nuki_lock_12345678:
      name: "Front door"
      room: "Entrance"
```

## Security Tips

1. **Use confirmations:** Whenever possible, use notifications with action buttons instead of direct automations
2. **Multiple conditions:** Add multiple conditions to unlock automations
3. **Logs:** Create automations to log all state changes
4. **Token backup:** Store your API token securely
5. **Notifications:** Set up notifications for all important events
