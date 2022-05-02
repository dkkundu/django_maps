"""project_name > juzzmin.py

https://django-jazzmin.readthedocs.io/configuration/
"""

CONFIG = {  # -----------------------------------------------------------------

    # title of the window
    "site_title": "TPL Django",
    # Title on the brand, and the login screen (19 chars max)
    "site_header": "TPL Django",
    # square logo to use for your site
    "site_logo": "tigerpark/logo.png",
    # Welcome text on the login screen
    "welcome_sign": "Welcome to TPL Django",
    # Copyright on the footer
    "copyright": "Tiger Park Limited",
    # The model admin to search from the search bar
    "search_model": "Core.user",
    # Field name on user model that contains avatar image
    "user_avatar": None,

    # Top Menu # --------------------------------------------------------------

    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {
            "name": "Home",
            "url": "admin:index",
            "permissions": ["Core.view_user"]
        },
        # external url that opens in a new window (Permissions can be added)
        {
            "name": "Demo",
            "url": "https://tpl-django.tiger-park.com/",
            "new_window": True
        },
        # model admin to link to (Permissions checked against model)
        {
            "model": "Core.user"
        },
        # App with dropdown menu to all its models pages
        # (Permissions checked against models)
        {
            "app": "Core"
        },
    ],

    # User Menu # -------------------------------------------------------------

    # Additional links to include in the user menu on the top right
    "usermenu_links": [
        {
            "model": "Core.user"
        }
    ],

    # Side Menu # -------------------------------------------------------------

    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": True,
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    # List of apps (and/or models) to base side menu ordering off of
    # (does not need to contain all apps/models)
    "order_with_respect_to": [],
    # Custom links to append to app groups, keyed on app name
    "custom_links": {},

    # Custom icons  https://fontawesome.com/icons?d=gallery&m=free
    # for a list of icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    # Related Modal # ---------------------------------------------------------
    # Use modals instead of popups
    "related_modal_active": False,

    # UI Tweaks # -------------------------------------------------------------
    # Relative paths to custom CSS/JS scripts(must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,

    # Change view # -----------------------------------------------------------
    # Render out the change view as a single form, or in tabs,
    # current options are:
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "Core.user": "collapsible", "auth.group": "vertical_tabs"
    },
    # Add a language dropdown into the admin
    "language_chooser": False,
}
