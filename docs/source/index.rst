ORBIBLEND: Molecular orbital visualization in Blender
=====================================================

.. image:: ../img/orbiblend_logo.png
   :alt: ORBIBLEND logo
   :align: center
   :width: 280px

**ORBIBLEND** is a Blender add-on for quickly visualizing molecules and
molecular orbitals from ``.abo`` files.  It is designed for classroom and
self-study settings: the main workflow lives in one Blender sidebar tab, and
this documentation assumes that you may be opening Blender for the first time.

The add-on connects quantum-chemistry output to Blender's rendering tools.  An
``.abo`` file stores atom positions and tessellated orbital isosurfaces; ORBIBLEND
lets you import those frames, choose the orbital or molecule view that you want,
adjust the camera, and render still images or rotating animations.

Start here
----------

If you are new to ORBIBLEND, read these pages in order:

#. :doc:`getting-started` explains installation and how to find the ABO sidebar.
#. :doc:`quickstart` walks through creating your first molecular-orbital render.
#. :doc:`interface` explains every panel and button in the add-on.
#. :doc:`workflow` gives practical step-by-step recipes for common classroom tasks.

Educational focus
-----------------

ORBIBLEND aims to help students build intuition about molecular orbitals rather
than to hide the chemistry behind a photorealistic image.  The documentation
therefore explains Blender vocabulary, suggests safe default settings, and points
out where visual choices can change how an orbital is perceived.

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: User guide

   getting-started
   quickstart
   interface
   workflow
   educational-use
   file-format
   troubleshooting
   glossary
