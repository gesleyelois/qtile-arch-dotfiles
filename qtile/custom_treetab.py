from __future__ import annotations

from collections.abc import Iterable

from libqtile.layout.base import Layout
from libqtile.layout.tree import Root, Section, TreeTab, Window


APP_ICON_RULES: tuple[tuple[tuple[str, ...], str], ...] = (
    (("alacritty", "kitty", "wezterm", "terminal", "warp"), ""),
    (("firefox",), ""),
    (("vivaldi",), ""),
    (("chromium", "chrome", "brave"), ""),
    (("code-oss", "code", "visual studio code", "cursor"), ""),
    (("jetbrains", "intellij", "idea", "pycharm", "webstorm"), ""),
    (("discord",), ""),
    (("slack",), ""),
    (("spotify",), ""),
    (("obsidian",), "󰠮"),
    (("postman", "insomnia"), "󰛮"),
    (("thunar", "nautilus", "dolphin", "file"), ""),
)

DEFAULT_APP_ICON = "󰣆"


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


def app_icon_for_window(window) -> str:
    terms = _window_terms(window)
    for patterns, icon in APP_ICON_RULES:
        if any(pattern in term for pattern in patterns for term in terms):
            return icon
    return DEFAULT_APP_ICON


class AppIconWindow(Window):
    def draw(self, layout, top, level=0):
        self._title_top = top

        left = layout.padding_left + level * layout.level_shift
        title = self.window.name or "Untitled"
        layout._layout.font_size = layout.fontsize
        layout._layout.text = self.add_superscript(f"{app_icon_for_window(self.window)} {title}")

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
        self._tree = AppIconRoot(self.sections)

    def clone(self, group):
        clone = Layout.clone(self, group)
        clone._focused = None
        clone._panel = None
        clone._tree = AppIconRoot(self.sections)
        return clone

