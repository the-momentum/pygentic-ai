"""Smoke test to verify basic package functionality."""

# Test that basic imports work

# Test that version is accessible
from pygentic_ai import __version__

assert __version__ is not None

print("✓ Smoke test passed - basic imports work!")
