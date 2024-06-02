#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
:filename: scripts.sample.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: A script to demonstrate AudiooPy capabilities.

.. _This file is part of AudiooPy:
..
    ---------------------------------------------------------------------

    Copyright (C) 2024 Brigitte Bigi
    Laboratoire Parole et Langage, Aix-en-Provence, France

    Use of this software is governed by the GNU Public License, version 3.

    AudiooPy is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    AudiooPy is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with AudiooPy. If not, see <https://www.gnu.org/licenses/>.

    This banner notice must not be removed.

    ---------------------------------------------------------------------

"""

import logging
import audioopy.aio
from audioopy.ipus.channelsilences import ChannelSilences
from audioopy.ipus.searchfor import SearchForIPUs

logging.getLogger().setLevel(0)


# Extract the only channel of the oriana1.wav sample
audio = audioopy.aio.open("tests/samples/oriana1.wav")
audio.extract_channel(0)
channel = audio[0]

# Create ChannelSilences() instance: estimate the rms values in windows of 20 ms length
channel_silences = ChannelSilences(channel, win_len=0.02, vagueness=0.005)
# Search for all the silences, comparing each rms to an automatically estimated threshold
threshold = channel_silences.search_silences()
print(list(channel_silences))
# Keep only silences during more than a given duration
channel_silences.filter_silences(threshold // 2, 0.250)
print(list(channel_silences))
# Get the (from_pos, to_pos) of the tracks during more than a given duration
tracks_1 = channel_silences.extract_tracks(0.300, 0.02, 0.02)
print(tracks_1)

# Create a SearchForIPUs() instance
searcher = SearchForIPUs(channel)
# Perform the full process and return tracks in the frames domain
tracks_2 = searcher.get_tracks(time_domain=False)
print(tracks_2)
assert tracks_1 == tracks_2
# Perform the full process and return tracks in the time domain
tracks = searcher.get_tracks(time_domain=True)
print(tracks)
