import os
import subprocess

from custom_treetab import AppIconTreeTab
from libqtile import bar, hook, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from system_status import cpu_status, cpu_temperature_status, memory_status, weather_status

mod = "mod4"
terminal = guess_terminal()


def sep():
    return widget.Sep(linewidth=0, padding=6)


keys = [
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "Tab", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod, "shift"], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod, "shift"], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod, "shift"], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod, "shift"], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle split/unsplit"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod, "control"], "t", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn cmd prompt"),
    Key([mod], "space", lazy.spawn("rofi -show drun"), desc="App launcher"),
    Key([], "Print", lazy.spawn("flameshot gui"), desc="Flameshot GUI"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-"), desc="Decrease brightness"),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%"), desc="Increase brightness"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5% && notify-send 'Volume up'"), desc="Increase volume"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5% && notify-send 'Volume down'"), desc="Decrease volume"),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle && notify-send 'Volume mute'"), desc="Mute volume"),
]

groups = [Group(i) for i in "12345"]
for group in groups:
    keys.extend(
        [
            Key([mod], group.name, lazy.group[group.name].toscreen(), desc=f"Switch to group {group.name}"),
            Key([mod, "shift"], group.name, lazy.window.togroup(group.name, switch_group=True), desc=f"Move window to group {group.name}"),
        ]
    )

layouts = [
    AppIconTreeTab(
        sections=["Apps"],
        panel_width=170,
        bg_color="1e1e2e",
        active_bg="89b4fa",
        active_fg="11111b",
        inactive_bg="313244",
        inactive_fg="cdd6f4",
        section_fg="f5c2e7",
    ),
    layout.Columns(border_focus="#ff0000", border_width=2),
    layout.Max(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={"launch": ("#ff0000", "#ffffff")},
                    name_transform=lambda name: name.upper(),
                ),
                widget.Systray(),
                sep(),
                widget.DF(partition="/", format="󰋊 {uf}{m} livre", visible_on_warn=False, warn_space=40),
                sep(),
                widget.Battery(
                    battery="BAT1",
                    charge_char="󰂄",
                    discharge_char="󰁹",
                    full_char="󰁹",
                    not_charging_char="󰂃",
                    unknown_char="󰂑",
                    format="{char} {percent:2.0%}",
                    full_short_text="󰁹 100%",
                    show_short_text=False,
                    low_percentage=0.15,
                ),
                sep(),
                widget.GenPollText(func=cpu_status, update_interval=2),
                sep(),
                widget.GenPollText(func=memory_status, update_interval=5),
                sep(),
                widget.GenPollText(func=cpu_temperature_status, update_interval=5),
                sep(),
                widget.GenPollText(func=weather_status, update_interval=900),
                sep(),
                widget.Volume(fmt="󰕾 {}", update_interval=0.1),
                sep(),
                widget.Clock(format="%Y-%m-%d %a %H:%M"),
                widget.QuickExit(),
            ],
            24,
        ),
    ),
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False

floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(title="pinentry"),
    ]
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True


@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.Popen(["sh", script])


wmname = "LG3D"
