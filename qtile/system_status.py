from __future__ import annotations

from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class CpuUsage:
    def __init__(self):
        self._previous: tuple[int, int] | None = None

    def __call__(self) -> str:
        sample = self._read_cpu_sample()
        if sample is None:
            return "󰻠 N/A"

        if self._previous is None:
            self._previous = sample
            return "󰻠 --%"

        idle, total = sample
        previous_idle, previous_total = self._previous
        self._previous = sample

        total_delta = total - previous_total
        idle_delta = idle - previous_idle
        if total_delta <= 0:
            return "󰻠 N/A"

        usage = (1 - idle_delta / total_delta) * 100
        return f"󰻠 {usage:.0f}%"

    @staticmethod
    def _read_cpu_sample() -> tuple[int, int] | None:
        try:
            fields = Path("/proc/stat").read_text().splitlines()[0].split()[1:]
            values = [int(value) for value in fields]
        except (OSError, IndexError, ValueError):
            return None

        idle = values[3] + values[4]
        total = sum(values)
        return idle, total


def memory_status() -> str:
    try:
        meminfo = {}
        for line in Path("/proc/meminfo").read_text().splitlines():
            key, value = line.split(":", 1)
            meminfo[key] = int(value.strip().split()[0])
    except (OSError, ValueError, IndexError):
        return "󰍛 N/A"

    total = meminfo.get("MemTotal")
    available = meminfo.get("MemAvailable")
    if not total or available is None:
        return "󰍛 N/A"

    used_gib = (total - available) / 1024 / 1024
    total_gib = total / 1024 / 1024
    return f"󰍛 {used_gib:.1f}/{total_gib:.1f}G"


def cpu_temperature_status() -> str:
    preferred = _read_temperature("coretemp", "Package id 0")
    fallback = preferred or _read_temperature("coretemp", None) or _read_temperature(None, None)

    if fallback is None:
        return "󰔏 N/A"

    return f"󰔏 {fallback:.0f}°C"


def _read_temperature(chip_name: str | None, label_name: str | None) -> float | None:
    for hwmon in sorted(Path("/sys/class/hwmon").glob("hwmon*")):
        name_path = hwmon / "name"
        try:
            current_chip = name_path.read_text().strip()
        except OSError:
            current_chip = ""

        if chip_name is not None and current_chip != chip_name:
            continue

        for input_path in sorted(hwmon.glob("temp*_input")):
            label_path = input_path.with_name(input_path.name.replace("_input", "_label"))
            try:
                current_label = label_path.read_text().strip()
            except OSError:
                current_label = ""

            if label_name is not None and current_label != label_name:
                continue

            try:
                return int(input_path.read_text().strip()) / 1000
            except (OSError, ValueError):
                continue

    return None


def weather_status() -> str:
    query = urlencode({"format": "󰖐 %l %t", "lang": "pt-br"})
    request = Request(
        f"https://wttr.in/?m&{query}",
        headers={"User-Agent": "qtile-arch-dotfiles"},
    )

    try:
        with urlopen(request, timeout=5) as response:
            text = response.read(160).decode("utf-8", errors="replace").strip()
    except (OSError, URLError, TimeoutError):
        return "󰖐 N/A"

    if not text or text.startswith("<"):
        return "󰖐 N/A"
    return " ".join(text.split())


cpu_status = CpuUsage()

