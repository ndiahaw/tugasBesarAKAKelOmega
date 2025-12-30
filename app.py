import streamlit as st
import math
import pandas as pd
import time
import sys

# Konfigurasi
st.set_page_config(
    page_title="Analisis Kompleksitas Tower of Hanoi",
    layout="wide"
)
st.markdown(
    """
    <style>
    h1, h2, h3 {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }

    .stMarkdown h1 a,
    .stMarkdown h2 a,
    .stMarkdown h3 a {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)
MAX_VISUAL_N = 15
MAX_GRAPH_N = 25
BASE_WIDTH = 120
ANIMATION_DELAY = 0.05

sys.setrecursionlimit(3000)

# Judul
st.markdown(
    """
    <div style="text-align:center;">
        <h1 style="margin-bottom: 4px;">
            Analisis Kompleksitas Algoritma
        </h1>
        <h3 style="margin-top: 0; font-weight: 400;">
            Studi Kasus: Tower of Hanoi
        </h3>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# Input
left, center, right = st.columns([1, 2, 1])

with center:
    n = st.number_input(
        "Jumlah disk (n)",
        min_value=1,
        max_value=1000,
        value=1,
        step=1
    )

# Rekursif
def hanoi_recursive_dummy(k):
    if k == 0:
        return
    hanoi_recursive_dummy(k - 1)
    hanoi_recursive_dummy(k - 1)

# Iteratif
def hanoi_iterative_dummy(k):
    stack = [k]
    while stack:
        x = stack.pop()
        if x > 0:
            stack.append(x - 1)
            stack.append(x - 1)

# Analisis
st.markdown("## Analisis Kompleksitas")

Tn = 2**n - 1
log10_Tn = n * math.log10(2)

c1, c2, c3 = st.columns(3)
c1.metric("Jumlah disk (n)", n,)
c2.metric("Jumlah langkah", f"2^{n} - 1")
c3.metric("Skala besar", f"10^{log10_Tn:.2f}")

# Grafik
st.markdown("## Perbandingan Waktu Eksekusi (Iterative vs Recursive)")

MAX_TEST_N = 25
max_n = min(n, MAX_TEST_N)

ns = list(range(1, max_n + 1))
recursive_times = []
iterative_times = []

for k in ns:
    # rekursig
    start = time.perf_counter()
    hanoi_recursive_dummy(k)
    recursive_times.append(time.perf_counter() - start)

    # iteratif
    start = time.perf_counter()
    hanoi_iterative_dummy(k)
    iterative_times.append(time.perf_counter() - start)

df_compare = pd.DataFrame({
    "n": ns,
    "Recursive": recursive_times,
    "Iterative": iterative_times
})

st.line_chart(df_compare.set_index("n"), height=350)


#Execution Time
st.markdown("## Waktu Eksekusi")

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

# psudocode
st.markdown("## Pseudocode")
pc1, pc2 = st.columns(2)

# rekursif
with pc1:       
    st.markdown("### Rekursif")
    st.code("""
Procedure Hanoi(n, A, B, C)
    if (n == 1) then
        output("Pindahkan disk dari", A, "ke", C)
    else
        Hanoi(n-1, A, C, B)
        output("Pindahkan disk dari", A, "ke", C)
        Hanoi(n-1, B, A, C)

""")
# iteratif
with pc2:
    st.markdown("### Iteratif (Stack)")
    st.code("""
Procedure Push(S, data)
    S.top = S.top + 1
    S[S.top] = data
Procedure Pop(S)
    if (S.top == -1) then
        output"Stack kosong"
    else
        data = S[S.top]
        S.top = S.top - 1
Procedure IterativeHanoi(n, A, B, C)
    S = CreateStack()
    Push(S, (n, A, B, C))
    while (S.top != -1) do
        Pop(S)
        if (k == 1) then
            output("Pindahkan disk dari", src, "ke", dst)
        else
            Push(S, (k-1, aux, src, dst))
            Push(S, (1, src, aux, dst))
            Push(S, (k-1, src, dst, aux))

""")
     
# Tampilan Visual
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
    
# input maks visual
if n <= MAX_VISUAL_N:
    if st.button("Jalankan visualisasi"):
        run_visual(n)
else:
    st.warning("Visualisasi hanya tersedia untuk n ≤ 15")
