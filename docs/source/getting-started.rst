Getting started
===============

This page helps you install ORBIBLEND and find the add-on inside Blender.  It is
written for users who have little or no Blender experience.

What you need
-------------

* A recent Blender installation.  ORBIBLEND is developed for Blender 4.x; the
  add-on metadata currently targets Blender 4.5 and Python 3.11.
* The ``abo-addon`` folder from this repository.
* One or more ``.abo`` files, for example the sample files in ``abo-files``.

Blender words used in this guide
--------------------------------

Blender has its own vocabulary.  These terms are enough to get started:

``Viewport``
   The large 3D area where the molecule and orbitals appear.

``Sidebar``
   A panel on the right side of the 3D viewport.  Press :kbd:`N` if it is hidden.

``Add-on``
   A package that adds extra tools to Blender.  ORBIBLEND is an add-on.

``Collection``
   A folder-like group of objects in Blender.  ORBIBLEND creates collections
   called ``Molecule``, ``Bonds``, ``Orbitals``, and ``Render tools``.

Installing the add-on
---------------------

#. Close Blender if it is already running.
#. Copy the entire ``abo-addon`` folder into Blender's add-ons directory.

   On Windows this is typically::

      %APPDATA%\Blender Foundation\Blender\4.x\scripts\addons

   On macOS this is typically::

      ~/Library/Application Support/Blender/4.x/scripts/addons

   On Linux this is typically::

      ~/.config/blender/4.x/scripts/addons

   Replace ``4.x`` with your Blender version folder, such as ``4.2`` or ``4.5``.

#. Start Blender.
#. Open :menuselection:`Edit --> Preferences --> Add-ons`.
#. Search for ``ORBIBLEND``.
#. Enable the check box next to the add-on.
#. Close the Preferences window.

Finding the ABO sidebar
-----------------------

#. Return to the main Blender window.
#. Make sure you are in the 3D viewport.
#. Press :kbd:`N` if the right sidebar is hidden.
#. Click the ``ABO`` tab in the sidebar.

You should now see panels for preparing the workspace, importing an ``.abo``
file, choosing frames, tweaking the view, and rendering.

Recommended first setup
-----------------------

For a first run, use the buttons from top to bottom:

#. Click **Delete unnecessary elements** to clear default scene objects that can
   distract from the molecule.
#. Click **Camera set-up** to create a camera, lighting, and animation path.
#. Click **Import .abo file** and select a sample file.
#. Select a frame and click **Create Meshes**.
#. Use the tweak controls if needed.
#. Render a still image or animation.

You do not need to understand Blender's object hierarchy to follow this order.
ORBIBLEND creates and organizes the required objects for you.
