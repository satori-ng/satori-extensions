import os

from hooker import hook

__name__ = 'stealthy'

@hook("imager.post_close")
def stealth_open(satori_image, file_path, file_type):

	time_dict = satori_image.get_attribute(file_path, 'times')
	# print ("[>]", file_path, time_dict['atime'], time_dict['mtime'])
	os.utime(
		file_path,
			(
			time_dict['atime'],
			time_dict['mtime'],
			),
		)
	# print ("[*]", file_path, time_dict['atime'], time_dict['mtime'])
