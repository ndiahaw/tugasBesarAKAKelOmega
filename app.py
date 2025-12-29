import streamlit as st
import math
import pandas as pd
import time

# ================== KONFIGURASI ==================
st.set_page_config(
    page_title="Analisis Kompleksitas Tower of Hanoi",
    layout="wide"
)

MAX_VISUAL_N = 15          # visual FULL hanya sampai n=15
MAX_GRAPH_N = 1000          # grafik pertumbuhan max 100
BASE_WIDTH = 100           # lebar dasar disk (stabil untuk n kecil)

# ================== JUDUL ==================
st.title("🗼 Analisis Kompleksitas Algoritma")
st.subheader("Studi Kasus: Tower of Hanoi")

st.markdown("""
Aplikasi ini menampilkan:
- **Analisis kompleksitas waktu**
- **Perbandingan rekursif vs iteratif**
- **Visualisasi Tower of Hanoi**
dengan pendekatan **aman dan akademis**.
""")

# ================== SIDEBAR ==================
st.sidebar.header("⚙️ Parameter")
n = st.sidebar.number_input(
    "Jumlah disk (n)",
    min_value=1,
    max_value=10000,
    value=5,
    step=1
)

show_visual = st.sidebar.checkbox(
    "🎨 Tampilkan Visualisasi",
    value=True
)

# ================== ANALISIS KOMPLEKSITAS ==================
start_time = time.perf_counter()
log10_Tn = n * math.log10(2)
Tn_approx = f"10^{log10_Tn:.2f}"
analysis_time = time.perf_counter() - start_time

st.markdown("## 📊 Hasil Analisis Kompleksitas")
c1, c2, c3 = st.columns(3)
c1.metric("Jumlah Disk (n)", n)
c2.metric("Rumus T(n)", "2ⁿ − 1")
c3.metric("Perkiraan Besar T(n)", Tn_approx)
st.caption(f"⏱️ Waktu analisis: {analysis_time:.6f} detik")

# ================== BIG-O ==================
st.markdown("## 📐 Analisis Big-O")
st.markdown("""
### ⏱️ Kompleksitas Waktu
- Rekursif → **O(2ⁿ)**
- Iteratif → **O(2ⁿ)**

# ================== GRAFIK PERTUMBUHAN ==================
st.markdown("## 📈 Laju Pertumbuhan Kompleksitas")

plot_n = min(n, MAX_GRAPH_N)
x = list(range(1, plot_n + 1))
y = [i * math.log10(2) for i in x]

df = pd.DataFrame({
    "n": x,
    "log10(2ⁿ)": y
})

st.line_chart(df, x="n", y="log10(2ⁿ)", height=400)
st.caption("Grafik dibatasi hingga n=100 agar tetap stabil (skala log).")

# ================== PSEUDOCODE ==================
st.markdown("## 🧠 Pseudocode")

pc1, pc2 = st.columns(2)

with pc1:
    st.markdown("### 🔁 Rekursif")
    st.code("""
procedure Hanoi(n, A, B, C):
    if n == 1:
        move A → C
    else:
        Hanoi(n-1, A, C, B)
        move A → C
        Hanoi(n-1, B, A, C)
""")

with pc2:
    st.markdown("### 🔂 Iteratif (Stack)")
    st.code("""
push (n, A, B, C) to stack
while stack not empty:
    pop (k, src, aux, dst)
    if k == 1:
        move src → dst
    else:
        push (k-1, aux, src, dst)
        push (1, src, aux, dst)
        push (k-1, src, dst, aux)
""")

# ================== PENJABARAN ANALISIS ==================
st.markdown("## 🧩 Penjabaran Analisis Kompleksitas")

st.markdown("### 🔁 Rekursif — Relasi Rekurens")
st.latex(r"T(n) = 2T(n-1) + 1,\quad T(1)=1")
st.latex(r"T(n) = 2^n - 1")

st.markdown("""
Relasi rekurens diperoleh langsung dari struktur pemanggilan fungsi
pada pseudocode rekursif.
""")

st.markdown("### 🔂 Iteratif — Substitusi / Deret Geometri")
st.latex(r"T(n) = 1 + 2 + 4 + \dots + 2^{n-1}")
st.latex(r"T(n) = \sum_{i=0}^{n-1} 2^i = 2^n - 1")

st.success("""
✅ Walaupun metode analisis berbeda (rekurens vs substitusi),
jumlah langkah Tower of Hanoi **tetap sama**.
""")

# ================== VISUALISASI ==================
st.markdown("## 🎨 Visualisasi Tower of Hanoi")

def hanoi_steps_recursive(n, src, aux, dst):
    if n == 1:
        yield (src, dst)
    else:
        yield from hanoi_steps_recursive(n-1, src, dst, aux)
        yield (src, dst)
        yield from hanoi_steps_recursive(n-1, aux, src, dst)

def hanoi_steps_iterative(n):
    stack = [(n, 0, 1, 2)]
    while stack:
        k, src, aux, dst = stack.pop()
        if k == 1:
            yield (src, dst)
        else:
            stack.append((k-1, aux, src, dst))
            stack.append((1, src, aux, dst))
            stack.append((k-1, src, dst, aux))

def render_towers(towers, title, placeholder):
    with placeholder.container():
        st.markdown(f"### {title}")
        cols = st.columns(3)
        labels = ["Tower A", "Tower B", "Tower C"]
        max_disk = max(len(t) for t in towers)

        for i in range(3):
            with cols[i]:
                st.markdown(f"**{labels[i]}**")
                for disk in reversed(towers[i]):
                    width = int((disk / max_disk) * BASE_WIDTH)
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

def run_side_by_side(n):
    rec = [list(range(n, 0, -1)), [], []]
    ite = [list(range(n, 0, -1)), [], []]

    rec_steps = hanoi_steps_recursive(n, 0, 1, 2)
    ite_steps = hanoi_steps_iterative(n)

    c1, c2 = st.columns(2)
    ph_rec = c1.empty()
    ph_ite = c2.empty()

    total_steps = 2**n - 1

    for _ in range(total_steps):
        s, d = next(rec_steps)
        rec[d].append(rec[s].pop())

        s, d = next(ite_steps)
        ite[d].append(ite[s].pop())

        render_towers(rec, "🔁 Rekursif", ph_rec)
        render_towers(ite, "📦 Iteratif", ph_ite)

        time.sleep(0.12)

    st.success("✅ Simulasi selesai — semua disk berpindah ke Tower C")

if show_visual:
    if n <= MAX_VISUAL_N:
        st.info(f"Visualisasi FULL aktif (n ≤ {MAX_VISUAL_N})")
        if st.button("▶️ Jalankan Rekursif & Iteratif"):
            run_side_by_side(n)
    else:
        st.warning(
            f"Visualisasi dinonaktifkan untuk n > {MAX_VISUAL_N} "
            "(jumlah langkah eksponensial)."
        )

# ================== KESIMPULAN ==================
st.success("""
🎯 **Kesimpulan Akhir**
- Tower of Hanoi memiliki kompleksitas **O(2ⁿ)**
- Visualisasi hanya layak untuk **n kecil**
- Untuk n besar, **analisis matematis adalah pendekatan yang benar**
""")

