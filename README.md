# wirelesstraitor
What WLAN-autoconnect tells us about you

## What this is

A small, currently cli-only, tool to show the geolocation of APs your device wants to connect to.

## What this is not

A tool to "hack" (whatever you think this means) a device.

## How it works

To install, please use pip:
```bash
	sudo pip install --upgrade .
```

Afterwards run
```bash
	wirelesstraitor-cli /path/to/your/apikey
```

You can get an API key from [Google](https://developers.google.com/maps/documentation/geolocation/get-api-key)

Internally, wirelesstraitor starts a process that looks for 802.11 probe request
packets, parses them and passes the parsed data on to Google's geolocation API.
Then it displays the info it could gather from that.

The program runs until you hit Ctrl-C.

## Credit
Thank you for the implementation of the Observer-Pattern, [Chad Lung](http://www.giantflyingsaucer.com/blog/?p=5117)!
