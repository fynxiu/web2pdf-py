from selenium import webdriver
from selenium.webdriver.common.by import By
import json

# useful links
# https://chromedriver.chromium.org/capabilities

# why not js?
# 1. setUserPreferences not working for me (chrome)
# 2. poor performance
# 3. poor documentation

# Preference is the user preferences of chrome, path: $HOME/.config/google-chrome/Default/Preferences (ubuntu)
# pdf would not be generated in headless mode

printingAppState = {
    "version": 2,
    "recentDestinations": [
        {
            "id": "Save as PDF",
            "origin": "local",
            "account": "",
            "capabilities": {
                "printer": {
                    "color": {
                        "option": [
                            {
                                "is_default": True,
                                "type": "STANDARD_COLOR",
                                "vendor_id": "2",
                            }
                        ]
                    },
                    "media_size": {
                        "option": [
                            {
                                "height_microns": 1189000,
                                "name": "ISO_A0",
                                "width_microns": 841000,
                                "custom_display_name": "A0",
                            },
                            {
                                "height_microns": 841000,
                                "name": "ISO_A1",
                                "width_microns": 594000,
                                "custom_display_name": "A1",
                            },
                            {
                                "height_microns": 594000,
                                "name": "ISO_A2",
                                "width_microns": 420000,
                                "custom_display_name": "A2",
                            },
                            {
                                "height_microns": 420000,
                                "name": "ISO_A3",
                                "width_microns": 297000,
                                "custom_display_name": "A3",
                            },
                            {
                                "height_microns": 297000,
                                "is_default": True,
                                "name": "ISO_A4",
                                "width_microns": 210000,
                                "custom_display_name": "A4",
                            },
                            {
                                "height_microns": 210000,
                                "name": "ISO_A5",
                                "width_microns": 148000,
                                "custom_display_name": "A5",
                            },
                            {
                                "height_microns": 355600,
                                "name": "NA_LEGAL",
                                "width_microns": 215900,
                                "custom_display_name": "Legal",
                            },
                            {
                                "height_microns": 279400,
                                "name": "NA_LETTER",
                                "width_microns": 215900,
                                "custom_display_name": "Letter",
                            },
                            {
                                "height_microns": 431800,
                                "name": "NA_LEDGER",
                                "width_microns": 279400,
                                "custom_display_name": "Tabloid",
                            },
                        ]
                    },
                    "page_orientation": {
                        "option": [
                            {"type": "PORTRAIT"},
                            {"type": "LANDSCAPE"},
                            {"is_default": True, "type": "AUTO"},
                        ]
                    },
                },
                "version": "1.0",
            },
            "displayName": "另存为 PDF",
            "extensionId": "",
            "extensionName": "",
            "icon": "cr:insert-drive-file",
        }
    ],
    "isCssBackgroundEnabled": False,
    "customMargins": {},
    "isHeaderFooterEnabled": False,
    "mediaSize": {
        "height_microns": 297000,
        "is_default": True,
        "name": "ISO_A4",
        "width_microns": 210000,
        "custom_display_name": "A4",
    },
}

# chrome preferences
prefs = {
    "printing.print_preview_sticky_settings.appState": json.dumps(printingAppState),
    "savefile": {"default_directory": "/home/fyn/Documents/inbox"},
}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--enable-print-browser")
chrome_options.add_argument("--kiosk-printing") # enable silent printing
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://docs.flutter.dev/development/ui/layout") # It does not matter which uri is, just an entry point.
links = set(
    filter(
        lambda x: "docs.flutter.dev" in x,
        filter(
            lambda x: "#" not in x,
            map(
                lambda x: x.get_attribute("href"),
                driver.find_elements(by=By.CLASS_NAME, value="site-sidebar")[
                    1
                ].find_elements(by=By.TAG_NAME, value="a"),
            ),
        ),
    )
)
for link in links:
    print("printing:", link)
    driver.get(link)
    driver.execute_script(
        """
  function printPage() {
    for (const x of Array.prototype.slice.call(
      document.querySelectorAll(".site-header")
    ))
      x.remove();
    for (const x of Array.prototype.slice.call(
      document.querySelectorAll("#overlay-under-drawer")
    ))
      x.remove();
    for (const x of Array.prototype.slice.call(
      document.querySelectorAll(".site-banner")
    ))
      x.remove();
    for (const x of Array.prototype.slice.call(
      document.querySelectorAll("#page-github-links")
    ))
      x.remove();
    for (const x of Array.prototype.slice.call(
      document.querySelectorAll("footer")
    ))
      x.remove();

    for (const x of Array.prototype.slice.call(
      document.querySelectorAll(".site-sidebar")
    ))
      x.remove();
    for (const x of Array.prototype.slice.call(
      document.querySelectorAll("#site-toc--side")
    ))
      x.remove();
    for (const x of Array.prototype.slice.call(document.querySelectorAll("main")))
      $(x).removeAttr("class");
    document.querySelectorAll("body")[0].style.fontSize = "1.5rem";
    window.print();
  }
  printPage();
  """
    )
print("done")
