This is the library itself: art/<kind>/<slug>.webp

Save each generated image under the exact build_filename its queue row names — the
filename is what wires it into Foundry, so it cannot be renamed.

Then, from the suite repo (C:ProjectsFoundryVTTDnD2E):
  npm run art-check     verify what you saved
  npm run build         with Foundry closed

Full procedure: ../upload/README-UPLOAD.md
