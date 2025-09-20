#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import json
import os

PLIST = os.path.expanduser("~/Library/Preferences/com.brave.Browser.plist")
NEEDS_SUDO = False  # No longer need sudo for user preferences

FEATURES = [
    ("Telemetry & Reporting", [
        ("Disable Metrics Reporting", "MetricsReportingEnabled", False, "bool"),
        ("Disable Safe Browsing Reporting", "SafeBrowsingExtendedReportingEnabled", False, "bool"),
        ("Disable URL Data Collection", "UrlKeyedAnonymizedDataCollectionEnabled", False, "bool"),
        ("Disable Feedback Surveys", "FeedbackSurveysEnabled", False, "bool"),
    ]),
    ("Privacy & Security", [
        ("Disable Safe Browsing", "SafeBrowsingProtectionLevel", 0, "int"),
        ("Disable Autofill (Addresses)", "AutofillAddressEnabled", False, "bool"),
        ("Disable Autofill (Credit Cards)", "AutofillCreditCardEnabled", False, "bool"),
        ("Disable Password Manager", "PasswordManagerEnabled", False, "bool"),
        ("Disable Browser Sign-in", "BrowserSignin", 0, "int"),
        ("Disable WebRTC IP Leak", "WebRtcIPHandling", "disable_non_proxied_udp", "string"),
        ("Disable QUIC Protocol", "QuicAllowed", False, "bool"),
        ("Block Third Party Cookies", "BlockThirdPartyCookies", True, "bool"),
        ("Enable Do Not Track", "EnableDoNotTrack", True, "bool"),
        ("Force Google SafeSearch", "ForceGoogleSafeSearch", True, "bool"),
        ("Disable IPFS", "IPFSEnabled", False, "bool"),
        ("Disable Incognito Mode", "IncognitoModeAvailability", 1, "int"),
        ("Force Incognito Mode", "IncognitoModeAvailability", 2, "int"),
    ]),
    ("Brave Features", [
        ("Disable Brave Rewards", "BraveRewardsDisabled", True, "bool"),
        ("Disable Brave Wallet", "BraveWalletDisabled", True, "bool"),
        ("Disable Brave VPN", "BraveVPNDisabled", True, "bool"),
        ("Disable Brave AI Chat", "BraveAIChatEnabled", False, "bool"),
        ("Disable Brave Shields", "BraveShieldsDisabledForUrls", ["https://*", "http://*"], "array"),
        ("Disable Tor", "TorDisabled", True, "bool"),
        ("Disable Sync", "SyncDisabled", True, "bool"),
    ]),
    ("Performance & Bloat", [
        ("Disable Background Mode", "BackgroundModeEnabled", False, "bool"),
        ("Disable Media Recommendations", "MediaRecommendationsEnabled", False, "bool"),
        ("Disable Shopping List", "ShoppingListEnabled", False, "bool"),
        ("Always Open PDF Externally", "AlwaysOpenPdfExternally", True, "bool"),
        ("Disable Translate", "TranslateEnabled", False, "bool"),
        ("Disable Spellcheck", "SpellcheckEnabled", False, "bool"),
        ("Disable Promotions", "PromotionsEnabled", False, "bool"),
        ("Disable Search Suggestions", "SearchSuggestEnabled", False, "bool"),
        ("Disable Printing", "PrintingEnabled", False, "bool"),
        ("Disable Default Browser Prompt", "DefaultBrowserSettingEnabled", False, "bool"),
        ("Disable Developer Tools", "DeveloperToolsDisabled", True, "bool"),
    ]),
]

DNS_MODES = ["automatic", "off", "custom"]

SECTION_TO_POSITION = {
    "Telemetry & Reporting": (0, 0),
    "Privacy & Security": (0, 1),
    "Brave Features": (1, 0),
    "Performance & Bloat": (1, 1),
}

class BeBraveApp:
    def __init__(self, master):
        self.master = master
        master.title("BeBrave for macOS")
        self.checkbox_vars = {}
        self.dns_mode = tk.StringVar(value=DNS_MODES[0])

        main_frame = tk.Frame(master, padx=10, pady=10)
        main_frame.pack(fill="both", expand=True)

        # --- Banner at the top ---
        banner_text = "Ready to configure Brave Browser preferences"
        banner_bg = "#d4f7d4"
        banner_fg = "#006600"
        banner = tk.Label(
            main_frame,
            text=banner_text,
            bg=banner_bg,
            fg=banner_fg,
            font=("Helvetica", 12, "bold"),
            pady=6
        )
        banner.grid(row=0, column=0, sticky="ew", pady=(0, 6), columnspan=2)

        # --- Select All Checkbox ---
        self.select_all_var = tk.BooleanVar()
        select_all_cb = tk.Checkbutton(main_frame, text="Select All", variable=self.select_all_var, command=self.on_select_all)
        select_all_cb.grid(row=1, column=0, sticky="w", padx=8, pady=(0, 5))

        # Create 2x2 grid for quadrants
        quadrant_frame = tk.Frame(main_frame)
        quadrant_frame.grid(row=2, column=0, sticky="nsew")
        quadrant_frame.columnconfigure(0, weight=1)
        quadrant_frame.columnconfigure(1, weight=1)
        quadrant_frame.rowconfigure(0, weight=1)
        quadrant_frame.rowconfigure(1, weight=1)

        self.section_frames = {}
        for section, _ in FEATURES:
            r, c = SECTION_TO_POSITION[section]
            outer, inner = self._scrollable_section(quadrant_frame, section)
            outer.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
            quadrant_frame.grid_columnconfigure(c, weight=1)
            quadrant_frame.grid_rowconfigure(r, weight=1)
            self.section_frames[section] = (outer, inner)

        # Populate checkboxes in correct quadrant
        for section, feats in FEATURES:
            outer, inner = self.section_frames[section]
            for feat in feats:
                var = tk.BooleanVar()
                cb = tk.Checkbutton(inner, text=feat[0], variable=var, anchor="w", justify="left",
                                   command=self.on_any_checkbox)
                cb.pack(anchor="w", padx=10, pady=2)
                self.checkbox_vars[feat[1]] = (var, feat)

        # Control area at bottom
        controls = tk.Frame(main_frame, pady=8)
        controls.grid(row=3, column=0, sticky="ew")
        controls.columnconfigure(0, weight=1)

        tk.Label(controls, text="DNS Over HTTPS Mode:").pack(side="left")
        dns_menu = tk.OptionMenu(controls, self.dns_mode, *DNS_MODES)
        dns_menu.pack(side="left", padx=8)

        tk.Button(controls, text="Apply Settings", command=self.apply_settings, bg="#81B29A", fg="black").pack(side="left", padx=5)
        tk.Button(controls, text="Reset All", command=self.reset_all, bg="#E07A5F", fg="white").pack(side="left", padx=5)
        tk.Button(controls, text="Export", command=self.export_settings).pack(side="left", padx=5)
        tk.Button(controls, text="Import", command=self.import_settings).pack(side="left", padx=5)

        # Load existing settings after UI is created
        self.load_existing_settings()

    def _scrollable_section(self, parent, title):
        outer = tk.Frame(parent, relief="groove", borderwidth=2)
        tk.Label(outer, text=title, font=("Helvetica", 12, "bold"), fg="#E07A5F").pack(anchor="w", pady=4, padx=6)
        canvas = tk.Canvas(outer, borderwidth=0, height=180)
        inner = tk.Frame(canvas)
        vsb = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=inner, anchor="nw")
        def _on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        inner.bind("<Configure>", _on_configure)
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        return outer, inner

    # --- Select All logic ---
    def on_select_all(self):
        val = self.select_all_var.get()
        for var, _ in self.checkbox_vars.values():
            var.set(val)

    def on_any_checkbox(self):
        # Whenever a checkbox is changed, update select_all_var accordingly
        all_selected = all(var.get() for var, _ in self.checkbox_vars.values())
        if self.select_all_var.get() != all_selected:
            self.select_all_var.set(all_selected)

    def apply_settings(self):
        for key, (var, feat) in self.checkbox_vars.items():
            if var.get():
                self.write_setting(feat[1], feat[2], feat[3])
            else:
                self.delete_setting(feat[1])

        dns = self.dns_mode.get()
        if dns:
            self.write_setting("DnsOverHttpsMode", dns, "string")

        messagebox.showinfo("Success", "Settings applied! Restart Brave to see changes.")

    def reset_all(self):
        if messagebox.askyesno("Reset All", "Erase ALL Brave policy settings and restore defaults?"):
            if os.path.exists(PLIST):
                subprocess.run(["rm", "-f", PLIST])
            messagebox.showinfo("Reset", "All settings reset! Restart Brave to see changes.")
            for var, _ in self.checkbox_vars.values():
                var.set(False)
            self.select_all_var.set(False)
            self.dns_mode.set(DNS_MODES[0])

    def export_settings(self):
        settings = {
            "features": [k for k, (var, _) in self.checkbox_vars.items() if var.get()],
            "dns_mode": self.dns_mode.get()
        }
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files","*.json")])
        if path:
            with open(path, "w") as f:
                json.dump(settings, f)
            messagebox.showinfo("Exported", f"Exported to {path}")

    def import_settings(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files","*.json")])
        if path:
            with open(path) as f:
                settings = json.load(f)
            for k, (var, _) in self.checkbox_vars.items():
                var.set(k in settings.get("features", []))
            # After import, update select_all checkbox state
            all_selected = all(var.get() for var, _ in self.checkbox_vars.values())
            self.select_all_var.set(all_selected)
            dns = settings.get("dns_mode")
            if dns in DNS_MODES:
                self.dns_mode.set(dns)
            messagebox.showinfo("Imported", f"Imported from {path}")

    def write_setting(self, key, value, typ):
        if typ == "bool":
            v = "TRUE" if value else "FALSE"
            subprocess.run(["defaults", "write", PLIST, key, "-bool", v])
        elif typ == "int":
            subprocess.run(["defaults", "write", PLIST, key, "-int", str(value)])
        elif typ == "string":
            subprocess.run(["defaults", "write", PLIST, key, "-string", str(value)])
        elif typ == "array":
            subprocess.run(["defaults", "delete", PLIST, key], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            args = ["defaults", "write", PLIST, key, "-array"] + list(map(str, value))
            subprocess.run(args)

    def load_existing_settings(self):
        """Load existing plist settings and update UI checkboxes"""
        if not os.path.exists(PLIST):
            return

        for key, (var, feat) in self.checkbox_vars.items():
            current_value = self.read_setting(key, feat[3])
            if current_value is not None:
                # Check if current value matches the "enabled" value for this feature
                expected_value = feat[2]  # The value we set when enabling this feature
                if current_value == expected_value:
                    var.set(True)

        # Load DNS setting
        dns_value = self.read_setting("DnsOverHttpsMode", "string")
        if dns_value and dns_value in DNS_MODES:
            self.dns_mode.set(dns_value)

        # Update select_all checkbox state after loading
        all_selected = all(var.get() for var, _ in self.checkbox_vars.values())
        self.select_all_var.set(all_selected)

    def read_setting(self, key, typ):
        """Read a setting from the plist file"""
        try:
            result = subprocess.run(
                ["defaults", "read", PLIST, key],
                capture_output=True,
                text=True,
                check=True
            )
            value_str = result.stdout.strip()

            if typ == "bool":
                return value_str == "1"
            elif typ == "int":
                return int(value_str)
            elif typ == "string":
                return value_str
            elif typ == "array":
                # For arrays, we'll do a simple check if it exists and has content
                return len(value_str) > 0 and value_str != "()"
        except (subprocess.CalledProcessError, ValueError):
            # Setting doesn't exist or can't be read
            return None

    def delete_setting(self, key):
        subprocess.run(["defaults", "delete", PLIST, key], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    root = tk.Tk()
    app = BeBraveApp(root)
    root.mainloop()
