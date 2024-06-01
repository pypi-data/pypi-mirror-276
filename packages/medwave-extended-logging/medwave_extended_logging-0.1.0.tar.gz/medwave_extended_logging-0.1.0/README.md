# Logging package

This package contains the logging utilities.

### Known issues

Loggers do not always exit quietly (ie sometimes there remains task that is supposed to stop logger yet it never quits). This should not be production issue thus loggers on production should never reach their timeout.
