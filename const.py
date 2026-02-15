"""Constants for the Nuki Web API integration."""

DOMAIN = "nuki_webapi"

# API Constants
API_BASE_URL = "https://api.nuki.io"
API_TIMEOUT = 10

# Smart Lock Actions
ACTION_UNLOCK = 1
ACTION_LOCK = 2
ACTION_UNLATCH = 3
ACTION_LOCK_N_GO = 4
ACTION_LOCK_N_GO_UNLATCH = 5

# Smart Lock States
STATE_UNCALIBRATED = 0
STATE_LOCKED = 1
STATE_UNLOCKING = 2
STATE_UNLOCKED = 3
STATE_LOCKING = 4
STATE_UNLATCHED = 5
STATE_UNLOCKED_LOCK_N_GO = 6
STATE_UNLATCHING = 7
STATE_MOTOR_BLOCKED = 254
STATE_UNDEFINED = 255

# Mapping of Nuki states to Home Assistant states
NUKI_STATES_MAP = {
    STATE_UNCALIBRATED: "locked",
    STATE_LOCKED: "locked",
    STATE_UNLOCKING: "unlocking",
    STATE_UNLOCKED: "unlocked",
    STATE_LOCKING: "locking",
    STATE_UNLATCHED: "unlocked",
    STATE_UNLOCKED_LOCK_N_GO: "unlocked",
    STATE_UNLATCHING: "unlocking",
    STATE_MOTOR_BLOCKED: "jammed",
    STATE_UNDEFINED: "unknown",
}
