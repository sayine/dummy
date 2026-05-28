from spatial_pixel_flow.models import FaceAdjacency, FaceAdjacencyType, SurfaceFace, SurfaceGraph


def test_surface_graph_neighbors_returns_outgoing_face_ids() -> None:
    graph = SurfaceGraph(
        vertices=(
            SurfaceFace(face_id=1, voxel_position=(0, 0, 0), normal=(1, 0, 0), local_face_id=0),
            SurfaceFace(face_id=2, voxel_position=(1, 0, 0), normal=(1, 0, 0), local_face_id=0),
        ),
        edges=(
            FaceAdjacency(source_face_id=1, target_face_id=2, adjacency_type=FaceAdjacencyType.COPLANAR),
        ),
    )

    assert graph.neighbors(1) == (2,)
    assert graph.neighbors(2) == ()
