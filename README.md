# Fractalify Blender Add-on
This add-on allows you to create [n-flake](https://en.wikipedia.org/wiki/N-flake) like fractals by recursively repeating a selected pattern. It is compatible with Blender 2.93 LTS.

## Table of Contents

- [**Download and installation**](#download-and-installation)
- [**How to use**](#how-to-use)

## Download and Installation
1. Download the add-on:

|Version|Blender Version|Download URL|
|---|---|---|
|v1.0 |[Blender 2.93](https://www.blender.org/download/releases/2-93/)|[Download](https://github.com/DaraJKong/Fractalify/releases/tag/v1.0)|

The simplest method is to download directly the .zip file containing \__init__.py, not the entire repository as a .zip file. The reason is you need to have the correct add-on structure for it to install properly into Blender.

2. Open the User Preferences in Blender (Edit > Preferences...). In the "Add-ons" tab, click on the "Install..." button. Then find the .zip file you downloaded and select it. The add-on should now appear in the window.
<img src="https://github.com/DaraJKong/Fractalify/blob/4bafc4a4c14ef315d55df9bbb3410e553ab99054/docs/BlenderUserPreferences.png" width="700" alt="User Preferences">

3. Tick the checkbox next to the name of the add-on. If the add-on did not appear in the list, just search for "Fractalify" in the input field. If you do not have the "Auto-Save Preferences" option enabled, save the user preferences. This will ensure the add-on gets loaded everytime you open Blender.
<img src="https://github.com/DaraJKong/Fractalify/blob/4bafc4a4c14ef315d55df9bbb3410e553ab99054/docs/BlenderEnableAddon.png" width="700" alt="Enable Addon">

4. Find the add-on in the right side panel of the 3D Viewport. You can open that panel by pressing the N key.

## How to Use

Once the addon is installed, you will find it in many places. The best is to open the right side panel (N). There you will find a tab named "Fractalify" with a user-friendly interface. You can also access the add-on under "Object > Quick Effects > Fractalify" in the 3D Viewport. Once you use the operator, the redo panel will let you tweak the settings of the last fractalization.

<img src="https://github.com/DaraJKong/Fractalify/blob/d6a403c14193a9e3ef851955d3e1ba220077f452/docs/HowToFindAddon.png" width="700" alt="Find Addon">

To create a fractal, you will first need a pattern. A pattern consists simply of duplicated objects. One of the objects in the pattern is the source object. It can be any of the objects, but as a rule of thumb, the biggest object in the pattern is generally the source one.
Once you created a pattern, select all of the objects in it (orange outline). Make sure the source object is active (yellow outline). Then click on "Fractalify Selection" in the panel. This add-on will automatically detect the pattern and repeat it recursively. Instead of repeating the operation multiple times, you can increase the number of iterations. This will repeat the operation for you. The benefit of this is it's quicker to undo.

The option "Include Source" is harder to understand than the number of recursions. If this option is enabled, Fractalify will use the active object in the pattern. This will make it so that every step of the pattern is conserved. However, if the source is excluded, only the last iteration of the fractal will be kept. Generally you want to include the source when adding geometry. In the case you want to remove geometry (cut the original object in smaller ones), you need to exclude the source. For example, in the [Sierpiński triangle](https://en.wikipedia.org/wiki/Sierpi%C5%84ski_triangle), the source triangle is replaced with three smaller ones. In that case, the source triangle needs to not be included.
