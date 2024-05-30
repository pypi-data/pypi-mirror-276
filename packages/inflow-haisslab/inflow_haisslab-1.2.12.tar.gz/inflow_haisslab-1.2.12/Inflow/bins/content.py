# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 15:36:36 2023

@author: tjostmou
"""

import struct, os, numpy as np


class Reader:

    def __init__(self, filepath):
        """
        Parameters
        ----------
        filepath : str
            path to the file binfile to read.
        """

        self.path = filepath

    def piezzo_stim_data(self, data_rate=200000, bytes_size=8, format="d", byte_order="@"):
        """Returns data formated as piezzo stimulation bin files, to a numpy array.

        Parameters
        ----------
        data_rate : int, optional
            In hertz. The default is 200000.
        bytes_size : TYPE, optional
            size in bytes of one data point. The default is 8.
        format : TYPE, optional
            format of the bytes. The default is 'd', wich correspond to double precision floating point.
            See https://docs.python.org/3/library/struct.html#format-characters for more info.
        byte_order : TYPE, optional
            The organization of the bytes (little or bid endian) in the file. The default is '@', wich corresponds to
            'native'.
            See https://docs.python.org/3/library/struct.html#byte-order-size-and-alignment for more info.

        Returns a
        -------
        TimelinedArray / np.ndarray
            A numpy ndarray with tilemine attached (in seconds) correspunding to the data in the binfile.
        """

        from timelined_array import TimelinedArray

        # read file content
        with open(os.path.abspath(self.path), "rb") as f:
            content = f.read()

        # format data as defined in parameters (float, int, etc...)
        bytes_data = []
        for index in range(0, len(content), bytes_size):
            byte = content[index : index + bytes_size]
            bytes_data.append(struct.unpack(byte_order + format, byte)[0])

        # compute the timeline in second based on number of items in the file and data_rate.
        timeline = np.linspace(0, len(bytes_data) / data_rate, num=len(bytes_data))

        return TimelinedArray(bytes_data, timeline=timeline)  # return the data as a TimelinedArray
