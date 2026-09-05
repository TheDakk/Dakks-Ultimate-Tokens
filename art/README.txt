This is the library itself: art/<kind>/<slug>.webp

Universal is complete (1408 files) and closed as of 2026-09-04. Nothing is saved here by
hand: every file is written by import_builtin_image.py from a keyed capture, under the
exact build_filename its queue row names. The filename is what wires it into Foundry, so
it cannot be renamed. aliases.json maps an alias slug to a canonical slug (no chains).

Then, from the suite repo (C:\Projects\FoundryVTT\DnD2E):
  npm run art-check     verify the library
  npm run build         with Foundry closed

Full procedure: ../upload/README-UPLOAD.md
