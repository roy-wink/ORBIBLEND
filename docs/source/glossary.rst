Glossary
========

``.abo file``
   Binary file imported by ORBIBLEND.  It stores atom coordinates and orbital
   surface mesh data.

Atom
   A sphere representing a nucleus/element in the molecule.

Bond
   A cylinder drawn between atoms when the distance is within ORBIBLEND's bond
   detection thresholds.

Bohr
   Atomic unit of length often used in quantum chemistry.

Angstrom
   Common chemistry unit of length, equal to ``10^-10`` meters.

Frame
   One entry inside an ``.abo`` file.  A frame may contain a molecule, one or
   more orbital-surface models, and a description.

Isosurface
   A surface showing where an orbital has a constant value.  Molecular orbitals
   are often visualized as positive and negative isosurfaces.

Lobe
   One connected part of an orbital isosurface.  ORBIBLEND may name two-model
   orbitals as positive and negative lobes.

Material
   Blender settings for object color, transparency, and surface appearance.

Mesh
   A Blender object made from vertices and faces.  ORBIBLEND converts orbital
   isosurfaces into meshes.

Molecular orbital
   A wavefunction describing electron distribution over a molecule.  ORBIBLEND
   visualizes orbital shapes; it does not calculate the orbital itself.

Nodal plane
   A plane where the orbital changes sign and the orbital value is zero.

Render
   The process of turning the Blender scene into a final image or animation.

Viewport
   The interactive 3D area in Blender.
