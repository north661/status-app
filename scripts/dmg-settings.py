import os

app = defines.get("app", "/tmp/Status.app")

files = [app]
symlinks = {"Applications": "/Applications"}

format = "UDZO"
compression_level = 9

icon_size = 220
text_size = 13

window_rect = ((200, 120), (900, 500))

default_view = "icon-view"
show_status_bar = False
show_tab_view = False
show_toolbar = False
show_pathbar = False
show_sidebar = False

background = os.path.join(os.getcwd(), "resources", "dmg-background-status.png")
icon = os.path.join(os.getcwd(), "status.icns")
badge_icon = icon

icon_locations = {
    "Status.app": (225, 238),
    "Applications": (676, 240),
}

hide_extensions = ["Status.app"]
