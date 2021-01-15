import re
import subprocess

import NetworkManager


class Py3status:

    vpn = "No VPN"

    def _get_new_output(self):
        conn = NetworkManager.NetworkManager.ActiveConnections
        conn = ["ProtonVPN" for c in conn if "proton" in c.Id]

        self.vpn = str(conn[0]) if conn else "No VPN"

        result = subprocess.run(['protonvpn-cli', 'status'], stdout=subprocess.PIPE)
        result = result.stdout.decode("utf-8")

        country = re.search("Country: \\t ([A-Za-z]+)", result)
        country = "" if not country else country.group(1)

        features = re.search(r"Server Features: ([A-Za-z0-9]+)", result)
        features = "" if not features else " | " + features.group(1)

        killswitch = re.search(r"Kill switch:\s+(\w+)", result)
        killswitch = "" if not killswitch else " | KS: " + killswitch.group(1)

        return self.py3.safe_format("{vpn}: {country}{features}{killswitch}",
                                    {"vpn": self.vpn, "country": country, "features": features,
                                     "killswitch": killswitch})

    def on_click(self, event):
        if self.vpn != "No VPN":
            result = subprocess.run(['protonvpn-cli', 'disconnect'], stdout=subprocess.PIPE)
        else:
            result = subprocess.run(['protonvpn-cli', 'connect', '-f', '-p', 'tcp'], stdout=subprocess.PIPE)

    def protonvpn_status(self):
        return {
            'full_text': self._get_new_output(),
            'cached_until': self.py3.time_in(3)
        }


if __name__ == "__main__":
    from py3status.module_test import module_test
    module_test(Py3status)
