# -*- coding: UTF-8 -*-
"""
:filename: aio.audiofactory.py
:author: Nicolas Chazeau, Brigitte Bigi
:contact: contact@sppas.org
:summary: Factory class for creating an AudioPCM.

.. _This file is part of SPPAS: https://sppas.org/
..
    ---------------------------------------------------------------------

     ######   ########   ########      ###      ######
    ##    ##  ##     ##  ##     ##    ## ##    ##    ##     the automatic
    ##        ##     ##  ##     ##   ##   ##   ##            annotation
     ######   ########   ########   ##     ##   ######        and
          ##  ##         ##         #########        ##        analysis
    ##    ##  ##         ##         ##     ##  ##    ##         of speech
     ######   ##         ##         ##     ##   ######

    Copyright (C) 2011-2024  Brigitte Bigi
    Laboratoire Parole et Langage, Aix-en-Provence, France

    Use of this software is governed by the GNU Affero Public License, version 3.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.

    This banner notice must not be removed.

    ---------------------------------------------------------------------

"""

from .waveio import WaveIO

from ..audioopyexc import AudioTypeError

# ----------------------------------------------------------------------------


class AudioFactory(object):
    """Factory for sppasAudioPCM.

    """

    AUDIO_TYPES = {
        "wav": WaveIO,
        "wave": WaveIO,
        }

    @staticmethod
    def new_audio_pcm(audio_type):
        """Return a new AudioPCM according to the format.

        :param audio_type: (str) a file extension.
        :return: AudioPCM

        """
        try:
            return AudioFactory.AUDIO_TYPES[audio_type.lower()]()
        except KeyError:
            raise AudioTypeError(audio_type)
