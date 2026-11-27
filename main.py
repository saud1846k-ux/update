from __future__ import annotations

from myers502_app import APP_VERSION, AUTHOR_NAME, Myers502CodecApp

BANNER = f"""
============================================================
   {AUTHOR_NAME} BASE64 CODEC TOOL  (v{APP_VERSION})
   Formats: UTF-8  |  PowerShell UTF-16LE (-EncodedCommand)
============================================================
"""


def main() -> None:
    print(BANNER)
    app = Myers502CodecApp()
    app.mainloop()


if __name__ == "__main__":
    main()