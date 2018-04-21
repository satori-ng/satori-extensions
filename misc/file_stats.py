import os.path
from hooker import hook

STATS_DICT = {
	'files':0,
	'dirs':0,
	'links':0,
}

__name__='file_stats'


@hook('pre_open')
def record_stats(satori_image, file_path, file_type):

	if os.path.isfile(file_path) :
		STATS_DICT['files'] += 1
		return
	if os.path.isdir(file_path) :
		STATS_DICT['dirs'] += 1
		return
	if os.path.islink(file_path) :
		STATS_DICT['links'] += 1
		return
	
	
@hook('on_end')
def present_stats():

	import pprint
	pprint.pprint(STATS_DICT)