"""System Health Report — CPU, RAM, disk, battery, uptime (stdlib only, Windows-friendly)."""
import ctypes
import os
import shutil
import time


def ram_status():
    try:
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        stat = MEMORYSTATUSEX()
        stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
        total_gb = stat.ullTotalPhys / 1e9
        avail_gb = stat.ullAvailPhys / 1e9
        return f"RAM: {total_gb - avail_gb:.1f} / {total_gb:.1f} GB used ({stat.dwMemoryLoad}%)"
    except Exception as e:
        return f"RAM: unavailable ({e})"


def battery_status():
    try:
        class SYSTEM_POWER_STATUS(ctypes.Structure):
            _fields_ = [
                ("ACLineStatus", ctypes.c_byte),
                ("BatteryFlag", ctypes.c_byte),
                ("BatteryLifePercent", ctypes.c_byte),
                ("Reserved1", ctypes.c_byte),
                ("BatteryLifeTime", ctypes.c_ulong),
                ("BatteryFullLifeTime", ctypes.c_ulong),
            ]

        sps = SYSTEM_POWER_STATUS()
        if not ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(sps)):
            return "Battery: unavailable"
        pct = sps.BatteryLifePercent
        if pct == 255 or sps.BatteryFlag == -128:
            return "Battery: no battery (desktop PC)"
        plugged = "plugged in" if sps.ACLineStatus == 1 else "on battery"
        return f"Battery: {pct}% ({plugged})"
    except Exception as e:
        return f"Battery: unavailable ({e})"


def uptime():
    try:
        ms = ctypes.windll.kernel32.GetTickCount64()
        hours = ms / 1000 / 3600
        return f"Uptime: {int(hours)}h {int((hours % 1) * 60)}m"
    except Exception:
        return f"Uptime: unavailable"


def main():
    print("=== SYSTEM HEALTH REPORT ===")
    print(f"CPU cores: {os.cpu_count()}")
    print(ram_status())
    try:
        du = shutil.disk_usage(os.environ.get("SystemDrive", "C:") + "\\")
        print(f"Disk (system drive): {du.used / 1e9:.0f} / {du.total / 1e9:.0f} GB used, {du.free / 1e9:.0f} GB free")
    except Exception as e:
        print(f"Disk: unavailable ({e})")
    print(battery_status())
    print(uptime())
    print(f"Report time: {time.strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Health report error: {e}")
