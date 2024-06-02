import zipfile
import io
import os
import numpy as np
import json
import time

##################
# CONSTANTS
##################
FULL_NAME = "full_name"
TIMESTAMP = "timestamp"
BYTES = "bytes"
NPY = "npy"
JSON = "json"


class Archive:
    """This is a derivative of the 'resultserializer' file format that's compatible with
    the visualization tools provides by Pairtree. This class is used to compress numpy data
    into an npz file type"""

    def __init__(self, fn):
        """
        Parameters
        ----------
        fn : str
            File name to save all Archive information to. This should have a '.npz' extension.

        Returns
        -------
        None
        """
        self._fn = fn
        self._to_add = {}
        self._compress_type = zipfile.ZIP_LZMA

        if self._file_exists():
            with self._open() as F:
                self._names = set([self._resolve_name(fullname) for fullname in F.namelist()])
        else:
            self._names = set()

    def _resolve_name(self, fullname):
        return fullname.rsplit('.', 1)[0]

    def _file_exists(self):
        return os.path.exists(self._fn)

    def _open(self, mode='r'):
        """Opens Archive file type"""
        assert mode in ('r', 'w'), "Incorrect mode to open results file in (%s)" % mode
        return zipfile.ZipFile(self._fn, mode, compression=self._compress_type,)

    def has(self, name):
        """Checks if the archive has a particular key value
        
        Parameters
        ----------
        name : str
            The key to check for in the archive

        Returns
        -------
        bool
            Returns True is the key exists in the archive, false otherwise
        """
        return name in self._names

    def save(self):
        """Saves all of the elements in the 'to_add' dictionary without overwriting 
        any existing information"""
        # if the file already exists, only write key, value pairs that don't already exist
        if self._file_exists():
            with self._open() as F:
                for zi in F.infolist():
                    fullname = zi.filename
                    name = self._resolve_name(fullname)
                    if name in self._to_add:
                        continue
                    with F.open(zi) as G:
                        self._to_add[name] = {
                            FULL_NAME: fullname,
                            BYTES: G.read(),
                            TIMESTAMP: zi.date_time,
                        }

        with self._open('w') as F:
            for name, data in self._to_add.items():
                zi = zipfile.ZipInfo(
                    filename=data[FULL_NAME],
                    date_time=data[TIMESTAMP],
                )
                F.writestr(zi, data[BYTES], compress_type=self._compress_type)

        self._to_add = {}

    def add(self, name, data):
        """Adds key, value pair to the archive
        
        Parameters
        ----------
        name : str
            The key to store the data under in the archive
        data : object
            The data to store in the archive (np.ndarray, list, np.int32, etc.)
        
        Return
        ------
        None
        """
        if isinstance(data, np.ndarray):
            output = io.BytesIO()
            np.save(output, data)
            output = output.getvalue()
            data_type = NPY
        else:
            output = (json.dumps(data) + '\n').encode('utf-8')
            data_type = JSON

        self._to_add[name] = {
            FULL_NAME: '%s.%s' % (name, data_type),
            TIMESTAMP: time.localtime(time.time()),
            BYTES: output,
        }
        self._names.add(name)

    def _load(self, full_name, data_type, F):
        """Loads the archive to allow for values to be extracted"""
        data = F.read(full_name)
        if data_type == NPY:
            bio = io.BytesIO(data)
            return np.load(bio, allow_pickle=False)
        elif data_type == JSON:
            return json.loads(data.decode('utf-8'))
        else:
            raise Exception('Unknown data type: %s' % data_type)

    def get(self, name):
        """Gets the value associated with a particular key in the archive
        
        Parameters
        ----------
        name : str 
            A key to extract from the archive
        
        Returns
        -------
        object
            the data associated with the name input
        """
        with self._open() as F:
            present = set(F.namelist())
            for data_type in (NPY, JSON):
                full_name = '%s.%s' % (name, data_type)
                if full_name in present:
                    return self._load(full_name, data_type, F)
            raise Exception(f'{name} is not present in {self._fn}')
         
    def get_mutrel(self, _):
        """This is an empty function for compatibility"""
        return []