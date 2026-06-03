Common workflows
================

The recipes below are written for classroom and lab use.  They keep the Blender
steps minimal and focus on producing clear educational visuals.

Create a still image for a worksheet
------------------------------------

#. Prepare the workspace.
#. Import the desired ``.abo`` file.
#. Select the orbital frame that supports the concept you want to discuss.
#. Enable **Show Molecule** so students can relate the orbital to the nuclei.
#. Click **Create Meshes**.
#. Use 15-degree rotations until the important feature is visible.
#. Reduce opacity slightly if atoms are hidden inside the orbital.
#. Render the current frame and save the image.

Teaching tip: for beginner students, include the molecule and use a view that
makes symmetry obvious.  Avoid dramatic camera angles when the goal is to compare
bonding and antibonding orbitals.

Create a rotating animation
---------------------------

#. Follow the still-image workflow first.
#. Confirm that the still render looks good.
#. Click **Render Animation**.
#. Wait for Blender to finish rendering.

Animations can take a long time.  For a first classroom test, use a small sample
file and render a short preview by reducing Blender's frame range before starting
the full render.

Show only the molecule
----------------------

Some ``.abo`` files include frames that contain atom data but no orbital models.
When such a frame is selected, ORBIBLEND automatically keeps **Show Molecule**
enabled.  Choose the molecule-only frame and click **Create Meshes**.

If the selected frame contains orbital models, **Create Meshes** will draw those
orbital surfaces.  In that case, choose a different frame or prepare a separate
``.abo`` file when you need a molecule-only figure.

Compare multiple orbitals
-------------------------

#. Import one ``.abo`` file.
#. Select the first frame and create meshes.
#. Render or save the view.
#. Select the next frame and click **Create Meshes** again.
#. Repeat with the same camera setup and similar rotations.

Keeping the camera setup and rotations consistent makes visual comparisons easier
for students.

Change colors for accessibility
-------------------------------

#. Create the meshes.
#. Click **Edit colors**.
#. Change orbital lobe colors to a high-contrast pair.
#. Click **Confirm**.
#. Render the image.

Use colors that remain distinguishable when printed in grayscale if the material
will be used in handouts.
