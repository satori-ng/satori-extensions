import binascii
import hashlib

from hooker import hook

__name__ = 'sha160'

@hook("with_open")
def hash_file(satori_image, file_path, file_type, fd):
    fd.seek(0)
    hash_obj = hashlib.new(__name__)

    n_chunk = 1024**2
    bytechunk = fd.read(n_chunk)
    while bytechunk:
        hash_obj.update(bytechunk)
        bytechunk = fd.read(n_chunk)
    
    hex_digest = hash_obj.hexdigest()
    satori_image.set_attribute(file_path, hex_digest, __name__, force_create=True)
