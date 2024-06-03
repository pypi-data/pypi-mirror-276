# -*- coding: utf-8 -*-
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

import os

import pytest

import kikuchipy as kp

DIR_PATH = os.path.dirname(__file__)
EMSOFT_FILE = os.path.join(
    DIR_PATH, "../../../data/emsoft_ecp_master_pattern/ecp_master_pattern.h5"
)


class TestEMsoftECPMasterPatternReader:
    """All other functionality supported by the reader is tested in the
    EBSD master pattern reader tests.
    """

    @pytest.mark.parametrize(
        "lazy, class_type",
        [(False, kp.signals.ECPMasterPattern), (True, kp.signals.LazyECPMasterPattern)],
    )
    def test_file_reader(self, lazy, class_type):
        s = kp.load(EMSOFT_FILE, lazy=lazy)
        assert isinstance(s, class_type)
