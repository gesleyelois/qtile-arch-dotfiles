from __future__ import annotations

import json
import os
from collections.abc import Iterable

from libqtile import pangocffi
from libqtile.command.base import expose_command
from libqtile.layout.base import Layout
from libqtile.layout.tree import Root, Section, TreeTab, Window


APP_RULES: tuple[tuple[tuple[str, ...], str, str], ...] = (
    (("warp",), "", "Warp"),
    (("alacritty", "kitty", "wezterm", "terminal"), "", "Terminal"),
    (("firefox",), "", "Firefox"),
    (("vivaldi",), "", "Vivaldi"),
    (("brave",), "", "Brave"),
    (("chromium",), "", "Chromium"),
    (("chrome",), "", "Chrome"),
    (("code-oss",), "", "Code OSS"),
    (("visual studio code", "code"), "", "VS Code"),
    (("cursor",), "", "Cursor"),
    (("intellij", "idea"), "", "IntelliJ"),
    (("pycharm",), "", "PyCharm"),
    (("webstorm",), "", "WebStorm"),
    (("jetbrains",), "", "JetBrains"),
    (("discord",), "", "Discord"),
    (("slack",), "", "Slack"),
    (("spotify",), "", "Spotify"),
    (("obsidian",), "󰠮", "Obsidian"),
    (("postman",), "󰛮", "Postman"),
    (("insomnia",), "󰛮", "Insomnia"),
    (("thunar",), "", "Thunar"),
    (("nautilus",), "", "Files"),
    (("dolphin",), "", "Dolphin"),
    (("file",), "", "Files"),
)

DEFAULT_APP_ICON = "󰣆"
DEFAULT_APP_LABEL = "App"
STATE_FILE = os.path.expanduser("~/.local/state/qtile-arch-dotfiles/treetab_state.json")
MIN_PANEL_WIDTH = 50


def _as_text_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, Iterable):
        return [str(item) for item in value if item]
    return [str(value)]


def _window_terms(window) -> list[str]:
    terms: list[str] = []

    for method_name in ("get_wm_class", "get_wm_window_role"):
        method = getattr(window, method_name, None)
        if callable(method):
            try:
                terms.extend(_as_text_list(method()))
            except Exception:
                pass

    for attr_name in ("wm_class", "window_class", "name", "title"):
        terms.extend(_as_text_list(getattr(window, attr_name, None)))

    return [term.lower() for term in terms if term]


def _window_classes(window) -> list[str]:
    terms: list[str] = []

    method = getattr(window, "get_wm_class", None)
    if callable(method):
        try:
            terms.extend(_as_text_list(method()))
        except Exception:
            pass

    for attr_name in ("wm_class", "window_class"):
        terms.extend(_as_text_list(getattr(window, attr_name, None)))

    return [term for term in terms if term]


def _fallback_label(window) -> str:
    terms = _window_classes(window) or _as_text_list(getattr(window, "name", None))
    if not terms:
        return DEFAULT_APP_LABEL

    label = terms[0].replace("-", " ").replace("_", " ").strip()
    return label.title() if label else DEFAULT_APP_LABEL


def app_icon_for_window(window) -> str:
    terms = _window_terms(window)
    for patterns, icon, _label in APP_RULES:
        if any(pattern in term for pattern in patterns for term in terms):
            return icon
    return DEFAULT_APP_ICON


def app_label_for_window(window) -> str:
    terms = _window_terms(window)
    for patterns, _icon, label in APP_RULES:
        if any(pattern in term for pattern in patterns for term in terms):
            return label
    return _fallback_label(window)


class AppIconWindow(Window):
    def draw(self, layout, top, level=0):
        self._title_top = top

        left = layout.padding_left + level * layout.level_shift
        layout._layout.font_size = layout.fontsize
        layout._layout.layout.set_alignment(pangocffi.ALIGNMENTS["left"])
        layout._layout.text = self.add_superscript(
            f"{app_icon_for_window(self.window)} {app_label_for_window(self.window)}"
        )

        if self.window is layout._focused:
            fg = layout.active_fg
            bg = layout.active_bg
        elif self.window.urgent:
            fg = layout.urgent_fg
            bg = layout.urgent_bg
        else:
            fg = layout.inactive_fg
            bg = layout.inactive_bg

        layout._layout.colour = fg
        layout._layout.width = layout.panel_width - left
        framed = layout._layout.framed(
            layout.border_width, bg, layout.padding_x, layout.padding_y
        )
        framed.draw_fill(left, top)

        top += framed.height + layout.vspace + layout.border_width
        return super(Window, self).draw(layout, top, level + 1)


class AppIconRoot(Root):
    def add_client(self, win, hint=None):
        parent = None

        if hint is not None:
            parent = hint.parent

        if parent is None:
            section_name = getattr(win, "tree_section", None)
            if section_name is not None:
                parent = self.sections.get(section_name)

        if parent is None:
            parent = self.def_section

        node = AppIconWindow(win)
        parent.add_client(node, hint=hint)
        return node


class AppIconTreeTab(TreeTab):
    def __init__(self, **config):
        super().__init__(**config)
        self.panel_width = self._load_panel_width(self.panel_width)
        self._tree = AppIconRoot(self.sections)

    def clone(self, group):
        clone = Layout.clone(self, group)
        clone._focused = None
        clone._panel = None
        clone._tree = AppIconRoot(self.sections)
        return clone

    def _load_panel_width(self, fallback: int) -> int:
        try:
            with open(STATE_FILE, encoding="utf-8") as state_file:
                state = json.load(state_file)
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return fallback

        panel_width = state.get("panel_width")
        return panel_width if isinstance(panel_width, int) and panel_width >= MIN_PANEL_WIDTH else fallback

    def _save_panel_width(self) -> None:
        try:
            os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
            with open(STATE_FILE, "w", encoding="utf-8") as state_file:
                json.dump({"panel_width": self.panel_width}, state_file)
        except OSError:
            pass

    @expose_command()
    def increase_ratio(self):
        super().increase_ratio()
        self._save_panel_width()

    @expose_command()
    def decrease_ratio(self):
        self.panel_width = max(MIN_PANEL_WIDTH, self.panel_width - 10)
        if self.group is not None:
            self.group.layout_all()
        self._save_panel_width()
