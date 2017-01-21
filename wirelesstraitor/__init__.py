from wirelesstraitor.display import CommandLineLocationDisplay
from wirelesstraitor.osint import LocationSearcher
from wirelesstraitor.sigint import ProbeRequestFinder, ProbeRequestParser
from wirelesstraitor.mockup import PacketMockup

if __name__ == "__main__":
    prfinder = ProbeRequestFinder()
    prparser = ProbeRequestParser()
    locationsearcher = LocationSearcher()
    display = LocationDisplay()

    prfinder.register(prparser)
    prparser.register(locationsearcher)
    locationsearcher.register(display)

    prfinder.start()
