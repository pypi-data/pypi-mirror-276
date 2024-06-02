import sys
from . import Effect

if __name__ == '__main__':
    lib = sys.argv[1]
    effect = Effect(lib)
    print('Stratus effect library {}:'.format(lib))
    print('  Effect name:....... {}'.format(effect.name))
    print('  Effect ID:......... {}'.format(effect.effectId))
    print('  Effect version:.... {}'.format(effect.version))
    print('  Number of knobs:... {}'.format(effect.knobCount))
    print('  Number of switches: {}'.format(effect.switchCount))
