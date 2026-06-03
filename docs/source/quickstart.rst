Quickstart: your first orbital render
=====================================

This tutorial creates a simple still image from an ``.abo`` file.  It assumes
that ORBIBLEND is already installed and enabled.

1. Open Blender
---------------

Start Blender and open the default scene.  It is fine if the default cube is
visible; ORBIBLEND can remove it.

2. Open the ABO tab
-------------------

Press :kbd:`N` to show the right sidebar if needed, then choose the ``ABO`` tab.

3. Prepare the workspace
------------------------

In **Prepare workspace**:

#. Click **Delete unnecessary elements**.
#. Click **Camera set-up**.

The camera setup creates a camera, a sun light, and circular guide paths.  These
objects are placed in a ``Render tools`` collection so they do not get mixed with
the molecule and orbitals.

4. Import an ABO file
---------------------

In **Import .abo file**:

#. Click **Import .abo file**.
#. Choose a file ending in ``.abo``.
#. Confirm the file selection.

After import, ORBIBLEND lists the frames contained in the file.  A frame may be a
single molecule-only view or one molecular orbital with its positive and negative
lobes.

5. Choose what to draw
----------------------

In **.abo frames**:

#. Click the frame you want.
#. Leave **Show Molecule** enabled for a first render.
#. Choose the correct unit, usually **Bohr** for PyQInt-generated files unless
   your source explicitly says the coordinates are in Angstrom.
#. Click **Create Meshes**.

The mesh creation step can take a moment for large orbitals.  ORBIBLEND loads the
selected frame and creates Blender objects for the molecule, bonds, and orbital
surfaces.

6. Adjust the view
------------------

In **tweak view**, try small changes first:

* **X 15°** tilts the molecule/orbitals.
* **Z 15°** rotates them around the vertical axis.
* **Zoom in** and **Zoom out** adjust the camera path scale.
* **Transp. down** and **Transp. up** change orbital transparency.
* **Edit colors** lets you change molecule, bond, and orbital material colors.

For educational figures, prefer simple views where the nodal plane, bonding
region, or antibonding region is easy to see.

7. Render
---------

In **render**:

* Click **Render Current Frame** to make a still image.
* Click **Render Animation** to create a rotating animation.  Blender may take a
  long time to render an animation, so start with a still image first.

Saving your image
-----------------

After a still render opens in Blender's render window, use
:menuselection:`Image --> Save As...` to save the image.
