"""""" # start delvewheel patch
def _delvewheel_patch_1_6_0():
    import os
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'giotto_tda.libs'))
    if os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_6_0()
del _delvewheel_patch_1_6_0
# end delvewheel patch

from ._version import __version__

__all__ = [
    'mapper',
    'time_series',
    'graphs',
    'images',
    'point_clouds',
    'homology',
    'diagrams',
    'curves',
    'plotting',
    'externals',
    'utils',
    'metaestimators',
    'local_homology',
    '__version__'
    ]
