from __future__ import annotations

import argparse
from pathlib import Path


def import_vox(args: argparse.Namespace) -> int:
    source = Path(args.input)
    if not source.exists():
        raise FileNotFoundError(f"Input file not found: {source}")
    print(f"[import-vox] queued import for {source}")
    return 0


def build_graph(args: argparse.Namespace) -> int:
    source = Path(args.input)
    if not source.exists():
        raise FileNotFoundError(f"Input file not found: {source}")
    print(f"[build-graph] building surface graph from {source}")
    return 0


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="spf3d", description="Spatial Pixel Flow 3D tooling")
    sub = parser.add_subparsers(dest="command", required=True)

    import_cmd = sub.add_parser("import-vox", help="Import a .vox file")
    import_cmd.add_argument("input", help="Path to .vox input")
    import_cmd.set_defaults(func=import_vox)

    graph_cmd = sub.add_parser("build-graph", help="Build a surface graph from a model")
    graph_cmd.add_argument("input", help="Path to model input")
    graph_cmd.set_defaults(func=build_graph)
    return parser


def main() -> int:
    parser = make_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
