"""
Displays status of connection to ProtonVPN, on click it connects you to the fastest server or disconnects you.

Configuration parameters:
    cache_timeout: refresh interval for this module (default 5)
    format: display format for this module (default '{vpn}: {country}{features}{killswitch}')
    connected_message: Message to display when connected (default 'ProtonVPN')
    not_connected_message: Message to display when disconnected (default 'No VPN')

Format placeholders:
    {vpn} The connected or disconnected status
    {country} Country to which connected
    {features} What features the server has (e.g. P2P)
    {killswitch} Whether the killswitch is enabled

Color options:
    color: color_good when connected, color_bad when disconnected

Requires:
    protonvpn-cli: https://github.com/ProtonVPN/linux-cli

Examples:
```
# configuration which only shows if you're connected and if the killswitch is on.

protonvpn_status {
    fromat = '{vpn}:{killswitch}'
    cache_timeout = 10
}
```

@author andcarnivorous

SAMPLE OUTPUT
disconnected
{'full_text': 'No VPN', 'color': '#FF0000', 'cached_until': 1610789504.0}

connected
{'full_text': 'ProtonVPN: Switzerland | KS: On', 'color': '#00FF00', 'cached_until': 1610791125.0}
"""


import re
import subprocess

STRING_NOT_INSTALLED = 'not installed'


class Py3status:

    format = '{vpn}: {country}{features}{killswitch}'
    connected_message = 'ProtonVPN'
    not_connected_message = 'No VPN'
    cache_timeout = 5

    def _get_new_output(self):

        if not self.py3.check_commands('protonvpn-cli'):
            raise Exception(STRING_NOT_INSTALLED)

        result = subprocess.run(['protonvpn-cli', 'status'], stdout=subprocess.PIPE)
        result = result.stdout.decode('utf-8')

        if 'No active ProtonVPN connection' in result:
            self.color = self.py3.COLOR_BAD
            return self.py3.safe_format('{vpn}', {'vpn':self.not_connected_message})

        self.color = self.py3.COLOR_GOOD

        country = re.search('Country: \\t ([A-Za-z]+)', result)
        country = '' if not country else country.group(1)

        features = re.search(r'Server Features: ([A-Za-z0-9]+)', result)
        features = '' if not features else ' | ' + features.group(1)

        killswitch = re.search(r'Kill switch:\s+(\w+)', result)
        killswitch = '' if not killswitch else ' | KS: ' + killswitch.group(1)

        return self.py3.safe_format(self.format,
                                    {'vpn': self.connected_message, 'country': country, 'features': features,
                                     'killswitch': killswitch})

    def on_click(self, event):
        if self.vpn != 'No VPN':
            result = subprocess.run(['protonvpn-cli', 'disconnect'], stdout=subprocess.PIPE)
        else:
            result = subprocess.run(['protonvpn-cli', 'connect', '-f', '-p', 'tcp'], stdout=subprocess.PIPE)

    def protonvpn_status(self):
        return {
            'full_text': self._get_new_output(),
            'cached_until': self.py3.time_in(self.cache_timeout),
            'color': self.color
        }


if __name__ == '__main__':
    from py3status.module_test import module_test
    module_test(Py3status)
