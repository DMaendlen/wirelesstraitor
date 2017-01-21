#!/usr/bin/python3

from .display import CommandLineLocationDisplay
from .osint import LocationSearcher
from .sigint import ProbeRequestFinder, ProbeRequestParser

if __name__ == "__main__":
    prfinder = ProbeRequestFinder()
    prparser = ProbeRequestParser()
    locationsearcher = LocationSearcher()
    display = LocationDisplay()

    prfinder.register(prparser)
    prparser.register(locationsearcher)
    locationsearcher.register(display)

    prfinder.start()
