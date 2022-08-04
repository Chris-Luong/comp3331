# States/Statuses
ERROR = -1 #FIXME: may not need this
ACTIVE_USER = 0
INACTIVE_USER = 1
BLOCKED_USER = 2

# Messages for authentication
USERNAME_REQUEST = "Username: "
PASSWORD_REQUEST = "Password: "
USERNAME_ERROR_MESSAGE = "Invalid username!"
PASSWORD_ERROR_MESSAGE = "Invalid password!"
LOGGED_IN_USER_MESSAGE = "User logged in successfully!"
WELCOME_MESSAGE = "Welcome to TOOM!"

# Messages for command instructions/errors
INVALID_ATTEMPT_NUMBER_MESSAGE = "Invalid number of allowed failed consecutive attempt: "
FIRST_BLOCKED_USER_MESSAGE = "Invalid password. Your account has been blocked. Please try again later"
BLOCKED_USER_MESSAGE = "Your account has been blocked due to multiple login failures. Please try again later"
COMMAND_INSTRUCTIONS = "Enter one of the following commands (BCM, ATU, SRB, SRM, RDM, OUT, UPD): "

# Mesages for commands
ATU_STATUS_ALONE = "No other active user"

# Miscellaneous messages
SERVER_SHUTDOWN = "Orderly shutdown on server end"