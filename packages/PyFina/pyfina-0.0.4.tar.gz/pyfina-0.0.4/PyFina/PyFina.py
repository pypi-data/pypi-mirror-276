"""pyfina module"""

import struct
import os
import math

import numpy as np

def trim(feed_id, data_dir, limit=100):
    """
    checks and removes anomalies (values above a threshold limit, eg 100)
    feed_id: feed number
    data_dir: feed path (eg /var/opt/emoncms/phpfina)
    limit: threshold we don't want to exceed
    """
    meta = getMeta(feed_id, data_dir)
    pos = 0
    i = 0
    nbn = 0
    with open(f"{data_dir}/{feed_id}.dat", "rb+") as ts:
        while pos <= meta["npoints"]:
            ts.seek(pos*4, 0)
            hexa = ts.read(4)
            aa = bytearray(hexa)
            if len(aa) == 4:
                value = struct.unpack('<f', aa)[0]
                if math.isnan(value):
                    nbn +=1
                elif value > limit:
                    print(f"anomaly detected at {pos} : {value}")
                    i += 1
                    nv = struct.pack('<f', float('nan'))
                    try:
                        ts.seek(pos*4, 0)
                        ts.write(nv)
                    except Exception as e:
                        print(e)
                    finally:
                        print("4 bytes written")
            pos +=1
        print(f"{i} anomaly(ies)")
        print(f"{nbn} nan")

def getMeta(feed_id, data_dir):
    """
    decoding the .meta file
    feed_id (4 bytes, Unsigned integer)
    npoints (4 bytes, Unsigned integer, Legacy : use instead filesize//4 )
    interval (4 bytes, Unsigned integer)
    start_time (4 bytes, Unsigned integer)
    """
    with open(f"{data_dir}/{feed_id}.meta","rb") as f:
        f.seek(8,0)
        hexa = f.read(8)
        aa= bytearray(hexa)
        if len(aa)==8:
            decoded=struct.unpack('<2I', aa)
        else:
            print("corrupted meta - aborting")
            return False
    meta = {
        "interval": decoded[0],
        "start_time": decoded[1],
        "npoints": os.path.getsize(f"{data_dir}/{feed_id}.dat") // 4
    }
    return meta

class PyFina(np.ndarray):
    """ pyfina class."""
    def __new__(cls, feed_id, data_dir, start, step, npts, remove_nan=True):
        meta = getMeta(feed_id, data_dir)
        if not meta:
            return None
        # decoding and sampling the .dat file
        # values are 32 bit floats, stored on 4 bytes
        # to estimate value(time), position in the dat file is calculated as follow :
        # pos = (time - meta["start_time"]) // meta["interval"]
        # Nota : if remove_nan is True and a NAN is detected, the algorithm takes previous value
        obj = np.zeros(npts).view(cls)
        raw_obj = np.empty(npts)

        end = start + (npts-1) * step
        time = start
        i = 0
        nb_nan = 0
        with open(f"{data_dir}/{feed_id}.dat", "rb") as ts:
            while time < end:
                time = start + step * i
                pos = (time - meta["start_time"]) // meta["interval"]
                if 0 <= pos < meta["npoints"]:
                    try:
                        #print(f"trying to find point {i} going to index {pos}")
                        ts.seek(pos*4, 0)
                        hexa = ts.read(4)
                        aa= bytearray(hexa)
                    except Exception as e:
                        print(f"error during file operation {e}")
                    else:
                        if len(aa)==4:
                            value = struct.unpack('<f', aa)[0]
                            obj[i] = value
                            raw_obj[i] = value
                            if remove_nan and np.isnan(value):
                                nb_nan += 1
                                obj[i] = obj[i-1]
                        else:
                            print(f"unpacking problem {i} len is {len(aa)} position is {pos}")
                i += 1
        first_non_nan_value = -1
        first_non_nan_index = -1
        starting_by_nan = np.isnan(raw_obj[0])
        if nb_nan < npts:
            finiteness_obj = np.isfinite(raw_obj)
            first_non_nan_index = np.where(finiteness_obj)[0][0]
            first_non_nan_value = raw_obj[finiteness_obj][0]
            if starting_by_nan and remove_nan:
                obj[:first_non_nan_index] = np.ones(first_non_nan_index) * first_non_nan_value
        # storing the "signature" of the "sampled" feed
        obj.start = start
        obj.step = step
        obj.nb_nan = nb_nan
        obj.first_non_nan_value = first_non_nan_value
        obj.first_non_nan_index = first_non_nan_index
        obj.starting_by_nan = starting_by_nan
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.start = getattr(obj, 'start', None)   # pylint: disable=W0201
        self.step = getattr(obj, 'step', None)  # pylint: disable=W0201

    def timescale(self):
        """
        return the time scale of the feed as a numpy array
        """
        return np.arange(0,self.step*self.shape[0],self.step)
