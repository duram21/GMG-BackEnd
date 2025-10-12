# filename: build_seoul_graph_v5_final.py
# pip: pip install osmnx networkx matplotlib scikit-learn geopandas
# (osmnx 최신 버전에 완벽 호환)

import os
import osmnx as ox
import networkx as nx
import matplotlib
matplotlib.use("Agg")  # GUI 창 띄우지 않고 파일로만 저장
import matplotlib.pyplot as plt

# ===================== 사용자 설정 =====================
SMALL_TEST = False
DIST_M = 2000
PLACE_NAME = "Seoul, South Korea"
CENTER = (37.56578, 126.9386)

SIMPLIFY = True
RETAIN_ALL = True

OUTDIR = "seoul_graph_out"
MODES = ["drive", "walk", "bike"]
# =======================================================

ox.settings.use_cache = True
ox.settings.log_console = True
ox.settings.requests_timeout = 180
ox.settings.cache_folder = os.path.join(OUTDIR, "cache")
os.makedirs(OUTDIR, exist_ok=True)

DEFAULT_SPEEDS = {
    "drive": {
        "motorway": 90, "trunk": 80, "primary": 60, "secondary": 50,
        "tertiary": 40, "residential": 30, "unclassified": 30, "service": 20
    },
    "walk":  {"footway": 4.5, "path": 4.0, "pedestrian": 4.5, "residential": 4.5},
    "bike":  {"cycleway": 15, "residential": 12, "tertiary": 18, "secondary": 20, "primary": 22},
}

def _parse_speed_kph(edge_data, mode="drive"):
    spd = edge_data.get("maxspeed")
    if isinstance(spd, list) and spd:
        spd = spd[0]
    if spd:
        try:
            return float(str(spd).split()[0])
        except Exception:
            pass
    hwy = edge_data.get("highway")
    if isinstance(hwy, list) and hwy:
        hwy = hwy[0]
    defaults = DEFAULT_SPEEDS.get(mode, {})
    return defaults.get(hwy, 40.0 if mode == "drive" else (15.0 if mode == "bike" else 4.5))

def add_travel_time(G, mode="drive"):
    for u, v, k, data in G.edges(keys=True, data=True):
        L = float(data.get("length", 0.0) or 0.0)
        kph = max(_parse_speed_kph(data, mode), 1e-6)
        data["travel_time"] = (L / 1000.0) / kph * 3600.0
    return G

def _route_sum_attr(G, route_nodes, attr):
    route_gdf = ox.routing.route_to_gdf(G, route_nodes, weight=attr)
    return route_gdf[attr].sum()

def plot_and_save(G, route_nodes, fname_png):
    fig, ax = ox.plot_graph_route(
        G, route_nodes, node_size=0, route_linewidth=3, route_alpha=0.9,
        bgcolor="white", show=False, close=False
    )
    fig.savefig(fname_png, dpi=220, bbox_inches="tight")
    plt.close(fig)

def build_graph(mode):
    if SMALL_TEST:
        G = ox.graph_from_point(
            CENTER, dist=DIST_M, network_type=mode,
            simplify=SIMPLIFY, retain_all=RETAIN_ALL
        )
    else:
        G = ox.graph_from_place(
            PLACE_NAME, network_type=mode,
            simplify=SIMPLIFY, retain_all=RETAIN_ALL
        )
    return G

def save_graph(G, mode, outdir=OUTDIR):
    graphml = os.path.join(outdir, f"{mode}.graphml")
    gpkg = os.path.join(outdir, f"{mode}.gpkg")
    ox.save_graphml(G, graphml)
    ox.save_graph_geopackage(G, filepath=gpkg, directed=True)
    return graphml, gpkg

def shortest_routes_and_plots(G, mode, outdir=OUTDIR):
    origin = CENTER
    dest   = (37.55171, 126.9261)
    try:
        # [!!!] 여기가 최종 수정된 부분입니다: longitude/latitude -> X/Y
        o = ox.distance.nearest_nodes(G, X=origin[1], Y=origin[0])
        d = ox.distance.nearest_nodes(G, X=dest[1],  Y=dest[0])
    except Exception as e:
        print(f"[{mode}] 최근접 노드 탐색 실패: {e}")
        return

    # 거리 기준
    try:
        route_dist = nx.shortest_path(G, o, d, weight="length")
        dist_m = _route_sum_attr(G, route_dist, "length")
        png1 = os.path.join(outdir, f"{mode}_route_distance.png")
        plot_and_save(G, route_dist, png1)
        print(f"[{mode}] distance≈{dist_m:.1f} m → {png1}")
    except nx.NetworkXNoPath:
        print(f"[{mode}] 경로 없음(거리 기준)")

    # 시간 기준
    add_travel_time(G, mode=mode)
    try:
        route_time = nx.shortest_path(G, o, d, weight="travel_time")
        t_sec = _route_sum_attr(G, route_time, "travel_time")
        png2 = os.path.join(outdir, f"{mode}_route_time.png")
        plot_and_save(G, route_time, png2)
        print(f"[{mode}] time≈{t_sec:.1f} s ({t_sec/60:.1f} min) → {png2}")
    except nx.NetworkXNoPath:
        print(f"[{mode}] 경로 없음(시간 기준)")

def main():
    print(f"Building graphs for modes: {MODES} | SMALL_TEST={SMALL_TEST} | "
          f"SIMPLIFY={SIMPLIFY} | RETAIN_ALL={RETAIN_ALL}")
    print(f"Cache folder: {ox.settings.cache_folder}")

    for mode in MODES:
        # 테스트를 위해 'drive' 모드만 실행하도록 하는 좋은 코드입니다.
        if mode != MODES[1] :
            continue
        
        print(f"\n=== Building {mode} graph ===")
        G = build_graph(mode)
        print(f"[{mode}] nodes={G.number_of_nodes():,}, edges={G.number_of_edges():,}")

        graphml, gpkg = save_graph(G, mode)
        print(f"[{mode}] saved GraphML: {graphml}")
        print(f"[{mode}] saved GPKG:    {gpkg}")

        shortest_routes_and_plots(G, mode)

    print("\nAll done. Saved to:", os.path.abspath(OUTDIR))

if __name__ == "__main__":
    main()