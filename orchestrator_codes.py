# -------------------------------------------------------------
# Protocol for asking the Orchestrator to do the following:
# - Startup a virtual runtime for a UNIQUE USER/CLIENT ID
#   this should also LOAD CLIENT ID stored modules (cached and)
#   pesisted via DB/other persistence mechanism through web
# - Check if a virtual runtime is running for a CLIENT ID
# - Stop a virtual runtime for a CLIENT ID
# - add a module by NAME to a virtual runtime for a CLIENT ID
# - execute a module by MODULE ID on a virtual runtime for a CLIENT ID
# - delete a module by MODULE ID on a virtual runtime for a CLIENT ID
# - list all modules by NAME and MODULE ID on a virtual runtime for a CLIENT ID
# -------------------------------------------------------------