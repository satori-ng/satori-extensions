import sys

import hooker

from satoricore.common import _STANDARD_EXT
from satoricore.logger import ext_logger
from satoricore.image.filesystem import _CONTENTS_S


__name__ = 'text'
default_enc = sys.getdefaultencoding()

@hooker.hook('imager.with_open', 'mime')
def store_text(satori_image, file_path, file_type, fd):
	if file_type != _STANDARD_EXT.FILE_T and file_type != _STANDARD_EXT.UNKNOWN_T:
		ext_logger.info("File '{}:{}' is not Regular file"
			.format(
					file_type,
					file_path
				)
			)
		return None
	try:
		ftype = satori_image.get_attribute(file_path, 'mime')

	except Exception as e:
		ext_logger.info("{}. File Type of '{}' is '{}'."
			.format(
					e,
					file_path,
					ftype,
				)
			)

	if 'text' not in ftype: return None

	fd.seek(0)
	content = fd.read()
	content = str(content, default_enc)

	try:
		satori_image.set_attribute(file_path, content, _CONTENTS_S, force_create=False)
	except Exception as e:
		ext_logger.warn(e)



@hooker.hook('fuse.on_read')
def read_text(satori_image, file_path, length, offset, fh, value):

	contents = satori_image.get_attribute(file_path, _CONTENTS_S)
	if not isinstance(contents, str):
		ret = ""
		return

	if offset <= len(contents) <= length + offset:
		ret = contents[offset:length+offset]

	value['return'] = ret
	return value['return']
