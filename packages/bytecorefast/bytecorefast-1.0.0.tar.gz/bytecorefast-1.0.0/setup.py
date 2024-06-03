from setuptools import setup, Extension

module = Extension(
    'bytecorefast.fast_emulator',
    sources=[
        'src/bytecorefast/fast_emulator.c',
        'src/emulator.c',
        'src/control_unit.c',
        'src/memory.c'
    ],
    include_dirs=['src']
)

setup(
    ext_modules=[module]
)
