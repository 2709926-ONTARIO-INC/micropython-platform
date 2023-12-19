freeze("$(PORT_DIR)/modules")
freeze("modules")
include("$(MPY_DIR)/extmod/asyncio")

# Useful networking-related packages.
require("bundle-networking")

# Require some micropython-lib modules.
require("base64")
require("umqtt.robust")
require("umqtt.simple")
require("logging")
require("__future__")
require("inspect")
require("functools")

