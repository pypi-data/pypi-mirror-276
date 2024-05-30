CHANGELOG
=========

0.4.0 - 2024-05-30
------------------

* First release to PyPI
* The code has been ported from PQt6 to PySide6
* Bugs fixed / Added features
  - The timeline can be zoomed/dezoomed
  - Annotation creation can be aborted
  - Annotation data can be saved in a CSV file
  - The configuration is now in YAML format and can store several annotation label definitions

0.3.7 - 2024-05-28
------------------

Depend on PySide6

0.3.6 - 2024-05-28
------------------

Add dependency on PyQt6-Qt6

0.3.5 - 2024-05-28
------------------

Force dependency on PyQt6 == 6.4

0.3.4 - 2024-05-23
------------------

Use GitLab CI and AutoPub for automatic publication of the package

0.3.3 - 2024-05-23
------------------

* First release to test.pypi.org
* The timeline is now implemented with QGraphics* objects
* Annotations are now clickable

0.2 - 2024-04-30
----------------

* Fix video playing issues
* The timeline is now functional and it is possible to add annotations

0.1 - 2024-03-25
----------------

Initial release, containing a very simple interface that allows loading a video file and playing it. A timeline is show but is not yet functional.
