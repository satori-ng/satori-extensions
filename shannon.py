from entropy import shannon_entropy

from hooker import hook

__name__ = 'shannon'


@hook("with_open")
def calculate(satori_image, file_path, file_type, fd):
    fd.seek(0)
    e = shannon_entropy(fd.read())
    satori_image.set_attribute(file_path, str(e), __name__, force_create=True)
