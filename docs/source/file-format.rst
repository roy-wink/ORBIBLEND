ABO files
=========

ORBIBLEND imports files with the ``.abo`` extension.  An ``.abo`` file is a
compact binary file containing one or more frames.  Each frame stores atom data
and zero or more orbital-surface models.

What a frame contains
---------------------

A frame includes:

* a frame index;
* a text description;
* atom entries with atomic number and coordinates;
* model entries for orbital surfaces;
* model color information;
* vertices, normals, and triangular faces for each orbital surface.

How ORBIBLEND reads files
-------------------------

ORBIBLEND uses a two-step loading strategy:

#. During import, it reads only frame descriptions and counts.  This keeps the UI
   responsive even when the file contains dense orbital meshes.
#. When **Create Meshes** is clicked, it reloads the selected frame and reads the
   full vertex, normal, and face arrays for that frame only.

This means the original file path is important.  Do not move or delete the
``.abo`` file between importing it and creating meshes from one of its frames.

Units
-----

The add-on lets you choose **Bohr** or **Angstrom** in the frame panel.  This
choice affects molecule radius scaling and bond detection.  If bonds are missing
or atoms look strangely sized, check the unit setting first.

Sample files
------------

The repository includes sample ``.abo`` files in the ``abo-files`` directory.
They are useful for testing installation, demonstrations, and documentation
examples.
