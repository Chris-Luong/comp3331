# States/Statuses
ERROR = -1
ACTIVE_USER = 0
INACTIVE_USER = 1
BLOCKED_USER = 2

# Messages sent from server
# Ends with terminator '\0' as sometimes, multiple messages are recevied as 1 in clieny
S_USERNAME_REQUEST = "Username: \0"
S_PASSWORD_REQUEST = "Password: \0"
S_USERNAME_ERROR_MESSAGE = "Invalid username!\0"
S_PASSWORD_ERROR_MESSAGE = "Invalid password!\0"
S_LOGGED_IN_USER_MESSAGE = "User logged in successfully!\0"
S_WELCOME_MESSAGE = "Welcome to TOOM!\0"

S_INVALID_ATTEMPT_NUMBER_MESSAGE = "Invalid number of allowed failed consecutive attempt: \0"
S_FIRST_BLOCKED_USER_MESSAGE = "Invalid password. Your account has been blocked. Please try again later\0"
S_BLOCKED_USER_MESSAGE = "Your account has been blocked due to multiple login failures. Please try again later\0"
S_COMMAND_INSTRUCTIONS = "Enter one of the following commands (BCM, ATU, SRB, SRM, RDM, OUT, UPD): \0"

# Messages for client
USERNAME_REQUEST = "Username: "
PASSWORD_REQUEST = "Password: "
USERNAME_ERROR_MESSAGE = "Invalid username!"
PASSWORD_ERROR_MESSAGE = "Invalid password!"
LOGGED_IN_USER_MESSAGE = "User logged in successfully!"
WELCOME_MESSAGE = "Welcome to TOOM!"

INVALID_ATTEMPT_NUMBER_MESSAGE = "Invalid number of allowed failed consecutive attempt: "
FIRST_BLOCKED_USER_MESSAGE = "Invalid password. Your account has been blocked. Please try again later"
BLOCKED_USER_MESSAGE = "Your account has been blocked due to multiple login failures. Please try again later"
COMMAND_INSTRUCTIONS = "Enter one of the following commands (BCM, ATU, SRB, SRM, RDM, OUT, UPD): "

SERVER_SHUTDOWN = "Orderly shutdown on server end"