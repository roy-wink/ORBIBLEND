Troubleshooting
===============

The ABO tab is not visible
--------------------------

* Make sure the add-on is enabled in :menuselection:`Edit --> Preferences --> Add-ons`.
* In the 3D viewport, press :kbd:`N` to show the sidebar.
* Look for the ``ABO`` tab on the right side of the viewport.

Import succeeds but no molecule or orbital appears
--------------------------------------------------

Importing only lists the frames.  After selecting a frame, click **Create Meshes**
to create the visible Blender objects.

Create Meshes says no file path is stored
-----------------------------------------

Import the ``.abo`` file again.  ORBIBLEND needs the stored path so it can load
the selected frame on demand.

The molecule looks too large or bonds are missing
------------------------------------------------

Check the **Units** setting in the frame panel.  A Bohr/Angstrom mismatch changes
bond detection and atom radius scaling.

The viewport is slow
--------------------

* Try a smaller ``.abo`` file or a frame with fewer vertices/faces.
* Hide the molecule if you only need the orbital surface.
* Render a still image before attempting an animation.
* Avoid repeatedly creating meshes from very large frames unless necessary.

Rendering an animation takes a long time
----------------------------------------

This is expected.  Animation rendering repeats the render for many frames.  Test
your view with **Render Current Frame** before starting a full animation.

Colors do not look like I expected
----------------------------------

Blender materials use lighting, alpha, and color-management settings.  If the
scientific meaning of the colors matters, use **Edit colors** to choose a clear
positive/negative lobe color pair and include a caption in teaching material.

I accidentally changed the scene
--------------------------------

For most beginner workflows, the safest fix is to press **Delete unnecessary
elements**, then **Camera set-up**, import the ``.abo`` file again, and recreate
the meshes.
