import streamlit as st
import math
import pandas as pd
import time
import sys

# ================== KONFIGURASI ==================
st.set_page_config(
    page_title="Analisis Kompleksitas Tower of Hanoi",
    layout="wide"
)

MAX_VISUAL_N = 15
MAX_GRAPH_N = 100
BASE_WIDTH = 120
ANIMATION_DELAY = 0.08

sys.setrecursionlimit(3000)

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
c2.metric("Jumlah langkah", f"2^{n} - 1")
c3.metric("Skala besar", f"10^{log10_Tn:.2f}")

# ================== GRAFIK ==================
st.markdown("## Laju Pertumbuhan")

plot_n = min(n, MAX_GRAPH_N)
df = pd.DataFrame({
    "n": range(1, plot_n + 1),
    "log10(2^n)": [i * math.log10(2) for i in range(1, plot_n + 1)]
})

st.line_chart(df, x="n", y="log10(2^n)", height=350)

# ================== WAKTU EKSEKUSI ==================
st.markdown("## Waktu Eksekusi (seperti terminal)")

# Rekursif aman (dummy depth kecil)
def hanoi_recursive_dummy(k):
    if k == 0:
        return
    hanoi_recursive_dummy(k - 1)
    hanoi_recursive_dummy(k - 1)

# Iteratif stack
def hanoi_iterative_dummy(k):
    stack = [k]
    while stack:
        x = stack.pop()
        if x > 0:
            stack.append(x - 1)
            stack.append(x - 1)

SAFE_N = min(n, 25)

col_r, col_i = st.columns(2)

with col_r:
    start = time.perf_counter()
    hanoi_recursive_dummy(SAFE_N)
    end = time.perf_counter()
    st.code(f"Recursive execution time: {end - start:.6f} seconds")

with col_i:
    start = time.perf_counter()
    hanoi_iterative_dummy(SAFE_N)
    end = time.perf_counter()
    st.code(f"Iterative execution time: {end - start:.6f} seconds")

st.caption("Pengukuran dibatasi depth kecil agar aman dari crash")

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
    anim_placeholder = st.empty()
    final_placeholder = st.empty()

    for src, dst in generate_moves(n, 0, 1, 2):
        disk = towers[src].pop()
        towers[dst].append(disk)
        anim_placeholder.empty()
        render_towers(towers, anim_placeholder)
        time.sleep(ANIMATION_DELAY)
        
    anim_placeholder.empty()
    render_towers(towers, final_placeholder)
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
- Rekursif rawan crash untuk n besar
- Iteratif lebih aman secara memori
- Visualisasi hanya masuk akal untuk n kecil
""")
