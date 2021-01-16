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
