# Copyright 2019-2024 The kikuchipy developers
#
# This file is part of kikuchipy.
#
# kikuchipy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# kikuchipy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kikuchipy. If not, see <http://www.gnu.org/licenses/>.

"""Pattern filters used on signals, e.g. for pattern averaging."""

__all__ = [
    "Window",
    "distance_to_origin",
    "highpass_fft_filter",
    "lowpass_fft_filter",
    "modified_hann",
]


def __dir__():
    return sorted(__all__)


def __getattr__(name):
    _import_mapping = {
        "Window": "window",
        "distance_to_origin": "window",
        "highpass_fft_filter": "window",
        "lowpass_fft_filter": "window",
        "modified_hann": "window",
    }
    if name in __all__:
        import importlib

        if name in _import_mapping.keys():
            import_path = f"{__name__}.{_import_mapping.get(name)}"
            return getattr(importlib.import_module(import_path), name)
        else:  # pragma: no cover
            return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
