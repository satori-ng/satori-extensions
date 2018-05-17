# satori-extensions
Extensions for the Satori-NG Suite 

The *Satori Extensions* are the main way to extend the *Satori Suite's* functionalities. It uses [`hooker`](https://github.com/satori-ng/hooker), a standalone Python Package (available with `pip`) to add functions in *events* declared in the *Satori Suite* components.

Each extension is responsible to *gather*, *store*, *compare*, and even provide a way to *visualize* a single aspect of an Operating System instance.


## Declared Events

In both [*Satori-ng Imager*](https://github.com/satori-ng/satori-imager) and [*Satori-ng Differ*](https://github.com/satori-ng/satori-differ), there have been declared 5 `hooker` events.

For [**Satori-ng Imager**](https://github.com/satori-ng/satori-imager) they are:
* `imager.on_start` - Executes when the *Satori-Imager* starts the OS imaging process
* `imager.pre_open` - Executes before a file is `open`'d using the `open` OS syscall
* `imager.with_open` - Executes when the file is opened, the *File Descriptor* of the file is available
* `imager.post_close` - Executes when the file is closed using `close` OS syscall
* `imager.on_end` - Finally, executes when the Imaging process finishes

For [**Satori-ng Differ**](https://github.com/satori-ng/satori-differ) they hold the same name with `differ` instead of `imager` (e.g `differ.on_start`, etc)

  
  
## Dissecting the `entropy` extension

The *entropy* extension code for the *Imager hook* is the following:

```python
from entropy import shannon_entropy # Python dependency, available with PyPI
from hooker import hook # The hooker package
__name__ = 'shannon'  # Name of the extension

@hook("imager.with_open") # When the file is opened
def calculate(satori_image, file_path, file_type, fd):
    '''
    This argument list is declared for the "imager.with_open" calls.
    All functions hooked for "imager.with_open" must have the same argument list
    
    satori_image: The image object where everything is stored
    file_path: The full path of the opened file
    file_type: The file type as returned from a 'stat' call
    fd: The file descriptor of the opened file
    '''
    
    fd.seek(0)  # Return to the beginning of the file
    e = shannon_entropy(fd.read())  # Read the contents and calculate the entropy - uses the 'entropy' external package
    # set a key named 'entropy' in the file's image, storing the entropy value 'e' in it
    satori_image.set_attribute(file_path, str(e), __name__, force_create=True)
```

## Non-data extensions

The `stealthy` extension does not gather data. It just uses `os.utime` call to perform naive [`timestomping`](http://www.forensicswiki.org/wiki/Timestomp) (Reset Access Time to previous values) on the files opened by the `Imager`


## Non-file extensions

What about reading and storing the `iptables` rules of the Linux OS that is *Image*'d?
No files are opened (as a single `iptables-save` command has all useful information).

This could be implemented using the `imager.on_start` event hook:


```python
from hooker import hook
from satoricore.image import _DATA_SECTION

def iptables_save(parser, args, satori_image):
  # Run the 'iptables-save' command and get the output
  proc = subprocess.Popen(['iptables-save'])
  outs, errs = proc.communicate()
  
  # Create a new 'class' in the image to store the iptables result
  satori_image.add_class(
      "iptables",
      section=_DATA_SECTION,
      data=outs,
  )
```





