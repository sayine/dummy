# dummy

Initial development scaffold for **Spatial Pixel Flow 3D**.

## Implemented from the plan
- Core data models for voxel/surface/puzzle/validation entities.
- First-pass CLI with `import-vox` and `build-graph` command stubs.
- Basic unit test coverage for `SurfaceGraph` neighbor traversal.

## Run locally
```bash
PYTHONPATH=src python -m spatial_pixel_flow.cli --help
PYTHONPATH=src pytest -q
```
