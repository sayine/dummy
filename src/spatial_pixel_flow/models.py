from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class FaceAdjacencyType(str, Enum):
    COPLANAR = "coplanar"
    CONVEX_CORNER = "convex_corner"
    CONCAVE_CORNER = "concave_corner"


@dataclass(frozen=True)
class VoxelCell:
    position: tuple[int, int, int]
    color_index: int | None = None
    flags: frozenset[str] = frozenset()


@dataclass(frozen=True)
class SurfaceFace:
    face_id: int
    voxel_position: tuple[int, int, int]
    normal: tuple[int, int, int]
    local_face_id: int
    color_state: int | None = None


@dataclass(frozen=True)
class FaceAdjacency:
    source_face_id: int
    target_face_id: int
    adjacency_type: FaceAdjacencyType


@dataclass(frozen=True)
class SurfaceGraph:
    vertices: tuple[SurfaceFace, ...]
    edges: tuple[FaceAdjacency, ...]

    def neighbors(self, face_id: int) -> tuple[int, ...]:
        return tuple(edge.target_face_id for edge in self.edges if edge.source_face_id == face_id)


@dataclass(frozen=True)
class PuzzleDefinition:
    terminals: dict[str, tuple[int, int]]
    allowed_colors: tuple[str, ...]
    ruleset: str
    difficulty: str


@dataclass(frozen=True)
class ValidationReport:
    solvable: bool
    unique: bool
    solve_time_ms: float
    branching_factor: float
    metadata: dict[str, str] = field(default_factory=dict)
