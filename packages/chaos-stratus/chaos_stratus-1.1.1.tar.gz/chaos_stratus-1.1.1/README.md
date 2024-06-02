
# chaos-stratus

This package provides tools for interacting with (appropriately compiled) [Chaos Audio Stratus pedal](https://chaosaudio.com/) effects libraries. 

By "appropriately compiled" we mean built with the Stratus build tools available with the most recent versions of [Faust](https://faust.grame.fr/), 
or with the [Faust IDE](https://faustide.grame.fr/).

Effects that are _not_ built with the Faust tools (e.g. those built before those tools became available) are still at least _partially_ compatible
with the library - they may not provide the documented class attributes, but they will provide the operational functions that allow you
to interact with them.

In _all_ cases, though, the effect must be built for the platform upon which this class is used - that means performing a "local" build with the
Faust tools (or by some other means) or installing this package on the Stratus pedal itself.

# LATEST NEWS
## version 1.1.0
The package now supports effects not built with the Faust tools.
The package now requires Python 3.8 as a minimum

# Installation

You can install this package using a standard `pip` invocation


```
python -m pip install chaos-stratus
```
# Usage/Examples

The main class of these tools is `Effect`.

You include that into your python script in the standard manner:

```python
from chaos_stratus import Effect
```

You instantiate the class for a specific effect library as follows:

```python
effect = Effect("path/to/my/effect.so")
```

See the module documentation for the API available to you.

## Examples

### Reporting on information concerning the library

```python
import sys
from chaos_stratus import Effect

lib = sys.argv[1]
effect = Effect(lib)
print(f'Stratus effect library {lib}:')
print(f'  Effect name:....... {effect.name}')
print(f'  Effect ID:......... {effect.effectId}')
print(f'  Effect version:.... {effect.version}')
print(f'  Number of knobs:... {effect.knobCount}')
print(f'  Number of switches: {effect.switchCount}')

```

This is, in fact, what is implemented by the command:

```sh
python -m chaos_stratus "path/to/my/effect.so"
```

### Applying the effect on raw sample data

Possibly the most interesting thing you can do with the tools is to apply the
effect to test sample data, with different knob and switch values, and check that
the output is what you expected.

This is how you can do that with raw sample from `stdin`, sending output to `stdout`:

```python
import sys
from chaos_stratus import Effect

lib = sys.argv[1]
effect = Effect(lib)

#
# Set knobs/switches to desired values
#
effect.setKnob(1, 0.5)

#
# Run the effect on stdin
#
BUFFERSIZE=8192
DATA_IN=sys.stdin.buffer
DATA_OUT=sys.stdout.buffer
input_buffer=bytearray(BUFFERSIZE)
while True:
    insize = DATA_IN.readinto(input_buffer)
    if insize == 0:
        break
    DATA_OUT.write(effect.computeBuf(input_buffer[:insize]))
```

To use that with, say, a `wav` input file and pump the output to the default output device of your computer (say, your headphones)

* install [sox](https://sourceforge.net/projects/sox/)
* write a Python script based on the above sample code
* Find a suitable `wav` file (or any other format that Sox supports out of the box)
* Run it all like this from the (shell) command line:

```sh
sox your-sounds.wav -b32 -e floating-point -r 44100 -t raw - | \
    python my-effect-script.py path/to/my/effect.so | \
    sox -b32 -e floating-point -r 44100 -t raw - -d
```

Add more effects to your pipeline at will :).
