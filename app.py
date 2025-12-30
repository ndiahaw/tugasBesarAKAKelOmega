import streamlit as st
import math
import pandas as pd
import time

# ================== KONFIGURASI ==================
st.set_page_config(
    page_title="Analisis Kompleksitas Tower of Hanoi",
    layout="wide"
)

MAX_VISUAL_N = 15
MAX_GRAPH_N = 100
BASE_WIDTH = 120
ANIMATION_DELAY = 0.08

# ================== JUDUL ==================
st.title("Analisis Kompleksitas Algoritma")
st.subheader("Studi Kasus: Tower of Hanoi")

# ================== SIDEBAR ==================
st.sidebar.header("Parameter")
n = st.sidebar.number_input(
    "Jumlah disk (n)",
    min_value=1,
    max_value=10000,
    value=5,
    step=1
)

show_visual = st.sidebar.checkbox("Tampilkan visualisasi", value=True)

# ================== ANALISIS MATEMATIS ==================
st.markdown("## Analisis Kompleksitas")

Tn = 2**n - 1
log10_Tn = n * math.log10(2)

c1, c2, c3 = st.columns(3)
c1.metric("Jumlah disk", n)
c2.metric("T(n)", "2^n - 1")
c3.metric("Skala besar", f"10^{log10_Tn:.2f}")

# ================== GRAFIK PERTUMBUHAN ==================
st.markdown("## Laju Pertumbuhan")

plot_n = min(n, MAX_GRAPH_N)
df = pd.DataFrame({
    "n": range(1, plot_n + 1),
    "log10(2^n)": [i * math.log10(2) for i in range(1, plot_n + 1)]
})

st.line_chart(df, x="n", y="log10(2^n)", height=350)

# ================== PENGUKURAN WAKTU EKSEKUSI ==================
st.markdown("## Waktu Eksekusi")

def hanoi_recursive_count(n):
    if n == 1:
        return 1
    return hanoi_recursive_count(n-1) + 1 + hanoi_recursive_count(n-1)

def hanoi_iterative_count(n):
    stack = [(n, 0, 1, 2)]
    count = 0
    while stack:
        k, _, _, _ = stack.pop()
        if k == 1:
            count += 1
        else:
            stack.append((k-1, 1, 0, 2))
            stack.append((1, 0, 1, 2))
            stack.append((k-1, 0, 2, 1))
    return count

col_r, col_i = st.columns(2)

with col_r:
    start = time.perf_counter()
    hanoi_recursive_count(n)
    end = time.perf_counter()
    st.metric("Rekursif (detik)", f"{end - start:.6f}")

with col_i:
    start = time.perf_counter()
    hanoi_iterative_count(n)
    end = time.perf_counter()
    st.metric("Iteratif (detik)", f"{end - start:.6f}")

# ================== VISUALISASI ==================
st.markdown("## Visualisasi Tower of Hanoi")

def generate_moves(n, src, aux, dst):
    if n == 1:
        yield (src, dst)
    else:
        yield from generate_moves(n-1, src, dst, aux)
        yield (src, dst)
        yield from generate_moves(n-1, aux, src, dst)

def render_towers(towers, placeholder):
    with placeholder.container():
        cols = st.columns(3)
        labels = ["Tower A", "Tower B", "Tower C"]
        for i in range(3):
            with cols[i]:
                st.markdown(f"**{labels[i]}**")
                for disk in reversed(towers[i]):
                    width = int((disk / MAX_VISUAL_N) * BASE_WIDTH)
                    st.markdown(
                        f"""
                        <div style="
                            background:#4da6ff;
                            height:16px;
                            width:{width}px;
                            margin:4px auto;
                            border-radius:6px;
                        "></div>
                        """,
                        unsafe_allow_html=True
                    )

def run_visual(n):
    towers = [list(range(n, 0, -1)), [], []]
    placeholder = st.empty()

    for src, dst in generate_moves(n, 0, 1, 2):
        disk = towers[src].pop()
        towers[dst].append(disk)
        render_towers(towers, placeholder)
        time.sleep(ANIMATION_DELAY)

    # FORCE FINAL STATE
    towers = [[], [], list(range(n, 0, -1))]
    render_towers(towers, placeholder)

    st.success("Simulasi selesai")

if show_visual:
    if n <= MAX_VISUAL_N:
        if st.button("Jalankan visualisasi"):
            run_visual(n)
    else:
        st.warning("Visualisasi hanya tersedia untuk n ≤ 15")

# ================== KESIMPULAN ==================
st.markdown("""
## Kesimpulan

- Tower of Hanoi memiliki kompleksitas waktu O(2^n)
- Rekursif dan iteratif menghasilkan jumlah langkah yang sama
- Iteratif lebih aman untuk n besar
- Visualisasi hanya layak untuk n kecil
""")
