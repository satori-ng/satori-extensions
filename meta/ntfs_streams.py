# -*- coding: utf-8 -*-

from hooker import hook
from satoricore.logger import ext_logger

__name__ = 'ntfs-streams'

@hook("imager.pre_open")
def find_streams(satori_image, file_path, file_type, os_context):

    if file_type is 'U' or file_type is 'F':

        if '"' in file_path:
            ext_logger.info("File path {} is not a valid NTFS path".format(file_path))
            return

        command = "dir \"{}\" /r".format(file_path)
        stdout = os_context.popen(command).read()

        stream_dict = parse_cmd(stdout)

        satori_image.set_attribute(file_path, stream_dict, __name__, force_create=True)

def parse_cmd(stdout):

    lines = stdout.splitlines()[5:-2]

    ret = {}
    for row in lines:
        try:
            filename = row.split()[-1]
        except IndexError:
            continue

        if ":" not in filename:
            continue
        fname, alt_stream, stream_type = filename.split(":")
        ret[alt_stream] = stream_type

    return ret
