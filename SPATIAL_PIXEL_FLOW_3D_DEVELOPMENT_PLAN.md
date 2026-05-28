# Spatial Pixel Flow 3D — Development Plan

## 1) Product Goals and Success Criteria

### Vision
Deliver a polished mobile 3D puzzle experience that merges:
- **Mode A (Connectivity):** deterministic topological path-connection puzzles on voxel surfaces.
- **Mode B (Sorting):** real-time conveyor-based color-sorting action loops.

### North-Star KPIs
- D1 retention: **>= 35%**
- D7 retention: **>= 12%**
- Puzzle completion rate (first 20 levels): **70–85%**
- Crash-free sessions: **>= 99.5%**
- Median frame rate on target mid-tier device: **>= 60 FPS**
- Median battery drain in 20-min session: **<= 8%**

### Quality Gates
- Every shipped Mode A puzzle is **solvable and uniqueness-verified**.
- Input latency (touch-down to visual response): **< 50 ms**.
- No blocker visual artifacts on 90° corner path transitions.

---

## 2) Scope Definition (MVP vs Post-Launch)

### MVP (Launch Scope)
1. `.vox` ingestion with validated puzzle-model import.
2. Surface graph extraction supporting coplanar, convex, and concave transitions.
3. Mode A core gameplay loop (terminals, paths, 100% coverage validation).
4. Mode B core gameplay loop (conveyor feed, queue, clear condition).
5. Solver stack:
   - Runtime: AC-3 backtracking validator.
   - Offline: SAT/MIP uniqueness checks for content pipeline.
6. 120–200 curated/procedurally validated levels.
7. Mobile rendering optimization: greedy meshing + instancing + lightweight post FX.
8. Basic economy: rewarded hints, no-ads IAP, daily challenge.
9. Analytics, crash reporting, remote config.

### Post-Launch (90-Day Roadmap)
- Seasonal event pass and cosmetic trails/palettes.
- Advanced topology packs (higher genus surfaces).
- Social/leaderboard challenge ladders.
- A/B tested onboarding variants.

---

## 3) Workstreams and Ownership

1. **Gameplay Systems**
   - Core rules engine for both modes.
   - Touch handling, camera orbit, and path state machine.
2. **Content Pipeline**
   - `.vox` import, graph generation, level metadata format.
   - Procedural generation with solver-backed validation.
3. **Solver & Verification**
   - Runtime hint/validation engine.
   - Offline uniqueness and solvability certification.
4. **Rendering & Performance**
   - Greedy mesh generation, path mesh extrusion, shader corner smoothing.
   - Mobile device profiling and optimization pass.
5. **UX/UI & Feedback**
   - Tutorial, progression map, haptics, particles, accessibility.
6. **LiveOps & Monetization**
   - Economy tuning, ad/IAP integration, challenge cadence.
7. **Data/Analytics/QA**
   - Event schema, dashboards, automated testing, device matrix.

---

## 4) Milestone Plan (8 Months)

## Phase 1 (Months 1–2): Asset Ingestion + Graph Assembly

### Deliverables
- `.vox` parser (build-time + runtime modes).
- Coordinate alignment policy (`CENTER_MODEL`, `CORNER_ALIGNED`) with default to corner-aligned for puzzles.
- Exposed-face extraction and immutable `SurfaceGraph` representation.
- Adjacency implementation:
  - Coplanar edge-neighbor links.
  - Convex 90° corner transitions.
  - Concave transitions with diagonal emptiness check.

### Exit Criteria
- 100% pass on unit tests for face extraction and adjacency rules.
- Imported reference assets produce deterministic graph hashes.
- Test scene renders graph overlays for debugging.

---

## Phase 2 (Months 3–4): Solvers + Generation

### Deliverables
- Formal puzzle representation (terminals, color sets, constraints).
- Generator pipeline:
  - Path-growing with randomized union-find.
  - Structural pre-checks for unsolvability.
  - Difficulty scoring tags.
- Solver stack:
  - Runtime AC-3 + backtracking for hinting and fail-fast checks.
  - Offline SAT and/or MIP uniqueness verification.
- Content tooling:
  - Batch “generate → solve → uniqueness check → publish” command.

### Exit Criteria
- Each candidate level gets a signed validation report:
  - solvable = true
  - unique = true
  - difficulty tier assigned
- Generation throughput target met (e.g., 500 valid puzzles/hour offline).

---

## Phase 3 (Months 5–6): Graphics + Optimization

### Deliverables
- Dynamic path mesh extrusion replacing `LineRenderer`.
- Corner-smoothing shader logic using adjacent-face normal interpolation.
- Greedy meshing + chunk strategy for static puzzle bodies.
- Job System/Burst integration for mesh rebuild tasks.
- Rendering strategy matrix implementation:
  - static batching (environment)
  - GPU instancing (dynamic repeated elements)
  - greedy-meshed model chunks
- Outline post-process pass with distance-consistent width.

### Exit Criteria
- 60 FPS on target mid-tier Android/iOS devices in worst-case scene budget.
- GPU and CPU frame timings within budget with < 2 ms spikes beyond threshold.
- No visible path clipping at right-angle transitions.

---

## Phase 4 (Months 7–8): UX Polish + Launch Readiness

### Deliverables
- Onboarding tutorials for both modes.
- Accessibility options (colorblind palettes, haptic intensity, left-handed UI layout).
- Progression/meta loop (stars, unlocks, challenge cadence).
- Monetization integration (rewarded ads, no-ads, cosmetic store shell).
- QA hardening, localization readiness, app store compliance.

### Exit Criteria
- Soft launch KPIs achieved in at least one test region.
- Crash rate and ANR thresholds within platform standards.
- Final go/no-go review with risk burndown complete.

---

## 5) Detailed Backlog by System

## A) Core Data Structures
- `VoxelCell { position, colorIndex, flags }`
- `SurfaceFace { voxelId, normal, localFaceId, colorState }`
- `SurfaceGraph { vertices: FaceId[], edges: FaceAdjacency[] }`
- `PuzzleDefinition { terminals, allowedColors, ruleset, difficulty }`
- `ValidationReport { solvable, unique, solveTimeMs, branchingFactor }`

## B) Mode A (Connectivity)
- Drag-to-paint with face snapping and corner traversal.
- Real-time legality checks (overlap, stranded regions, dead-end warnings).
- Completion validator:
  1. all terminals connected to correct pair,
  2. no overlaps,
  3. full surface coverage.

## C) Mode B (Sorting)
- Conveyor state machine (spawn/move/consume).
- Tap queue injection and ammo accounting.
- Clear/loss conditions and pacing controls (speed ramps, combo windows).

## D) Generation + Solver Tooling
- CLI commands:
  - `import-vox`
  - `build-graph`
  - `generate-levels`
  - `verify-unique`
  - `publish-pack`
- Seeded RNG for reproducibility.
- “Reject reason taxonomy” for tuning generator quality.

## E) Telemetry
Track at minimum:
- tutorial step funnels,
- level start/fail/complete,
- hint usage,
- mode preference split,
- session length,
- ad engagement and IAP conversion.

---

## 6) Risk Register and Mitigations

1. **3D touch ambiguity on mobile**
   - Mitigate via aggressive face highlighting, sticky snapping, camera assist, and undo gestures.
2. **Solver cost explosion on complex topology**
   - Use tiered validation (fast pre-checks -> AC-3 -> SAT/MIP offline only).
3. **Runtime performance regressions**
   - Device farm profiling each sprint; enforce perf budgets in CI gates.
4. **Content quality drift (duplicate-feel levels)**
   - Uniqueness checks + entropy/diversity constraints in generator scoring.
5. **Monetization harming retention**
   - Cap ad frequency and prioritize rewarded opt-in design.

---

## 7) Team Cadence and Delivery Process

- Sprint length: **2 weeks**.
- Every sprint includes:
  - 1 planning day,
  - 8 execution days,
  - 1 QA/perf hardening day.
- Definition of Done for gameplay tickets:
  - feature complete,
  - unit/integration tests green,
  - telemetry hooks added,
  - performance budget validated.

---

## 8) Launch Plan

### Soft Launch (4–6 weeks)
- Regions: one English-primary + one secondary market.
- Goals: tutorial completion, D1/D7 retention, economy baseline.
- Weekly tuning via remote config (difficulty curve, reward cadence, ad pacing).

### Global Launch
- Trigger only after soft-launch KPI thresholds are met for two consecutive weeks.
- Pair launch with first seasonal content drop to improve conversion and retention.

---

## 9) Immediate Next 30-Day Execution Checklist

1. Build `.vox` parser prototype and validate 10 benchmark assets.
2. Ship `SurfaceGraph` extraction with debug visualization.
3. Implement Mode A input + path legality checks on simple cube/torus test levels.
4. Stand up offline solver service and uniqueness report format.
5. Define telemetry schema and instrument first 20 core events.
6. Run first performance baseline on representative mid-tier devices.

This plan is designed to move from technical certainty (graph and solver correctness) to production confidence (performance, UX clarity, and monetization balance), minimizing late-stage rework while preserving room for content-driven growth.
