# ORBIBLEND


## Purpose

This is an add-on for blender to visualize molecules and their molecular orbitals. The add-on is capable of importing externally generated .abo files. Without any understanding of Blender, the user can set-up the necessary settings in Blender, import the molecule, selected the wanted MO, tweak the view, and render an image or animation. All from the comfort of a single UI.

If the user has a deeper understanding of Blender, other tweaks can be made as wished.

This add-on is made for and tested on Blender version 4.2.5 LTS, running Python 3.11.7 (distributed with this specific Blender version).

## Status

Work in progress. 

Already implemented:
- Workspace preparation and camera set-up (mostly copied over from IMOR).
- Import function and script for swiftly reading in the binary file.
- Custom, rigid data structuring by means of custom collection properties. This is seamlessly integrated into Blender's UI, and therefore also stored in .blend files if the user wishes to come back to the project later.
- Unambiguous visualization of the frames present in the loaded file in the UI.
- Data validation without breaking errors.
- Rendering of chosen MO by a click-of-the-button, using Blender native functions.
- Coloring the MO's by the color provided in the .abo file
- A checkbox to decide whether the user wants to create the molecule meshes
- Rendering the molecule by the user's discretion. possible pitfalls are how big to draw the atoms and what color to give them, and between what atoms to draw a bond. The user does need to specify the unit (Bohr/Angstrom) in order for the molecule to be drawn correctly.
- Tweaking the view, e.g. zooming in/out; tilting the molecule/MO's; rotating the molecule/MO's.
- Rendering an image or animation.

As present, the script is finished and operable. Cosmetic changes are still in the pipeline, as well as even more robust monkey proofing. 


## Usage.

Download the abo-addon folder, and place the entire (unpacked) folder in %APPDATA%\Blender Foundation\Blender\4.2\scripts\addons

In Blender, go to Edit > Preferences > Add-ons, and check `ABO BLENDER RENDER`. A new menu called `ABO` appears at the right-hand side of the 3D workspace. You might need to press the tiny `<` next to the coordinate system.

The add-on works best when the buttons are pressed from top to bottom. However, the add-on should not break when buttons are pressed in a different order or repeatedly. Please let me know if this is the case. 
