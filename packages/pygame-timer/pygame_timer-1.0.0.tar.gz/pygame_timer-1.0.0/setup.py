from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = 'A package for various types of timers'
LONG_DESCRIPTION = '''
A comprehensive Python package providing various types of timers including:
- Target Timer: Tracks time against a target time.
- Stopwatch Timer: A simple stopwatch.
- Interval Timer: Checks if a specified interval has passed.
- Activation Timer: Checks if an activation state has started or stopped for a certain time.
- Cooldown Timer: Tracks cooldown periods.

This package is useful for building applications that require precise timing functionality.
'''
URL = 'https://github.com/FrickTzy/Pygame-Timer'

setup(
    name="pygame_timer",
    version=VERSION,
    author="FrickTzy (Kurt Arnoco)",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    url=URL,
    install_requires=['pygame'],
    keywords=['python', 'pygame', 'python game', 'python game development', 'pygame timer'],
)