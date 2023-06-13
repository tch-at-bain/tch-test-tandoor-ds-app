import os

# Used for forming an absolute URL to your redirect URI.
# The absolute URL must match the redirect URI you set
# in the app's registration in the Azure portal.
REDIRECT_PATH = "/retrieveToken"

# Route path that the dash app will be served from
DASH_ROUTE_PATHNAME = "/home/"

# You can find more Microsoft Graph API endpoints from Graph Explorer
# https://developer.microsoft.com/en-us/graph/graph-explorer
ENDPOINT = (
    "https://graph.microsoft.com/v1.0/users"  # This resource requires no admin consent
)

# You can find the proper permission names from this document
# https://docs.microsoft.com/en-us/graph/permissions-reference
SCOPE = ["User.Read"]

SESSION_TYPE = (
    "filesystem"  # Specifies the token cache should be stored in server-side session
)
