Interface guide
===============

ORBIBLEND places its workflow in the ``ABO`` tab of Blender's 3D viewport
sidebar.  The panels are intended to be used from top to bottom, but most buttons
can be pressed repeatedly without damaging the scene.

Prepare workspace
-----------------

**Delete unnecessary elements**
   Selects and removes scene objects that are not part of ORBIBLEND's render
   setup.  Camera, camera path, sun light, and light path are preserved when
   present.

**Camera set-up**
   Creates or updates the camera, lighting, animation paths, render engine,
   render resolution, and animation frame range.  It also switches the viewport
   to camera view when possible.

Import .abo file
----------------

**Import .abo file** opens a file picker for ``.abo`` files.  Importing a file
clears previous ORBIBLEND molecule, bond, and orbital objects.  The add-on reads
lightweight frame metadata first, so importing large files should remain
responsive.

.abo frames
-----------

This panel appears after a file has been imported.

Frame list
   Shows all frames found in the ``.abo`` file.  The first line of each frame
   description is shown in the list.

Additional Description
   Displays extra description lines for the selected frame, if present.

Show Molecule
   Controls whether atoms and bonds are created together with orbital surfaces.
   If a frame has no orbital models, this option is forced on so that molecule-only
   frames still display something useful.

Units
   Chooses whether coordinates should be treated as ``Bohr`` or ``Angstrom`` for
   molecule radii and bond detection.  A wrong unit can make atoms look too large
   or prevent bonds from being drawn correctly.

Create Meshes
   Loads the selected frame from the stored ``.abo`` file and creates the Blender
   objects.  This is the step where large orbital meshes are actually loaded.

Tweak view
----------

This panel appears after meshes exist.

X rotation buttons
   Tilt the molecule, bonds, and orbitals around the X axis.

Z rotation buttons
   Rotate the molecule, bonds, and orbitals around the Z axis.

Transparency buttons
   Increase or decrease orbital transparency.  Transparency is useful for seeing
   atoms inside an orbital lobe.

Zoom buttons
   Move the camera closer or farther away by scaling the camera path.

Edit colors
   Shows inline color controls for ORBIBLEND materials.  Use **Confirm** to apply
   the edited colors or **Cancel** to restore the previous colors.

Render
------

This panel appears after meshes exist.

Render Current Frame
   Starts a still render using Blender's current render settings.

Render Animation
   Opens a confirmation dialog and then renders the animation.  The default setup
   uses a 360-frame camera/light path, so animation rendering is much slower than
   a still image.
