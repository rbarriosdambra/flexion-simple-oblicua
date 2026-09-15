
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon

st.set_page_config(
    page_title="Aplicación Didáctica de Flexión",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# ESTILO
# =========================================================
st.markdown("""
<style>
.block-container {
    padding-top: 1.3rem;
    padding-bottom: 2rem;
    max-width: 1280px;
}
h1, h2, h3 {
    letter-spacing: -0.02em;
}
.app-subtitle {
    color: #666;
    margin-top: -0.65rem;
    margin-bottom: 1.1rem;
}
.status-card {
    border: 1px solid rgba(128,128,128,0.22);
    border-radius: 14px;
    padding: 0.70rem 0.95rem;
    margin-bottom: 1rem;
    background: rgba(128,128,128,0.05);
}
.compact-card {
    border: 1px solid rgba(128,128,128,0.18);
    border-radius: 12px;
    padding: 0.75rem 0.85rem;
    background: rgba(128,128,128,0.035);
}
.result-card {
    border: 1px solid rgba(128,128,128,0.18);
    border-radius: 10px;
    padding: 0.45rem 0.60rem;
    background: rgba(128,128,128,0.035);
    min-height: 70px;
}
.result-label {
    font-size: 0.74rem;
    color: #666;
    margin-bottom: 0.18rem;
}
.result-value {
    font-size: 1.05rem;
    line-height: 1.1;
    font-weight: 500;
    white-space: nowrap;
}
.small {
    font-size: 0.88rem;
    color: #666;
}
@media (max-width: 768px) {
    .result-card {
        padding: 0.38rem 0.48rem;
        min-height: 60px;
    }
    .result-label {
        font-size: 0.68rem;
    }
    .result-value {
        font-size: 0.92rem;
    }
}
</style>
""", unsafe_allow_html=True)

st.title("📐 Aplicación Didáctica de Flexión")
st.markdown(
    '<div class="app-subtitle">Flexión simple y flexión oblicua</div>',
    unsafe_allow_html=True
)

# =========================================================
# FUNCIONES
# =========================================================
def propiedades_seccion(seccion, vals):
    if seccion == "Rectangular maciza":
        b_cm = vals["b_cm"]
        h_cm = vals["h_cm"]
        b = b_cm / 100.0
        h = h_cm / 100.0
        Ix = b * h**3 / 12.0
        Wx = Ix / (h/2)
        y_ext_cm = h_cm/2
        return Ix, Wx, y_ext_cm

    elif seccion == "Circular maciza":
        d_cm = vals["d_cm"]
        d = d_cm / 100.0
        Ix = np.pi * d**4 / 64.0
        Wx = Ix / (d/2)
        y_ext_cm = d_cm/2
        return Ix, Wx, y_ext_cm

    elif seccion == "Tubular circular":
        D_cm = vals["D_cm"]
        di_cm = vals["di_cm"]
        D = D_cm / 100.0
        di = di_cm / 100.0
        Ix = np.pi * (D**4 - di**4) / 64.0
        Wx = Ix / (D/2)
        y_ext_cm = D_cm/2
        return Ix, Wx, y_ext_cm

    else:
        h_cm = vals["h_cm"]
        bf_cm = vals["bf_cm"]
        tf_cm = vals["tf_cm"]
        tw_cm = vals["tw_cm"]

        h = h_cm / 100.0
        bf = bf_cm / 100.0
        tf = tf_cm / 100.0
        tw = tw_cm / 100.0
        hw = h - 2*tf

        Ix = (
            2 * (
                bf*tf**3/12.0
                + (bf*tf)*(h/2.0 - tf/2.0)**2
            )
            + tw*hw**3/12.0
        )
        Wx = Ix / (h/2)
        y_ext_cm = h_cm/2
        return Ix, Wx, y_ext_cm


def entrada_geometria(prefix="sec"):
    seccion = st.selectbox(
        "Tipo de sección",
        ["Rectangular maciza", "Circular maciza", "Tubular circular", "Doble T"],
        key=f"{prefix}_tipo"
    )

    vals = {}

    if seccion == "Rectangular maciza":
        c1, c2 = st.columns(2)
        with c1:
            vals["b_cm"] = st.number_input(
                "Base b [cm]", min_value=0.1, value=20.0, step=1.0,
                key=f"{prefix}_b"
            )
        with c2:
            vals["h_cm"] = st.number_input(
                "Altura h [cm]", min_value=0.1, value=40.0, step=1.0,
                key=f"{prefix}_h"
            )

    elif seccion == "Circular maciza":
        vals["d_cm"] = st.number_input(
            "Diámetro d [cm]", min_value=0.1, value=30.0, step=1.0,
            key=f"{prefix}_d"
        )

    elif seccion == "Tubular circular":
        c1, c2 = st.columns(2)
        with c1:
            vals["D_cm"] = st.number_input(
                "Diámetro exterior D [cm]", min_value=0.2, value=30.0, step=1.0,
                key=f"{prefix}_D"
            )
        with c2:
            vals["di_cm"] = st.number_input(
                "Diámetro interior d [cm]", min_value=0.1, value=20.0, step=1.0,
                key=f"{prefix}_di"
            )
        if vals["di_cm"] >= vals["D_cm"]:
            st.error("El diámetro interior debe ser menor que el exterior.")
            st.stop()

    else:
        c1, c2 = st.columns(2)
        with c1:
            vals["h_cm"] = st.number_input(
                "Altura total h [cm]", min_value=1.0, value=40.0, step=1.0,
                key=f"{prefix}_hDT"
            )
            vals["tw_cm"] = st.number_input(
                "Espesor de alma tw [cm]", min_value=0.1, value=1.0, step=0.1,
                key=f"{prefix}_tw"
            )
        with c2:
            vals["bf_cm"] = st.number_input(
                "Ancho de ala bf [cm]", min_value=0.2, value=20.0, step=1.0,
                key=f"{prefix}_bf"
            )
            vals["tf_cm"] = st.number_input(
                "Espesor de ala tf [cm]", min_value=0.1, value=2.0, step=0.1,
                key=f"{prefix}_tf"
            )

        if 2*vals["tf_cm"] >= vals["h_cm"]:
            st.error("Debe cumplirse 2·tf < h.")
            st.stop()
        if vals["tw_cm"] >= vals["bf_cm"]:
            st.error("Debe cumplirse tw < bf.")
            st.stop()

    return seccion, vals


def dibujar_seccion(ax, seccion, vals, Mx, y_sel=None, stress_diagram=True):
    Ix, Wx, y_ext_cm = propiedades_seccion(seccion, vals)
    tol = 1e-12

    if seccion == "Rectangular maciza":
        b = vals["b_cm"]
        h = vals["h_cm"]
        x_left, x_right = -b/2, b/2
        y_bottom, y_top = -h/2, h/2
        ax.add_patch(Rectangle((x_left, y_bottom), b, h, fill=False, linewidth=2.2))
        halfw = b/2

    elif seccion == "Circular maciza":
        r = vals["d_cm"]/2
        x_left, x_right = -r, r
        y_bottom, y_top = -r, r
        ax.add_patch(Circle((0,0), r, fill=False, linewidth=2.2))
        halfw = r

    elif seccion == "Tubular circular":
        R = vals["D_cm"]/2
        ri = vals["di_cm"]/2
        x_left, x_right = -R, R
        y_bottom, y_top = -R, R
        ax.add_patch(Circle((0,0), R, fill=False, linewidth=2.2))
        ax.add_patch(Circle((0,0), ri, fill=False, linewidth=2.0))
        halfw = R

    else:
        h = vals["h_cm"]
        bf = vals["bf_cm"]
        tf = vals["tf_cm"]
        tw = vals["tw_cm"]

        x_left, x_right = -bf/2, bf/2
        y_bottom, y_top = -h/2, h/2
        halfw = bf/2

        ax.add_patch(Rectangle((-bf/2, y_top-tf), bf, tf, fill=False, linewidth=2.2))
        ax.add_patch(Rectangle((-bf/2, y_bottom), bf, tf, fill=False, linewidth=2.2))
        ax.add_patch(Rectangle((-tw/2, y_bottom+tf), tw, h-2*tf, fill=False, linewidth=2.2))

    ax.axhline(0, linestyle="--", linewidth=1.3)
    ax.axvline(0, linestyle=":", linewidth=1.0)
    ax.scatter([0],[0], s=24, zorder=5)
    ax.text(0.7, 0.8, "G", fontsize=9)
    ax.text(x_right+1.1, 0, "Eje neutro", va="center", fontsize=8.5)

    # Momento desde el baricentro. Mx positivo apunta hacia la izquierda.
    if abs(Mx) > tol:
        x_end = x_left + 1.0 if Mx > 0 else x_right - 1.0
        ax.annotate(
            "", xy=(x_end,0), xytext=(0,0),
            arrowprops=dict(arrowstyle="->", linewidth=2.4),
            zorder=6
        )
        ax.text(0, -2.0, f"Mx {'>' if Mx > 0 else '<'} 0", ha="center", fontsize=9)

    # Eje y positivo hacia abajo
    y_arrow_len = max((y_top-y_bottom)*0.18, 2.5)
    ax.annotate(
        "", xy=(0, -y_arrow_len), xytext=(0, 0),
        arrowprops=dict(arrowstyle="->", linewidth=1.4),
        zorder=5
    )
    ax.text(0.8, -y_arrow_len*0.75, "y +", fontsize=8.5)

    # Convención de la cátedra:
    # x positivo hacia la izquierda
    # y positivo hacia abajo
    # Mx positivo: vector hacia la izquierda
    # σ positiva = tracción; σ negativa = compresión
    sigma_sup = (Mx*1e3*(-y_ext_cm/100))/Ix/1e6 if Ix else 0
    sigma_inf = (Mx*1e3*( y_ext_cm/100))/Ix/1e6 if Ix else 0

    ax.text(
        x_left-4.5, y_ext_cm*0.55,
        "Compresión" if sigma_sup < 0 else "Tracción",
        ha="right", va="center", fontsize=9
    )
    ax.text(
        x_left-4.5, -y_ext_cm*0.55,
        "Compresión" if sigma_inf < 0 else "Tracción",
        ha="right", va="center", fontsize=9
    )

    if y_sel is not None:
        y_plot = -y_sel
        ax.scatter([0],[y_plot], s=65, zorder=7)
        ax.text(1.0, y_plot+0.7, f"y = {y_sel:.2f} cm", fontsize=8.5)

    if stress_diagram:
        gap = max(halfw*2.0, 16.0)
        x0 = x_right + gap
        ax.plot([x0,x0],[y_bottom,y_top], linewidth=1.1)

        ys = np.array([y_bottom,0,y_top])
        sigs = np.array([sigma_inf,0,sigma_sup])
        max_sig = max(abs(sigma_sup),abs(sigma_inf),1e-9)
        scale = max(halfw*1.8,10.0)/max_sig
        xs = x0 + sigs*scale

        ax.plot(xs,ys,linewidth=2.0)
        ax.fill_betweenx(ys,x0,xs,alpha=0.16)
        ax.text(x0,y_top+1.5,"Diagrama σ",ha="center",fontsize=9)
        ax.text(xs[-1],y_top,f"  {sigma_sup:.2f} MPa",va="center",fontsize=8.5)
        ax.text(xs[0],y_bottom,f"  {sigma_inf:.2f} MPa",va="center",fontsize=8.5)

        x_max = max(np.max(xs),x0)+max(10.0,halfw*2.0)
    else:
        x_max = x_right + max(8.0,halfw*1.2)

    x_min = x_left - max(8.0,halfw*1.2)
    y_min = y_bottom - 4
    y_max = y_top + 5

    ax.set_xlim(x_min,x_max)
    ax.set_ylim(y_min,y_max)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks([])
    ax.set_ylabel("y [cm]")
    ax.grid(alpha=0.15)

    return Ix, Wx, y_ext_cm, sigma_sup, sigma_inf


def card(col, label, value):
    with col:
        st.markdown(
            f"""<div class="result-card">
            <div class="result-label">{label}</div>
            <div class="result-value">{value}</div>
            </div>""",
            unsafe_allow_html=True
        )

# =========================================================
# TABS PRINCIPALES
# =========================================================
tab_simple, tab_oblicua = st.tabs(["Flexión simple", "Flexión oblicua"])

# =========================================================
# PESTAÑA PRINCIPAL - FLEXIÓN SIMPLE
# =========================================================
with tab_simple:
    st.subheader("Flexión simple")
    st.caption(
        "Estudio de secciones, vigas, comparación geométrica y verificación por tensiones."
    )

    sub_sec, sub_viga, sub_comp, sub_verif = st.tabs(
        ["Sección", "Viga", "Comparar secciones", "Verificación"]
    )

    with sub_sec:

            modo = st.segmented_control(
                "Modo de trabajo",
                options=["Conceptual", "Cálculo", "Explorar sección"],
                default="Cálculo",
                key="modo_sec"
            )

            left, right = st.columns([0.95,1.75], gap="large")

            with left:
                st.subheader("Datos de entrada")
                seccion, vals = entrada_geometria("sec")
                Mx = st.number_input(
                    "Momento flector Mx [kN·m]",
                    value=20.0, step=1.0, format="%.2f",
                    key="sec_Mx"
                )
                My = st.number_input(
                    "Momento flector My [kN·m]",
                    value=0.0, step=1.0, format="%.2f",
                    key="sec_My"
                )

                Ix, Wx, y_ext_cm = propiedades_seccion(seccion, vals)

                if modo == "Explorar sección":
                    y_cm = st.slider(
                        "Posición de la fibra y [cm]",
                        min_value=float(-y_ext_cm),
                        max_value=float(y_ext_cm),
                        value=0.0,
                        step=max(float(2*y_ext_cm/200),0.1),
                        key="sec_y"
                    )
                else:
                    y_cm = None

            es_simple = abs(Mx) > 1e-10 and abs(My) <= 1e-10
            if es_simple:
                st.markdown(
                    f'<div class="status-card"><b>✅ Flexión simple</b><br>'
                    f'<span class="small">Mx = {Mx:.2f} kN·m · My = {My:.2f} kN·m · {seccion}</span></div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div class="status-card"><b>⚠️ Verificar condición de flexión simple</b></div>',
                    unsafe_allow_html=True
                )

            with right:
                st.subheader("Visualización")
                fig, ax = plt.subplots(figsize=(8.0,5.1))
                Ix, Wx, y_ext_cm, sigsup, siginf = dibujar_seccion(
                    ax, seccion, vals, Mx, y_sel=y_cm, stress_diagram=True
                )
                st.pyplot(fig, width="stretch")

            st.markdown("### Resultados")
            r1,r2,r3,r4 = st.columns(4)
            card(r1,"Iₓ",f"{Ix*1e8:,.1f} cm⁴")
            card(r2,"Wₓ",f"{Wx*1e6:,.1f} cm³")
            card(r3,"σ superior",f"{sigsup:.3f} MPa")
            card(r4,"σ inferior",f"{siginf:.3f} MPa")

            if modo == "Explorar sección" and y_cm is not None:
                sigma_y = (Mx*1e3*(y_cm/100))/Ix/1e6
                estado = "Eje neutro" if abs(sigma_y)<1e-9 else ("Compresión" if sigma_y<0 else "Tracción")
                st.markdown("#### Fibra seleccionada")
                a,b,c = st.columns(3)
                card(a,"y",f"{y_cm:.2f} cm")
                card(b,"σ(y)",f"{sigma_y:.3f} MPa")
                card(c,"Estado",estado)

            if modo == "Cálculo":
                st.subheader("Relaciones utilizadas")
                st.latex(r"\sigma(y)=\frac{M_x}{I_x}\,y")
                st.caption("Convención: x positivo hacia la izquierda; y positivo hacia abajo; σ positiva = tracción.")

            with st.expander("📘 Ver explicación teórica"):
                st.markdown("### Condición para flexión simple")
                st.markdown(
                    "Se considera **flexión simple** cuando el momento flector actúa alrededor de "
                    "**un solo eje principal centroidal**."
                )
                st.markdown("Para esta aplicación:")
                st.latex(r"M_x \neq 0 \qquad M_y = 0")
                st.markdown(
                    "- El eje **x positivo** de la viga se considera **hacia la izquierda**.\n"
                    "- El eje **y positivo** se considera **hacia abajo**.\n"
                    "- **Mx > 0** → vector momento hacia la izquierda.\n"
                    "- **Mx > 0** → compresión en las fibras superiores y tracción en las inferiores.\n"
                    "- **Mx < 0** → se invierte la distribución."
                )


    with sub_viga:

            st.subheader("Análisis de vigas")
            st.caption("Relación entre cargas, reacciones, momento flector y tensiones normales")

            caso_viga = st.selectbox(
                "Caso de carga",
                [
                    "Carga puntual centrada",
                    "Carga distribuida uniforme",
                    "Voladizo con carga puntual en el extremo",
                    "Voladizo con carga distribuida uniforme"
                ],
                key="caso_viga"
            )

            cL, cCarga = st.columns(2)

            with cL:
                L = st.number_input(
                    "Longitud de la viga L [m]",
                    min_value=0.5,
                    value=6.0,
                    step=0.5,
                    key="viga_L"
                )

            if caso_viga == "Carga puntual centrada":
                with cCarga:
                    P = st.number_input(
                        "Carga puntual P [kN]",
                        min_value=0.1,
                        value=20.0,
                        step=1.0,
                        key="viga_P"
                    )
                q = None

            elif caso_viga == "Carga distribuida uniforme":
                with cCarga:
                    q = st.number_input(
                        "Carga distribuida q [kN/m]",
                        min_value=0.1,
                        value=10.0,
                        step=0.5,
                        key="viga_q"
                    )
                P = None

            elif caso_viga == "Voladizo con carga puntual en el extremo":
                with cCarga:
                    P = st.number_input(
                        "Carga puntual en el extremo P [kN]",
                        min_value=0.1,
                        value=20.0,
                        step=1.0,
                        key="viga_P_vol"
                    )
                q = None

            else:
                with cCarga:
                    q = st.number_input(
                        "Carga distribuida q [kN/m]",
                        min_value=0.1,
                        value=10.0,
                        step=0.5,
                        key="viga_q_vol"
                    )
                P = None

            st.markdown("#### Sección transversal")
            seccion_v, vals_v = entrada_geometria("viga")

            Ix_v, Wx_v, yext_v = propiedades_seccion(seccion_v, vals_v)

            # -----------------------------------------------------
            # Reacciones y funciones de momento
            # -----------------------------------------------------
            if caso_viga == "Carga puntual centrada":
                RA = P / 2
                RB = P / 2
                Mmax_abs = P * L / 4

                def M_abs_func(x):
                    if x <= L/2:
                        return RA * x
                    return RB * (L - x)

                x_sel_default = L / 2
                etiqueta_reac_1 = "RA"
                etiqueta_reac_2 = "RB"
                reac_1 = RA
                reac_2 = RB

            elif caso_viga == "Carga distribuida uniforme":
                RA = q * L / 2
                RB = q * L / 2
                Mmax_abs = q * L**2 / 8

                def M_abs_func(x):
                    return RA * x - q * x**2 / 2

                x_sel_default = L / 2
                etiqueta_reac_1 = "RA"
                etiqueta_reac_2 = "RB"
                reac_1 = RA
                reac_2 = RB

            elif caso_viga == "Voladizo con carga puntual en el extremo":
                VA = P
                MA = P * L
                Mmax_abs = P * L

                def M_abs_func(x):
                    return P * (L - x)

                x_sel_default = 0.0
                etiqueta_reac_1 = "VA"
                etiqueta_reac_2 = "MA"
                reac_1 = VA
                reac_2 = MA

            else:
                VA = q * L
                MA = q * L**2 / 2
                Mmax_abs = q * L**2 / 2

                def M_abs_func(x):
                    return q * (L - x)**2 / 2

                x_sel_default = 0.0
                etiqueta_reac_1 = "VA"
                etiqueta_reac_2 = "MA"
                reac_1 = VA
                reac_2 = MA

            # Convención de la cátedra:
            # +x hacia la izquierda
            # +y hacia abajo
            # La expresión de tensiones es sigma = Mx*y/Ix
            x_sel = st.slider(
                "Posición de análisis x [m]",
                min_value=0.0,
                max_value=float(L),
                value=float(x_sel_default),
                step=max(float(L/200), 0.01),
                key=f"viga_x_{caso_viga}"
            )

            M_abs_x = M_abs_func(x_sel)

            # Convención elegida para la app:
            # - en los casos simplemente apoyados, Mx positivo -> compresión arriba y tracción abajo
            # - en los voladizos cargados hacia abajo, Mx negativo -> tracción arriba y compresión abajo
            if caso_viga in ["Voladizo con carga puntual en el extremo", "Voladizo con carga distribuida uniforme"]:
                Mx_x = -M_abs_x
            else:
                Mx_x = M_abs_x

            sigma_sup_x = (Mx_x * 1e3 * (-yext_v/100)) / Ix_v / 1e6
            sigma_inf_x = (Mx_x * 1e3 * ( yext_v/100)) / Ix_v / 1e6

            # -----------------------------------------------------
            # Resultados principales
            # -----------------------------------------------------
            st.markdown("### Resultados de la viga")
            a, b, c, d = st.columns(4)
            card(a, etiqueta_reac_1, f"{reac_1:.2f} kN" if etiqueta_reac_1 != "MA" else f"{reac_1:.2f} kN·m")
            card(b, etiqueta_reac_2, f"{reac_2:.2f} kN" if etiqueta_reac_2 != "MA" else f"{reac_2:.2f} kN·m")
            card(c, "|M|max", f"{Mmax_abs:.2f} kN·m")
            card(d, "Mx(x)", f"{Mx_x:.2f} kN·m")

            # -----------------------------------------------------
            # Esquema estructural
            # -----------------------------------------------------
            st.markdown("### Esquema estructural")
            st.caption("Convención de ejes: +x hacia la izquierda · +y hacia abajo")
            fig1, ax1 = plt.subplots(figsize=(9.0, 3.0))

            if caso_viga in ["Carga puntual centrada", "Carga distribuida uniforme"]:
                ax1.plot([0, L], [0, 0], linewidth=3)

                triA = Polygon(
                    [[0, -0.05], [-0.18, -0.35], [0.18, -0.35]],
                    closed=True,
                    fill=False,
                    linewidth=1.5
                )
                triB = Polygon(
                    [[L, -0.05], [L-0.18, -0.35], [L+0.18, -0.35]],
                    closed=True,
                    fill=False,
                    linewidth=1.5
                )
                ax1.add_patch(triA)
                ax1.add_patch(triB)

                # Reacciones
                ax1.annotate(
                    "",
                    xy=(0, 0.65),
                    xytext=(0, 0.02),
                    arrowprops=dict(arrowstyle="->", linewidth=1.8)
                )
                ax1.annotate(
                    "",
                    xy=(L, 0.65),
                    xytext=(L, 0.02),
                    arrowprops=dict(arrowstyle="->", linewidth=1.8)
                )
                ax1.text(0.08, 0.45, f"RA = {RA:.1f}", fontsize=8.5)
                ax1.text(L-0.75, 0.45, f"RB = {RB:.1f}", fontsize=8.5)

                if caso_viga == "Carga puntual centrada":
                    ax1.annotate(
                        "",
                        xy=(L/2, 0.02),
                        xytext=(L/2, 0.95),
                        arrowprops=dict(arrowstyle="->", linewidth=2.2)
                    )
                    ax1.text(L/2 + 0.08, 0.75, f"P = {P:.1f} kN", fontsize=9)

                else:
                    n_arrows = 9
                    xpos = np.linspace(0.3, L-0.3, n_arrows)
                    ax1.plot([0.2, L-0.2], [0.9, 0.9], linewidth=1.4)
                    for xp in xpos:
                        ax1.annotate(
                            "",
                            xy=(xp, 0.04),
                            xytext=(xp, 0.88),
                            arrowprops=dict(arrowstyle="->", linewidth=1.4)
                        )
                    ax1.text(L/2, 1.00, f"q = {q:.1f} kN/m", ha="center", fontsize=9)

            else:
                # Voladizo
                ax1.plot([0, L], [0, 0], linewidth=3)

                # Empotramiento
                ax1.plot([0, 0], [-0.55, 0.75], linewidth=3)
                for yy in np.linspace(-0.5, 0.65, 8):
                    ax1.plot([-0.18, 0], [yy-0.08, yy+0.05], linewidth=1.1)

                if caso_viga == "Voladizo con carga puntual en el extremo":
                    ax1.annotate(
                        "",
                        xy=(L, 0.02),
                        xytext=(L, 0.95),
                        arrowprops=dict(arrowstyle="->", linewidth=2.2)
                    )
                    ax1.text(L-0.15, 0.78, f"P = {P:.1f} kN", fontsize=9, ha="right")

                else:
                    n_arrows = 9
                    xpos = np.linspace(0.3, L-0.1, n_arrows)
                    ax1.plot([0.12, L-0.08], [0.9, 0.9], linewidth=1.4)
                    for xp in xpos:
                        ax1.annotate(
                            "",
                            xy=(xp, 0.04),
                            xytext=(xp, 0.88),
                            arrowprops=dict(arrowstyle="->", linewidth=1.4)
                        )
                    ax1.text(L/2, 1.00, f"q = {q:.1f} kN/m", ha="center", fontsize=9)

                # Reacción vertical y momento de empotramiento
                ax1.annotate(
                    "",
                    xy=(0.18, 0.65),
                    xytext=(0.18, 0.02),
                    arrowprops=dict(arrowstyle="->", linewidth=1.8)
                )
                ax1.text(0.28, 0.47, f"VA = {VA:.1f}", fontsize=8.5)

                theta = np.linspace(np.pi/3, 5*np.pi/3, 80)
                r = 0.28
                xc = 0.55 + r*np.cos(theta)
                yc = 0.10 + r*np.sin(theta)
                ax1.plot(xc, yc, linewidth=1.6)
                ax1.annotate(
                    "",
                    xy=(xc[-1], yc[-1]),
                    xytext=(xc[-4], yc[-4]),
                    arrowprops=dict(arrowstyle="->", linewidth=1.6)
                )
                ax1.text(0.75, 0.52, f"MA = {MA:.1f} kN·m", fontsize=8.5)

            # sección seleccionada
            ax1.axvline(x_sel, linestyle="--", linewidth=1.2)
            ax1.text(x_sel, -0.60, f"x = {x_sel:.2f} m", ha="center", fontsize=9)

            ax1.set_xlim(-0.6, L+0.6)
            ax1.set_ylim(-0.85, 1.2)
            ax1.axis("off")
            st.pyplot(fig1, width="stretch")

            # -----------------------------------------------------
            # Diagrama de momento
            # -----------------------------------------------------
            st.markdown("### Diagrama de momento flector")

            xx = np.linspace(0, L, 400)

            if caso_viga == "Carga puntual centrada":
                Mabs = np.where(xx <= L/2, RA*xx, RB*(L-xx))
                Mx_arr = Mabs
                Mx_arr_plot = -Mabs   # lado traccionado = abajo
                Mx_x_plot = -M_abs_x

            elif caso_viga == "Carga distribuida uniforme":
                Mabs = RA*xx - q*xx**2/2
                Mx_arr = Mabs
                Mx_arr_plot = -Mabs   # lado traccionado = abajo
                Mx_x_plot = -M_abs_x

            elif caso_viga == "Voladizo con carga puntual en el extremo":
                Mabs = P*(L-xx)
                Mx_arr = -Mabs
                Mx_arr_plot = Mabs    # lado traccionado = arriba
                Mx_x_plot = M_abs_x

            else:
                Mabs = q*(L-xx)**2/2
                Mx_arr = -Mabs
                Mx_arr_plot = Mabs    # lado traccionado = arriba
                Mx_x_plot = M_abs_x

            fig2, ax2 = plt.subplots(figsize=(9.0, 3.2))
            ax2.plot(xx, Mx_arr_plot, linewidth=2)
            ax2.fill_between(xx, 0, Mx_arr_plot, alpha=0.16)
            ax2.axhline(0, linewidth=1)
            ax2.axvline(x_sel, linestyle="--", linewidth=1.1)
            ax2.scatter([x_sel], [Mx_x_plot], s=45, zorder=5)
            ax2.text(
                x_sel,
                Mx_x_plot,
                f"  Mx = {Mx_x:.2f} kN·m",
                va="center",
                fontsize=9
            )
            ax2.set_xlabel("x [m]")
            ax2.set_ylabel("Diagrama de Mx [kN·m]")
            ax2.grid(alpha=0.2)
            st.pyplot(fig2, width="stretch")

            # -----------------------------------------------------
            # Sección seleccionada + tensiones
            # -----------------------------------------------------
            st.markdown("### Sección en la posición seleccionada")
            csec, cres = st.columns([1.55, 0.85], gap="large")

            with csec:
                fig3, ax3 = plt.subplots(figsize=(7.5, 4.8))
                dibujar_seccion(
                    ax3,
                    seccion_v,
                    vals_v,
                    Mx_x,
                    y_sel=None,
                    stress_diagram=True
                )
                st.pyplot(fig3, width="stretch")

            with cres:
                st.markdown("#### Estado en x")
                q1, q2 = st.columns(2)
                card(q1, "σ superior", f"{sigma_sup_x:.3f} MPa")
                card(q2, "σ inferior", f"{sigma_inf_x:.3f} MPa")

                st.markdown("<br>", unsafe_allow_html=True)

                if caso_viga == "Carga puntual centrada":
                    texto_fisico = (
                        "La carga puntual centrada genera un diagrama de momento lineal por tramos. "
                        "El valor máximo aparece en el centro del vano. En este caso <b>Mx es positivo</b> "
                        "y su vector apunta hacia la izquierda. Así se obtiene <b>compresión arriba</b> "
                        "y <b>tracción abajo</b>. El diagrama se dibuja hacia abajo, del lado traccionado."
                    )
                elif caso_viga == "Carga distribuida uniforme":
                    texto_fisico = (
                        "La carga distribuida uniforme genera un diagrama de momento <b>parabólico</b>. "
                        "El máximo aparece en el centro del vano. En este caso <b>Mx es positivo</b> "
                        "y su vector apunta hacia la izquierda. Así se obtiene <b>compresión arriba</b> "
                        "y <b>tracción abajo</b>. El diagrama se dibuja hacia abajo, del lado traccionado."
                    )
                elif caso_viga == "Voladizo con carga puntual en el extremo":
                    texto_fisico = (
                        "En el voladizo con carga puntual en el extremo, el máximo momento aparece en el "
                        "empotramiento. En este caso <b>Mx es negativo</b>, por lo que se obtiene "
                        "<b>tracción arriba</b> y <b>compresión abajo</b>. El diagrama se dibuja hacia arriba, "
                        "del lado traccionado."
                    )
                else:
                    texto_fisico = (
                        "En el voladizo con carga distribuida uniforme, el diagrama de momento es "
                        "<b>parabólico</b> y el máximo aparece en el empotramiento. En este caso "
                        "<b>Mx es negativo</b>, por lo que se obtiene <b>tracción arriba</b> y "
                        "<b>compresión abajo</b>. El diagrama se dibuja hacia arriba, del lado traccionado."
                    )

                st.markdown(
                    f'<div class="compact-card"><b>Lectura física</b><br>{texto_fisico}</div>',
                    unsafe_allow_html=True
                )

            # -----------------------------------------------------
            # Desarrollo teórico
            # -----------------------------------------------------
            with st.expander("📘 Desarrollo del caso"):
                if caso_viga == "Carga puntual centrada":
                    st.markdown("Para una carga puntual centrada:")
                    st.latex(r"R_A=R_B=\frac{P}{2}")
                    st.latex(r"|M|_{\max}=\frac{P\,L}{4}")
                    st.markdown("El momento absoluto es:")
                    st.latex(
                        r"|M(x)|="
                        r"\begin{cases}"
                        r"R_Ax & 0\leq x\leq L/2\\"
                        r"R_B(L-x) & L/2\leq x\leq L"
                        r"\end{cases}"
                    )
                    st.markdown("Para este caso en la convención de la app:")
                    st.latex(r"M_x(x)=|M(x)|")

                elif caso_viga == "Carga distribuida uniforme":
                    st.markdown("Para una carga distribuida uniforme:")
                    st.latex(r"R_A=R_B=\frac{qL}{2}")
                    st.latex(r"|M|_{\max}=\frac{qL^2}{8}")
                    st.markdown("El momento absoluto a lo largo del vano es:")
                    st.latex(r"|M(x)|=R_Ax-\frac{q\,x^2}{2}")
                    st.markdown("Para este caso en la convención de la app:")
                    st.latex(r"M_x(x)=|M(x)|")

                elif caso_viga == "Voladizo con carga puntual en el extremo":
                    st.markdown("Para un voladizo con carga puntual en el extremo:")
                    st.latex(r"V_A=P")
                    st.latex(r"|M|_{\max}=PL")
                    st.markdown("El momento absoluto a lo largo de la viga es:")
                    st.latex(r"|M(x)|=P(L-x)")
                    st.markdown("Para este caso en la convención de la app:")
                    st.latex(r"M_x(x)=-|M(x)|")

                else:
                    st.markdown("Para un voladizo con carga distribuida uniforme:")
                    st.latex(r"V_A=qL")
                    st.latex(r"|M|_{\max}=\frac{qL^2}{2}")
                    st.markdown("El momento absoluto a lo largo de la viga es:")
                    st.latex(r"|M(x)|=\frac{q(L-x)^2}{2}")
                    st.markdown("Para este caso en la convención de la app:")
                    st.latex(r"M_x(x)=-|M(x)|")

                st.markdown("La tensión normal se obtiene con:")
                st.latex(r"\sigma(x,y)=\frac{M_x(x)}{I_x}\,y")
                st.markdown(
                    "Recordar que en la app se usa: **+x hacia la izquierda** y **+y hacia abajo**. "
                    "Además, el diagrama de momentos se dibuja del **lado traccionado**."
                )



    with sub_comp:

            st.subheader("Comparación de secciones")
            st.caption(
                "Observe cómo la forma y la distribución del material influyen en Ix, Wx y la tensión máxima."
            )

            modo_comp = st.segmented_control(
                "Tipo de comparación",
                options=["Dimensiones libres", "Misma cantidad de material"],
                default="Dimensiones libres",
                key="modo_comp"
            )

            Mcomp = st.number_input(
                "Momento flector común Mx [kN·m]",
                value=20.0,
                step=1.0,
                format="%.2f",
                key="comp_Mx"
            )

            # -----------------------------------------------------
            # MODO A: DIMENSIONES LIBRES
            # -----------------------------------------------------
            if modo_comp == "Dimensiones libres":
                st.markdown(
                    '<div class="compact-card">'
                    '<b>Comparación libre:</b> cada sección conserva las dimensiones que usted ingrese. '
                    'Esto permite comparar casos reales, aunque las cantidades de material sean diferentes.'
                    '</div>',
                    unsafe_allow_html=True
                )

                st.markdown("### Geometrías a comparar")

                c1, c2 = st.columns(2, gap="large")

                with c1:
                    st.markdown("#### Rectangular maciza")
                    r1, r2 = st.columns(2)
                    with r1:
                        br = st.number_input(
                            "b [cm]", min_value=0.1, value=20.0, step=1.0,
                            key="comp_rect_b"
                        )
                    with r2:
                        hr = st.number_input(
                            "h [cm]", min_value=0.1, value=40.0, step=1.0,
                            key="comp_rect_h"
                        )

                with c2:
                    st.markdown("#### Circular maciza")
                    dc = st.number_input(
                        "d [cm]", min_value=0.1, value=30.0, step=1.0,
                        key="comp_circ_d"
                    )

                c3, c4 = st.columns(2, gap="large")

                with c3:
                    st.markdown("#### Tubular circular")
                    t1, t2 = st.columns(2)
                    with t1:
                        Dt = st.number_input(
                            "D [cm]", min_value=0.2, value=30.0, step=1.0,
                            key="comp_tub_D"
                        )
                    with t2:
                        dit = st.number_input(
                            "d interior [cm]", min_value=0.1, value=20.0, step=1.0,
                            key="comp_tub_di"
                        )
                    if dit >= Dt:
                        st.error("En la sección tubular debe cumplirse d interior < D.")
                        st.stop()

                with c4:
                    st.markdown("#### Doble T")
                    d1, d2 = st.columns(2)
                    with d1:
                        hdt = st.number_input(
                            "h [cm]", min_value=1.0, value=40.0, step=1.0,
                            key="comp_dt_h"
                        )
                        twdt = st.number_input(
                            "tw [cm]", min_value=0.1, value=1.0, step=0.1,
                            key="comp_dt_tw"
                        )
                    with d2:
                        bfdt = st.number_input(
                            "bf [cm]", min_value=0.2, value=20.0, step=1.0,
                            key="comp_dt_bf"
                        )
                        tfdt = st.number_input(
                            "tf [cm]", min_value=0.1, value=2.0, step=0.1,
                            key="comp_dt_tf"
                        )
                    if 2*tfdt >= hdt:
                        st.error("En la doble T debe cumplirse 2·tf < h.")
                        st.stop()
                    if twdt >= bfdt:
                        st.error("En la doble T debe cumplirse tw < bf.")
                        st.stop()

            # -----------------------------------------------------
            # MODO B: MISMA CANTIDAD DE MATERIAL
            # -----------------------------------------------------
            else:
                st.markdown(
                    '<div class="compact-card">'
                    '<b>Misma cantidad de material:</b> se supone el mismo material y se fija la misma '
                    '<b>área transversal A</b> para las cuatro secciones. '
                    'De esta manera se aísla mejor el efecto de la <b>forma geométrica</b>.'
                    '</div>',
                    unsafe_allow_html=True
                )

                A_obj = st.number_input(
                    "Área común A [cm²]",
                    min_value=1.0,
                    value=80.0,
                    step=5.0,
                    key="comp_A_obj"
                )

                st.markdown("### Proporciones geométricas")

                p1, p2 = st.columns(2, gap="large")

                with p1:
                    st.markdown("#### Rectangular maciza")
                    relacion_hb = st.number_input(
                        "Relación h / b",
                        min_value=0.2,
                        value=2.0,
                        step=0.1,
                        key="comp_hb"
                    )

                    # A = b*h = r*b²
                    br = np.sqrt(A_obj / relacion_hb)
                    hr = relacion_hb * br

                    st.caption(f"Dimensiones resultantes: b = {br:.2f} cm · h = {hr:.2f} cm")

                    st.markdown("#### Tubular circular")
                    relacion_dD = st.slider(
                        "Relación d / D",
                        min_value=0.10,
                        max_value=0.90,
                        value=0.65,
                        step=0.05,
                        key="comp_dD"
                    )

                    # A = pi/4 * D² * (1-k²)
                    Dt = np.sqrt(4*A_obj / (np.pi*(1-relacion_dD**2)))
                    dit = relacion_dD * Dt

                    st.caption(f"Dimensiones resultantes: D = {Dt:.2f} cm · d = {dit:.2f} cm")

                with p2:
                    st.markdown("#### Circular maciza")
                    # A = pi d²/4
                    dc = np.sqrt(4*A_obj/np.pi)
                    st.caption(f"Diámetro resultante: d = {dc:.2f} cm")

                    st.markdown("#### Doble T")
                    st.caption("Las proporciones se expresan respecto de la altura total h.")

                    q1, q2 = st.columns(2)
                    with q1:
                        alpha_bf = st.number_input(
                            "bf / h",
                            min_value=0.10,
                            max_value=1.00,
                            value=0.50,
                            step=0.05,
                            key="comp_alpha_bf"
                        )
                        gamma_tw = st.number_input(
                            "tw / h",
                            min_value=0.005,
                            max_value=0.30,
                            value=0.025,
                            step=0.005,
                            format="%.3f",
                            key="comp_gamma_tw"
                        )
                    with q2:
                        beta_tf = st.number_input(
                            "tf / h",
                            min_value=0.01,
                            max_value=0.24,
                            value=0.05,
                            step=0.01,
                            key="comp_beta_tf"
                        )

                    coef_area = 2*alpha_bf*beta_tf + gamma_tw*(1-2*beta_tf)

                    if coef_area <= 0 or 2*beta_tf >= 1 or gamma_tw >= alpha_bf:
                        st.error("Las proporciones elegidas para la doble T no son geométricamente válidas.")
                        st.stop()

                    # A = h² * coef_area
                    hdt = np.sqrt(A_obj/coef_area)
                    bfdt = alpha_bf*hdt
                    tfdt = beta_tf*hdt
                    twdt = gamma_tw*hdt

                    st.caption(
                        f"Dimensiones resultantes: h = {hdt:.2f} cm · bf = {bfdt:.2f} cm · "
                        f"tf = {tfdt:.2f} cm · tw = {twdt:.2f} cm"
                    )

            # -----------------------------------------------------
            # PROPIEDADES DE LAS CUATRO SECCIONES
            # -----------------------------------------------------
            vals_rect = {"b_cm": br, "h_cm": hr}
            Ix_r, Wx_r, y_r = propiedades_seccion("Rectangular maciza", vals_rect)
            A_r = (br/100)*(hr/100)

            vals_circ = {"d_cm": dc}
            Ix_c, Wx_c, y_c = propiedades_seccion("Circular maciza", vals_circ)
            A_c = np.pi*(dc/100)**2/4

            vals_tub = {"D_cm": Dt, "di_cm": dit}
            Ix_t, Wx_t, y_t = propiedades_seccion("Tubular circular", vals_tub)
            A_t = np.pi*((Dt/100)**2 - (dit/100)**2)/4

            vals_dt = {"h_cm": hdt, "bf_cm": bfdt, "tf_cm": tfdt, "tw_cm": twdt}
            Ix_d, Wx_d, y_d = propiedades_seccion("Doble T", vals_dt)
            A_d = (
                2*(bfdt/100)*(tfdt/100)
                + (twdt/100)*((hdt-2*tfdt)/100)
            )

            props = [
                ("Rectangular", Ix_r, Wx_r, A_r),
                ("Circular", Ix_c, Wx_c, A_c),
                ("Tubular", Ix_t, Wx_t, A_t),
                ("Doble T", Ix_d, Wx_d, A_d),
            ]

            comp_data = []

            for nombre, Ix_i, Wx_i, A_i in props:
                sigma_max = abs(Mcomp*1e3/Wx_i)/1e6 if Wx_i != 0 else 0.0
                eficiencia_I = Ix_i/A_i if A_i != 0 else 0.0
                eficiencia_W = Wx_i/A_i if A_i != 0 else 0.0

                comp_data.append({
                    "nombre": nombre,
                    "Ix": Ix_i,
                    "Wx": Wx_i,
                    "A": A_i,
                    "sigma": sigma_max,
                    "I_A": eficiencia_I,
                    "W_A": eficiencia_W,
                })

            # -----------------------------------------------------
            # RESULTADOS
            # -----------------------------------------------------
            st.markdown("### Resultados comparativos")

            cols = st.columns(4)

            for col, item in zip(cols, comp_data):
                with col:
                    st.markdown(f"#### {item['nombre']}")

                    st.markdown(
                        f"""<div class="result-card">
                        <div class="result-label">Área A</div>
                        <div class="result-value">{item['A']*1e4:,.1f} cm²</div>
                        </div>""",
                        unsafe_allow_html=True
                    )
                    st.markdown("<div style='height:0.30rem'></div>", unsafe_allow_html=True)

                    st.markdown(
                        f"""<div class="result-card">
                        <div class="result-label">Ix</div>
                        <div class="result-value">{item['Ix']*1e8:,.1f} cm⁴</div>
                        </div>""",
                        unsafe_allow_html=True
                    )
                    st.markdown("<div style='height:0.30rem'></div>", unsafe_allow_html=True)

                    st.markdown(
                        f"""<div class="result-card">
                        <div class="result-label">Wx</div>
                        <div class="result-value">{item['Wx']*1e6:,.1f} cm³</div>
                        </div>""",
                        unsafe_allow_html=True
                    )
                    st.markdown("<div style='height:0.30rem'></div>", unsafe_allow_html=True)

                    st.markdown(
                        f"""<div class="result-card">
                        <div class="result-label">|σ|max</div>
                        <div class="result-value">{item['sigma']:.3f} MPa</div>
                        </div>""",
                        unsafe_allow_html=True
                    )

            # -----------------------------------------------------
            # GRÁFICOS COMPARATIVOS
            # -----------------------------------------------------
            nombres = [d["nombre"] for d in comp_data]
            Ix_vals = np.array([d["Ix"]*1e8 for d in comp_data])
            Wx_vals = np.array([d["Wx"]*1e6 for d in comp_data])
            sig_vals = np.array([d["sigma"] for d in comp_data])
            WA_vals = np.array([d["W_A"]*1e2 for d in comp_data])

            st.markdown("### Influencia de la geometría")

            g1, g2 = st.columns(2, gap="large")

            with g1:
                figI, axI = plt.subplots(figsize=(6.0, 3.8))
                axI.bar(nombres, Ix_vals)
                axI.set_ylabel("Ix [cm⁴]")
                axI.set_title("Momento de inercia")
                axI.grid(axis="y", alpha=0.2)
                axI.tick_params(axis="x", rotation=20)
                st.pyplot(figI, width="stretch")

            with g2:
                figS, axS = plt.subplots(figsize=(6.0, 3.8))
                axS.bar(nombres, sig_vals)
                axS.set_ylabel("|σ|max [MPa]")
                axS.set_title("Tensión máxima para el mismo Mx")
                axS.grid(axis="y", alpha=0.2)
                axS.tick_params(axis="x", rotation=20)
                st.pyplot(figS, width="stretch")

            g3, g4 = st.columns(2, gap="large")

            with g3:
                figW, axW = plt.subplots(figsize=(6.0, 3.8))
                axW.bar(nombres, Wx_vals)
                axW.set_ylabel("Wx [cm³]")
                axW.set_title("Módulo resistente")
                axW.grid(axis="y", alpha=0.2)
                axW.tick_params(axis="x", rotation=20)
                st.pyplot(figW, width="stretch")

            with g4:
                figE, axE = plt.subplots(figsize=(6.0, 3.8))
                axE.bar(nombres, WA_vals)
                axE.set_ylabel("Wx / A [cm]")
                axE.set_title("Eficiencia resistente por área")
                axE.grid(axis="y", alpha=0.2)
                axE.tick_params(axis="x", rotation=20)
                st.pyplot(figE, width="stretch")

            # -----------------------------------------------------
            # INTERPRETACIÓN AUTOMÁTICA
            # -----------------------------------------------------
            mejor_W = max(comp_data, key=lambda d: d["Wx"])
            menor_sigma = min(comp_data, key=lambda d: d["sigma"])
            mejor_ef = max(comp_data, key=lambda d: d["W_A"])

            st.markdown("### Interpretación")

            if modo_comp == "Misma cantidad de material":
                st.markdown(
                    f"""
                    Como las cuatro secciones tienen prácticamente la **misma área**, la comparación permite
                    observar directamente el efecto de la **forma** y de la ubicación del material respecto
                    del eje neutro.

                    - Mayor **Wx**: **{mejor_W['nombre']}**
                    - Menor **|σmax|**: **{menor_sigma['nombre']}**
                    - Mayor **Wx/A**: **{mejor_ef['nombre']}**
                    """
                )
            else:
                st.markdown(
                    f"""
                    Para las dimensiones ingresadas:

                    - Mayor **Wx**: **{mejor_W['nombre']}**
                    - Menor **|σmax|**: **{menor_sigma['nombre']}**
                    - Mayor eficiencia **Wx/A**: **{mejor_ef['nombre']}**
                    """
                )

            st.markdown(
                '<div class="compact-card">'
                '<b>Concepto:</b> el material ubicado lejos del eje neutro tiene una influencia '
                'muy importante sobre Ix y Wx. Por eso una sección puede ser más eficiente en flexión '
                'sin necesariamente utilizar más material.'
                '</div>',
                unsafe_allow_html=True
            )

            with st.expander("📘 ¿Qué estamos comparando?"):
                st.markdown("La tensión extrema se calcula mediante:")
                st.latex(r"|\sigma_{\max}|=\frac{|M_x|}{W_x}")
                st.markdown(
                    "Por lo tanto, para un mismo momento flector, **a mayor módulo resistente Wx, "
                    "menor tensión máxima**."
                )
                st.markdown(
                    "Cuando se selecciona **Misma cantidad de material**, se impone la misma área transversal "
                    "y se supone el mismo material. Así puede analizarse con mayor claridad el efecto de la forma."
                )



    with sub_verif:

            st.subheader("Verificación por tensión admisible")
            st.caption(
                "Compruebe si una sección resiste el momento aplicado de acuerdo con una tensión admisible."
            )

            cM, cS = st.columns(2)

            with cM:
                M_ver = st.number_input(
                    "Momento flector Mx [kN·m]",
                    value=20.0,
                    step=1.0,
                    format="%.2f",
                    key="ver_M"
                )

            with cS:
                sigma_adm = st.number_input(
                    "Tensión admisible σadm [MPa]",
                    min_value=0.1,
                    value=160.0,
                    step=5.0,
                    key="ver_sigma_adm"
                )

            st.markdown("### Sección a verificar")
            seccion_ver, vals_ver = entrada_geometria("ver")

            Ix_ver, Wx_ver, yext_ver = propiedades_seccion(seccion_ver, vals_ver)

            sigma_calc = abs(M_ver*1e3/Wx_ver)/1e6
            eta = sigma_calc/sigma_adm
            W_req_m3 = abs(M_ver*1e3)/(sigma_adm*1e6)
            W_req_cm3 = W_req_m3*1e6
            margen = sigma_adm - sigma_calc

            verifica = sigma_calc <= sigma_adm

            if verifica:
                st.success("✅ **LA SECCIÓN VERIFICA**")
            else:
                st.error("❌ **LA SECCIÓN NO VERIFICA**")

            st.markdown("### Resultados")

            r1, r2, r3, r4 = st.columns(4)
            card(r1, "Wx disponible", f"{Wx_ver*1e6:,.1f} cm³")
            card(r2, "Wx requerido", f"{W_req_cm3:,.1f} cm³")
            card(r3, "|σ|max", f"{sigma_calc:.3f} MPa")
            card(r4, "σadm", f"{sigma_adm:.3f} MPa")

            st.markdown("### Índice de utilización")

            utilizacion_pct = eta*100

            u1, u2, u3 = st.columns(3)
            card(u1, "η = σ / σadm", f"{eta:.3f}")
            card(u2, "Utilización", f"{utilizacion_pct:.1f} %")
            card(u3, "Margen", f"{margen:.3f} MPa")

            # Barra: se limita visualmente al 100 %, aunque el valor real se informa arriba
            st.progress(min(float(eta), 1.0))

            if eta <= 1:
                st.caption(
                    f"La tensión calculada utiliza aproximadamente el {utilizacion_pct:.1f}% "
                    "de la tensión admisible."
                )
            else:
                st.caption(
                    f"La tensión calculada supera la admisible en aproximadamente "
                    f"{(eta-1)*100:.1f}%."
                )

            # -----------------------------------------------------
            # VISUALIZACIÓN DE LA SECCIÓN
            # -----------------------------------------------------
            st.markdown("### Distribución de tensiones")

            figv, axv = plt.subplots(figsize=(7.5, 4.8))
            dibujar_seccion(
                axv,
                seccion_ver,
                vals_ver,
                M_ver,
                y_sel=None,
                stress_diagram=True
            )
            st.pyplot(figv, width="stretch")

            # -----------------------------------------------------
            # DESARROLLO
            # -----------------------------------------------------
            with st.expander("📘 Desarrollo de la verificación"):
                st.markdown("La condición de verificación es:")
                st.latex(r"|\sigma_{\max}|\leq\sigma_{adm}")

                st.markdown("La tensión extrema se obtiene mediante:")
                st.latex(r"|\sigma_{\max}|=\frac{|M_x|}{W_x}")

                st.markdown("El módulo resistente mínimo requerido es:")
                st.latex(r"W_{req}=\frac{|M_x|}{\sigma_{adm}}")

                st.markdown("Y el índice de utilización:")
                st.latex(r"\eta=\frac{|\sigma_{\max}|}{\sigma_{adm}}")

                st.markdown(
                    "- Si **η ≤ 1**: **verifica**.\n"
                    "- Si **η > 1**: **no verifica**."
                )

                st.markdown(
                    "Esta herramienta se plantea con finalidad **didáctica** para estudiar la relación "
                    "entre momento flector, geometría de la sección y tensión normal."
                )




# =========================================================
# PESTAÑA PRINCIPAL - FLEXIÓN OBLICUA
# =========================================================
with tab_oblicua:
    st.subheader("Flexión oblicua")
    st.caption(
        "Secciones con dos ejes de simetría, un eje de simetría y secciones no simétricas."
    )

    modo_oblicua = st.segmented_control(
        "Modo de trabajo",
        options=["Explorar", "Ejercicio guiado"],
        default="Explorar",
        key="obl_modo_trabajo"
    )

    familia_ob = st.segmented_control(
        "Familia de sección",
        options=[
            "Dos ejes de simetría",
            "Un eje de simetría",
            "Sin ejes de simetría"
        ],
        default="Dos ejes de simetría",
        key="obl_familia"
    )

    if familia_ob == "Dos ejes de simetría":
        st.markdown(
            '<div class="compact-card">'
            '<b>Dos ejes de simetría:</b> los ejes centroidales x-y son ejes principales '
            'y el producto de inercia es nulo.'
            '</div>',
            unsafe_allow_html=True
        )
    elif familia_ob == "Un eje de simetría":
        st.markdown(
            '<div class="compact-card">'
            '<b>Un eje de simetría:</b> si uno de los ejes centroidales coincide con el eje '
            'de simetría, x-y también son ejes principales y el producto de inercia es nulo.'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="compact-card">'
            '<b>Sección no simétrica:</b> los ejes centroidales x-y no son, en general, '
            'ejes principales. Se utiliza el <b>Círculo de Mohr–Land</b> para obtener '
            'los ejes principales u-v antes de resolver la flexión.'
            '</div>',
            unsafe_allow_html=True
        )

    # =====================================================
    # DATOS DE ENTRADA
    # =====================================================
    st.markdown("### Datos de entrada")
    cgeom, cmom = st.columns(2, gap="large")

    with cgeom:
        st.markdown("#### Sección")

        if familia_ob == "Dos ejes de simetría":
            tipo_ob = st.selectbox(
                "Tipo de sección",
                ["Rectangular maciza", "Circular maciza"],
                key="obl_tipo_2ejes"
            )

            if tipo_ob == "Rectangular maciza":
                g1, g2 = st.columns(2)
                with g1:
                    b_ob = st.number_input(
                        "Base b [cm]", min_value=0.1,
                        value=20.0, step=1.0, key="obl_b"
                    )
                with g2:
                    h_ob = st.number_input(
                        "Altura h [cm]", min_value=0.1,
                        value=40.0, step=1.0, key="obl_h"
                    )
                d_ob = None

            else:
                d_ob = st.number_input(
                    "Diámetro d [cm]", min_value=0.1,
                    value=30.0, step=1.0, key="obl_d"
                )
                b_ob = d_ob
                h_ob = d_ob

        elif familia_ob == "Un eje de simetría":
            tipo_ob = "Sección T"
            st.caption("Sección T simétrica respecto del eje vertical.")

            g1, g2 = st.columns(2)
            with g1:
                bf_ob = st.number_input(
                    "Ancho de ala bf [cm]", min_value=0.1,
                    value=30.0, step=1.0, key="obl_t_bf"
                )
                tw_ob = st.number_input(
                    "Espesor de alma tw [cm]", min_value=0.1,
                    value=6.0, step=0.5, key="obl_t_tw"
                )
            with g2:
                hT_ob = st.number_input(
                    "Altura total h [cm]", min_value=0.1,
                    value=40.0, step=1.0, key="obl_t_h"
                )
                tf_ob = st.number_input(
                    "Espesor de ala tf [cm]", min_value=0.1,
                    value=6.0, step=0.5, key="obl_t_tf"
                )

            if tw_ob >= bf_ob or tf_ob >= hT_ob:
                st.error("Para una sección T válida debe cumplirse tw < bf y tf < h.")
                st.stop()

            b_ob = bf_ob
            h_ob = hT_ob
            d_ob = None

        else:
            tipo_ob = "Sección L"
            st.caption("Sección L formada por dos alas rectangulares.")

            g1, g2 = st.columns(2)
            with g1:
                B_ob = st.number_input(
                    "Ancho total B [cm]", min_value=0.1,
                    value=30.0, step=1.0, key="obl_l_B"
                )
                tv_ob = st.number_input(
                    "Espesor ala vertical tv [cm]", min_value=0.1,
                    value=6.0, step=0.5, key="obl_l_tv"
                )
            with g2:
                H_ob = st.number_input(
                    "Altura total H [cm]", min_value=0.1,
                    value=40.0, step=1.0, key="obl_l_H"
                )
                th_ob = st.number_input(
                    "Espesor ala horizontal th [cm]", min_value=0.1,
                    value=6.0, step=0.5, key="obl_l_th"
                )

            if tv_ob >= B_ob or th_ob >= H_ob:
                st.error("Para una sección L válida debe cumplirse tv < B y th < H.")
                st.stop()

            b_ob = B_ob
            h_ob = H_ob
            d_ob = None

    with cmom:
        st.markdown("#### Momento flector")

        modo_momento_ob = st.segmented_control(
            "Entrada de momentos",
            options=["Mx y My", "M y ángulo θ"],
            default="Mx y My",
            key="obl_modo_momento"
        )

        if modo_momento_ob == "Mx y My":
            m1, m2 = st.columns(2)
            with m1:
                Mx_ob = st.number_input(
                    "Mx [kN·m]", value=20.0,
                    step=1.0, format="%.2f", key="obl_Mx"
                )
            with m2:
                My_ob = st.number_input(
                    "My [kN·m]", value=10.0,
                    step=1.0, format="%.2f", key="obl_My"
                )

            M_ob = float(np.hypot(Mx_ob, My_ob))
            theta_ob = (
                float(np.degrees(np.arctan2(My_ob, Mx_ob)))
                if M_ob > 1e-12 else 0.0
            )

        else:
            M_ob = st.number_input(
                "Magnitud M [kN·m]",
                min_value=0.0, value=20.0,
                step=1.0, format="%.2f", key="obl_M"
            )
            theta_ob = st.slider(
                "Ángulo θ respecto del eje x [°]",
                min_value=-180, max_value=180,
                value=30, step=1, key="obl_theta"
            )

            theta_rad = np.radians(theta_ob)
            Mx_ob = M_ob * np.cos(theta_rad)
            My_ob = M_ob * np.sin(theta_rad)

            q1, q2 = st.columns(2)
            card(q1, "Mx", f"{Mx_ob:.3f} kN·m")
            card(q2, "My", f"{My_ob:.3f} kN·m")

    Mx_Nm = Mx_ob * 1e3
    My_Nm = My_ob * 1e3

    # =====================================================
    # GEOMETRÍA E INERCIAS
    # Todas las propiedades geométricas se calculan primero
    # en cm, cm² y cm⁴ para facilitar su lectura didáctica.
    # =====================================================
    Ixy_cm4 = 0.0
    alpha_pr_deg = 0.0
    alpha_pr = 0.0
    xbar_local = 0.0
    ybar_local = 0.0
    outline_course = None

    if tipo_ob == "Rectangular maciza":
        A_cm2 = b_ob * h_ob
        Ix_cm4 = b_ob * h_ob**3 / 12.0
        Iy_cm4 = h_ob * b_ob**3 / 12.0

        vertices_course = [
            (+b_ob/2, -h_ob/2),
            (-b_ob/2, -h_ob/2),
            (-b_ob/2, +h_ob/2),
            (+b_ob/2, +h_ob/2),
        ]
        outline_course = vertices_course + [vertices_course[0]]

    elif tipo_ob == "Circular maciza":
        A_cm2 = np.pi * d_ob**2 / 4.0
        Ix_cm4 = np.pi * d_ob**4 / 64.0
        Iy_cm4 = Ix_cm4
        vertices_course = []

    elif tipo_ob == "Sección T":
        # Ala superior + alma debajo del ala, sin superposición.
        A1 = bf_ob * tf_ob
        A2 = tw_ob * (hT_ob - tf_ob)
        A_cm2 = A1 + A2

        y1 = tf_ob / 2.0
        y2 = tf_ob + (hT_ob - tf_ob) / 2.0
        ybar_local = (A1*y1 + A2*y2) / A_cm2

        Ix_cm4 = (
            bf_ob*tf_ob**3/12.0 + A1*(y1-ybar_local)**2
            + tw_ob*(hT_ob-tf_ob)**3/12.0 + A2*(y2-ybar_local)**2
        )
        Iy_cm4 = (
            tf_ob*bf_ob**3/12.0
            + (hT_ob-tf_ob)*tw_ob**3/12.0
        )

        ytop = -ybar_local
        yfb = tf_ob - ybar_local
        ybot = hT_ob - ybar_local

        vertices_course = [
            (+bf_ob/2, ytop),
            (-bf_ob/2, ytop),
            (-bf_ob/2, yfb),
            (-tw_ob/2, yfb),
            (-tw_ob/2, ybot),
            (+tw_ob/2, ybot),
            (+tw_ob/2, yfb),
            (+bf_ob/2, yfb),
        ]
        outline_course = vertices_course + [vertices_course[0]]

    else:
        # Sección L: ala horizontal superior + tramo vertical debajo,
        # evitando doble conteo de la zona común.
        A1 = B_ob * th_ob
        A2 = tv_ob * (H_ob - th_ob)
        A_cm2 = A1 + A2

        x1 = B_ob / 2.0
        y1 = th_ob / 2.0
        x2 = B_ob - tv_ob/2.0
        y2 = th_ob + (H_ob-th_ob)/2.0

        xbar_local = (A1*x1 + A2*x2) / A_cm2
        ybar_local = (A1*y1 + A2*y2) / A_cm2

        Ix_cm4 = (
            B_ob*th_ob**3/12.0 + A1*(y1-ybar_local)**2
            + tv_ob*(H_ob-th_ob)**3/12.0 + A2*(y2-ybar_local)**2
        )
        Iy_cm4 = (
            th_ob*B_ob**3/12.0 + A1*(x1-xbar_local)**2
            + (H_ob-th_ob)*tv_ob**3/12.0 + A2*(x2-xbar_local)**2
        )
        Ixy_cm4 = (
            A1*(x1-xbar_local)*(y1-ybar_local)
            + A2*(x2-xbar_local)*(y2-ybar_local)
        )

        # Contorno en coordenadas centroidales del curso (+x izquierda, +y abajo).
        local_poly = [
            (0.0, 0.0),
            (B_ob, 0.0),
            (B_ob, H_ob),
            (B_ob-tv_ob, H_ob),
            (B_ob-tv_ob, th_ob),
            (0.0, th_ob),
        ]

        vertices_course = [
            (x-xbar_local, y-ybar_local)
            for x, y in local_poly
        ]
        outline_course = vertices_course + [vertices_course[0]]

        # -------------------------------------------------
        # Círculo de Mohr–Land según la convención de la cátedra
        # -------------------------------------------------
        # Se dibuja verticalmente:
        # O -> X = Ix
        # X -> D = Iy
        # por lo tanto OD = Ix + Iy.
        #
        # Desde X se lleva Ixy horizontalmente:
        # Ixy > 0 hacia la derecha; Ixy < 0 hacia la izquierda.
        # El extremo es el polo P.
        Jpolar_cm4 = Ix_cm4 + Iy_cm4

        land_O = np.array([0.0, 0.0])
        land_X = np.array([0.0, Ix_cm4])
        land_D = np.array([0.0, Jpolar_cm4])
        land_C = np.array([0.0, Jpolar_cm4/2.0])
        land_R = Jpolar_cm4/2.0
        land_P = np.array([Ixy_cm4, Ix_cm4])

        # -------------------------------------------------
        # Eje de fuerzas f y eje neutro n
        # -------------------------------------------------
        # El eje de fuerzas f es perpendicular al vector momento M.
        if M_ob > 1e-12:
            theta_M = np.arctan2(My_ob, Mx_ob)
        else:
            theta_M = 0.0

        theta_f = theta_M + np.pi/2.0
        df = np.array([np.cos(theta_f), np.sin(theta_f)])

        # O-A: paralela al eje de fuerzas f.
        # Como O pertenece a la circunferencia, la segunda intersección
        # se obtiene directamente.
        tA = 2.0*np.dot(land_C, df)
        if abs(tA) < 1e-12:
            land_A = land_O.copy()
        else:
            land_A = tA*df

        # A-P-B: la recta que une A con el polo P corta nuevamente
        # a la circunferencia en B.
        vAP = land_P - land_A
        aq = np.dot(vAP, vAP)

        if aq > 1e-18:
            bq = 2.0*np.dot(land_A-land_C, vAP)
            cq = np.dot(land_A-land_C, land_A-land_C) - land_R**2
            roots = np.roots([aq, bq, cq])
            roots_real = [
                float(np.real(r))
                for r in roots
                if abs(np.imag(r)) < 1e-8
            ]

            lambda_B = 0.0
            for rr in roots_real:
                if abs(rr) > 1e-7:
                    lambda_B = rr
                    break

            land_B = land_A + lambda_B*vAP
        else:
            land_B = land_A.copy()

        # O-B da la dirección conjugada de f, es decir el eje neutro n.
        theta_n_land = np.arctan2(land_B[1], land_B[0])
        theta_n_land_deg = np.degrees(theta_n_land)

        # Momento de inercia respecto del eje neutro.
        cn = np.cos(theta_n_land)
        sn = np.sin(theta_n_land)

        In_cm4 = (
            Ix_cm4*cn**2
            + Iy_cm4*sn**2
            - 2.0*Ixy_cm4*sn*cn
        )
        In_ob = In_cm4/1e8

        # Proyección del vector momento sobre el eje neutro.
        Mn_ob = (
            Mx_ob*np.cos(theta_n_land)
            + My_ob*np.sin(theta_n_land)
        )
        Mn_Nm = Mn_ob*1e3

        # Ángulo entre M y n, útil para la lectura didáctica.
        # Ángulo beta geométrico entre el plano de cargas f y el eje neutro n.
        # Se toma como el ángulo agudo entre ambas rectas: 0° <= beta <= 90°.
        beta_raw = theta_n_land - theta_f
        beta_raw = np.arctan2(np.sin(beta_raw), np.cos(beta_raw))

        # Ángulo entre rectas (sin orientación)
        beta_geom = abs(beta_raw)
        if beta_geom > np.pi/2:
            beta_geom = np.pi - beta_geom

        beta_fn = beta_geom
        beta_deg = np.degrees(beta_geom)

        # En la fórmula de un término se utiliza la magnitud positiva M·sen(beta).
        M_sen_beta_ob = M_ob * np.sin(beta_geom)
        M_sen_beta_Nm = M_sen_beta_ob * 1e3

        Mn_ob = M_sen_beta_ob
        Mn_Nm = M_sen_beta_Nm

        # Verificación de conjugación f-n.
        cf = np.cos(theta_f)
        sf = np.sin(theta_f)
        Ifn_check = (
            Iy_cm4*sf*sn
            + Ix_cm4*cf*cn
            - Ixy_cm4*(sf*cn + cf*sn)
        )

        # Variables de compatibilidad para el resto del programa.
        alpha_pr = 0.0
        alpha_pr_deg = 0.0
        Iu_cm4 = Ix_cm4
        Iv_cm4 = Iy_cm4
        Iuv_check_cm4 = Ixy_cm4

    Ix_ob = Ix_cm4 / 1e8
    Iy_ob = Iy_cm4 / 1e8

    if tipo_ob != "Sección L":
        Iu_cm4 = Ix_cm4
        Iv_cm4 = Iy_cm4
        Iuv_check_cm4 = 0.0

    Iu_ob = Iu_cm4 / 1e8
    Iv_ob = Iv_cm4 / 1e8

    # =====================================================
    # COMPONENTES DEL MOMENTO EN EJES PRINCIPALES
    # =====================================================
    ca = np.cos(alpha_pr)
    sa = np.sin(alpha_pr)

    Mu_ob = Mx_ob*ca + My_ob*sa
    Mv_ob = -Mx_ob*sa + My_ob*ca

    Mu_Nm = Mu_ob*1e3
    Mv_Nm = Mv_ob*1e3

    def xy_to_uv(x_cm, y_cm):
        u = x_cm*ca + y_cm*sa
        v = -x_cm*sa + y_cm*ca
        return u, v

    def sigma_ob_mpa(x_cm, y_cm):
        if tipo_ob == "Sección L":
            # Fórmula de un término con la convención de signos de la cátedra:
            # +x hacia la izquierda, +y hacia abajo y regla de la mano derecha.
            # Con esta convención:
            # sigma = -(Mn/In) * yn
            # yn = distancia algebraica perpendicular al eje neutro.
            yn_cm = (
                -x_cm*np.sin(theta_n_land)
                + y_cm*np.cos(theta_n_land)
            )
            return (
                -(Mn_Nm/In_ob)*(yn_cm/100.0)
            ) / 1e6

        u_cm, v_cm = xy_to_uv(x_cm, y_cm)
        u_m = u_cm/100.0
        v_m = v_cm/100.0
        return (
            (Mu_Nm/Iu_ob)*v_m
            - (Mv_Nm/Iv_ob)*u_m
        ) / 1e6

    # =====================================================
    # PUNTOS CRÍTICOS
    # =====================================================
    if tipo_ob == "Circular maciza":
        R_cm = d_ob/2.0

        # Para Ix=Iy, la dirección de máxima variación de sigma
        # es perpendicular al vector momento resultante.
        axcoef = -My_Nm/Iy_ob
        aycoef = Mx_Nm/Ix_ob
        norma = np.hypot(axcoef, aycoef)

        if norma > 1e-18:
            x_t = R_cm*axcoef/norma
            y_t = R_cm*aycoef/norma
            x_c = -x_t
            y_c = -y_t
            sigma_t_max = sigma_ob_mpa(x_t, y_t)
            sigma_c_max = sigma_ob_mpa(x_c, y_c)
        else:
            x_t = y_t = x_c = y_c = 0.0
            sigma_t_max = sigma_c_max = 0.0

        max_name = "Punto crítico de tracción"
        min_name = "Punto crítico de compresión"
        point_results = {
            max_name: sigma_t_max,
            min_name: sigma_c_max,
        }

    else:
        point_results = {
            f"P{i+1}": sigma_ob_mpa(xc, yc)
            for i, (xc, yc) in enumerate(vertices_course)
        }

        max_name = max(point_results, key=point_results.get)
        min_name = min(point_results, key=point_results.get)

        imax = int(max_name[1:]) - 1
        imin = int(min_name[1:]) - 1

        x_t, y_t = vertices_course[imax]
        x_c, y_c = vertices_course[imin]
        sigma_t_max = point_results[max_name]
        sigma_c_max = point_results[min_name]

        if tipo_ob == "Rectangular maciza":
            names_rect = {
                0: "Superior izquierda",
                1: "Superior derecha",
                2: "Inferior derecha",
                3: "Inferior izquierda",
            }
            max_name = names_rect[imax]
            min_name = names_rect[imin]
        elif tipo_ob == "Sección T":
            max_name = f"Vértice P{imax+1}"
            min_name = f"Vértice P{imin+1}"
        else:
            max_name = f"Vértice P{imax+1}"
            min_name = f"Vértice P{imin+1}"

    # =====================================================
    # ECUACIÓN LINEAL DEL CAMPO Y EJE NEUTRO
    # =====================================================
    # sigma = gx*x + gy*y en las coordenadas centroidales x-y.
    # Se obtiene a partir de las componentes principales.
    Acoef = Mu_Nm/Iu_ob
    Bcoef = Mv_Nm/Iv_ob

    gx = -Acoef*sa - Bcoef*ca
    gy =  Acoef*ca - Bcoef*sa

    if abs(gy) > 1e-18:
        slope_en = -gx/gy
        angle_en = np.degrees(np.arctan2(slope_en, 1.0))
    else:
        slope_en = None
        angle_en = 90.0

    # =====================================================
    # ESTADO CONCEPTUAL
    # =====================================================
    if abs(Mx_ob) > 1e-12 and abs(My_ob) > 1e-12:
        tipo_estado = "Flexión oblicua"
        st.success("✅ **Caso de flexión oblicua:** actúan simultáneamente Mx y My.")
    elif abs(Mx_ob) > 1e-12 or abs(My_ob) > 1e-12:
        tipo_estado = "Flexión simple"
        st.info("ℹ️ Solo actúa una componente de momento.")
    else:
        tipo_estado = "Sin flexión"
        st.warning("⚠️ No hay momento flector aplicado.")

    # =====================================================
    # PROPIEDADES GEOMÉTRICAS
    # =====================================================
    st.markdown("### Propiedades geométricas")

    if tipo_ob == "Sección L":
        pr1, pr2, pr3, pr4 = st.columns(4)
        card(pr1, "Ix", f"{Ix_cm4:,.1f} cm⁴")
        card(pr2, "Iy", f"{Iy_cm4:,.1f} cm⁴")
        card(pr3, "Ixy", f"{Ixy_cm4:,.1f} cm⁴")
        card(pr4, "Área", f"{A_cm2:,.1f} cm²")

        st.caption(
            f"Baricentro medido desde la esquina superior derecha adoptada: "
            f"xG = {xbar_local:.2f} cm · yG = {ybar_local:.2f} cm."
        )
    else:
        pr1, pr2, pr3 = st.columns(3)
        card(pr1, "Ix", f"{Ix_cm4:,.1f} cm⁴")
        card(pr2, "Iy", f"{Iy_cm4:,.1f} cm⁴")
        card(pr3, "Área", f"{A_cm2:,.1f} cm²")

        if tipo_ob == "Sección T":
            st.caption(
                f"El baricentro se encuentra a yG = {ybar_local:.2f} cm "
                f"medidos desde la cara superior."
            )

    # =====================================================
    # MOHR–LAND PARA SECCIÓN NO SIMÉTRICA
    # =====================================================
    if tipo_ob == "Sección L":
        st.markdown("### Círculo de Mohr–Land")

        st.markdown(
            '<div class="compact-card">'
            'Construcción según la convención de la cátedra: primero se lleva '
            '<b>Ix verticalmente</b> y a continuación <b>Iy</b>. '
            'Desde el extremo de Ix se representa <b>Ixy</b>: hacia la derecha '
            'si es positivo y hacia la izquierda si es negativo. Su extremo es '
            'el <b>polo P</b>.'
            '</div>',
            unsafe_allow_html=True
        )

        ml, mr = st.columns([1.25, 0.75], gap="large")

        with ml:
            figml, axml = plt.subplots(figsize=(5.3, 5.0))

            tt_land = np.linspace(0, 2*np.pi, 600)
            cx = land_C[0] + land_R*np.cos(tt_land)
            cy = land_C[1] + land_R*np.sin(tt_land)
            axml.plot(cx, cy, linewidth=1.8)

            # Diámetro vertical Ix + Iy
            axml.plot(
                [land_O[0], land_D[0]],
                [land_O[1], land_D[1]],
                linewidth=1.6
            )

            # Segmentos Ix e Iy
            axml.plot(
                [land_O[0], land_X[0]],
                [land_O[1], land_X[1]],
                linewidth=3.0
            )
            axml.plot(
                [land_X[0], land_D[0]],
                [land_X[1], land_D[1]],
                linewidth=2.0
            )

            # Ixy desde el extremo de Ix hasta P
            axml.plot(
                [land_X[0], land_P[0]],
                [land_X[1], land_P[1]],
                linewidth=2.2
            )

            # Puntos básicos
            for pt, lab in [
                (land_O, "O"),
                (land_X, "X"),
                (land_D, "D"),
                (land_P, "P"),
            ]:
                marker = "D" if lab == "P" else "o"
                size = 58 if lab == "P" else 38
                axml.scatter([pt[0]], [pt[1]], s=size, marker=marker, zorder=7)
                axml.annotate(
                    lab, xy=pt, xytext=(7, 5),
                    textcoords="offset points", fontsize=8.5
                )

            # Eje de fuerzas f: O-A
            axml.plot(
                [land_O[0], land_A[0]],
                [land_O[1], land_A[1]],
                linewidth=2.0
            )
            axml.scatter([land_A[0]], [land_A[1]], s=45, zorder=7)
            axml.annotate(
                "A", xy=land_A, xytext=(6, 5),
                textcoords="offset points", fontsize=9
            )

            # Cuerda A-P-B
            axml.plot(
                [land_A[0], land_B[0]],
                [land_A[1], land_B[1]],
                linewidth=1.8
            )
            axml.scatter([land_B[0]], [land_B[1]], s=45, zorder=7)
            axml.annotate(
                "B", xy=land_B, xytext=(6, 5),
                textcoords="offset points", fontsize=9
            )

            # Eje conjugado/neutro O-B
            axml.plot(
                [land_O[0], land_B[0]],
                [land_O[1], land_B[1]],
                linewidth=2.3
            )

            # Ángulo beta entre el plano de cargas f y el eje neutro n
            delta_beta_raw = np.arctan2(
                np.sin(theta_n_land - theta_f),
                np.cos(theta_n_land - theta_f)
            )

            # Arco correspondiente al ángulo geométrico agudo entre f y n
            if abs(delta_beta_raw) <= np.pi/2:
                delta_beta = delta_beta_raw
            else:
                delta_beta = delta_beta_raw - np.sign(delta_beta_raw)*np.pi

            rb = 0.16 * land_R
            angs_b = theta_f + np.linspace(0.0, delta_beta, 60)
            axml.plot(
                rb * np.cos(angs_b),
                rb * np.sin(angs_b),
                linewidth=1.25
            )
            ang_bm = theta_f + delta_beta / 2.0
            axml.text(
                1.18 * rb * np.cos(ang_bm),
                1.18 * rb * np.sin(ang_bm),
                "β",
                fontsize=10
            )

            # Etiquetas Ix, Iy e Ixy
            axml.annotate(
                "Ix",
                xy=((land_O[0]+land_X[0])/2,
                    (land_O[1]+land_X[1])/2),
                xytext=(-26, 0),
                textcoords="offset points",
                va="center", fontsize=9
            )
            axml.annotate(
                "Iy",
                xy=((land_X[0]+land_D[0])/2,
                    (land_X[1]+land_D[1])/2),
                xytext=(-26, 0),
                textcoords="offset points",
                va="center", fontsize=9
            )
            axml.annotate(
                "Ixy",
                xy=((land_X[0]+land_P[0])/2,
                    (land_X[1]+land_P[1])/2),
                xytext=(0, 8),
                textcoords="offset points",
                ha="center", fontsize=9
            )

            axml.text(
                land_A[0]*0.45,
                land_A[1]*0.45,
                "f",
                fontsize=10
            )
            axml.text(
                land_B[0]*0.48,
                land_B[1]*0.48,
                "n",
                fontsize=10
            )

            axml.set_title("Construcción de Mohr–Land", fontsize=10)
            axml.set_xlabel("Ixy positivo → derecha")
            axml.set_ylabel("Ix seguido de Iy")
            axml.set_aspect("equal", adjustable="datalim")
            axml.grid(alpha=0.10)

            st.pyplot(figml, width="stretch")

        with mr:
            st.markdown("#### Lectura")

            q1, q2 = st.columns(2)
            card(q1, "Ix", f"{Ix_cm4:,.1f} cm⁴")
            card(q2, "Iy", f"{Iy_cm4:,.1f} cm⁴")

            q3, q4 = st.columns(2)
            card(q3, "Ixy", f"{Ixy_cm4:,.1f} cm⁴")
            card(q4, "In", f"{In_cm4:,.1f} cm⁴")

            q5, q6 = st.columns(2)
            card(q5, "β", f"{beta_deg:.2f}°")
            card(q6, "M·senβ", f"{M_sen_beta_ob:.3f} kN·m")

            st.markdown(
                r"""
                **Construcción**

                1. \(O-X=I_x\)
                2. \(X-D=I_y\)
                3. desde \(X\): \(I_{xy}\) hasta el polo \(P\)
                4. \(O-A\) es paralelo al eje de fuerzas \(f\)
                5. la cuerda \(A-P-B\) corta nuevamente el círculo
                6. \(O-B\) determina el eje conjugado \(n\)

                En flexión oblicua, \(n\) es el **eje neutro**.
                """
            )

            st.caption(
                f"Comprobación numérica de conjugación f–n: "
                f"Ifn = {Ifn_check:.3e} cm⁴ ≈ 0. "
                f"El ángulo β es el formado por el plano de cargas f y el eje neutro n."
            )

        # -------------------------------------------------
        # Fórmula de un término
        # -------------------------------------------------
        st.markdown("#### Fórmula de un término")

        st.latex(r"\sigma=\frac{M\sin\beta}{I_n}\,y_n")

        ft1, ft2, ft3 = st.columns(3)
        card(ft1, "β", f"{beta_deg:.2f}°")
        card(ft2, "M·senβ", f"{M_sen_beta_ob:.3f} kN·m")
        card(ft3, "In", f"{In_cm4:,.1f} cm⁴")

        st.info(
            "Se utiliza directamente la componente **M·senβ**, con β medido entre el plano de cargas f y el eje neutro n. "
            "Luego la tensión en cada punto depende únicamente de su "
            "distancia algebraica perpendicular al eje neutro, yn. "
            "En esta app se adoptó la convención de la cátedra: "
            "+x hacia la izquierda, +y hacia abajo y signo de σ "
            "compatible con la regla de la mano derecha."
        )

        # -------------------------------------------------
        # Correspondencia con la sección real
        # -------------------------------------------------
        st.markdown("#### Correspondencia con la sección")

        figsec, axsec = plt.subplots(figsize=(4.6, 3.8))

        xo_sec = [-p[0] for p in outline_course]
        yo_sec = [-p[1] for p in outline_course]
        axsec.plot(xo_sec, yo_sec, linewidth=2.0)

        Ldir = 0.50*min(B_ob, H_ob)

        # Momento M
        mxv = -np.cos(theta_M)*Ldir
        myv = -np.sin(theta_M)*Ldir
        axsec.annotate(
            "",
            xy=(mxv, myv), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", linewidth=2.0)
        )
        axsec.text(mxv*1.08, myv*1.08, "M", fontsize=9)

        # Eje de fuerzas f, perpendicular a M
        fx = -np.cos(theta_f)*Ldir
        fy = -np.sin(theta_f)*Ldir
        axsec.plot([-fx, fx], [-fy, fy], linewidth=1.4)
        axsec.text(fx*1.08, fy*1.08, "f", fontsize=9)

        # Eje neutro n
        nx = -np.cos(theta_n_land)*Ldir
        ny = -np.sin(theta_n_land)*Ldir
        axsec.plot([-nx, nx], [-ny, ny], linewidth=2.2)
        axsec.text(nx*1.08, ny*1.08, "n", fontsize=9)

        # Proyección Mn sobre n
        mn_scale = 0.72*Ldir
        if M_ob > 1e-12:
            frac_mn = Mn_ob/M_ob
        else:
            frac_mn = 0.0

        pmx = -np.cos(theta_n_land)*mn_scale*frac_mn
        pmy = -np.sin(theta_n_land)*mn_scale*frac_mn

        axsec.annotate(
            "",
            xy=(pmx, pmy), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", linewidth=1.7)
        )
        axsec.text(pmx*1.08, pmy*1.08, "M·senβ", fontsize=8.5)

        axsec.scatter([0], [0], s=28, zorder=7)
        axsec.text(0.7, 0.7, "G", fontsize=9)

        mrg = 0.12*max(B_ob, H_ob)
        axsec.set_xlim(
            -max([p[0] for p in vertices_course])-mrg,
            -min([p[0] for p in vertices_course])+mrg
        )
        axsec.set_ylim(
            -max([p[1] for p in vertices_course])-mrg,
            -min([p[1] for p in vertices_course])+mrg
        )
        axsec.set_aspect("equal", adjustable="box")
        axsec.set_xticks([])
        axsec.set_yticks([])
        axsec.grid(alpha=0.08)

        sc1, sc2, sc3 = st.columns([1.2, 1.6, 1.2])
        with sc2:
            st.pyplot(figsec, width="stretch")

        st.caption(
            "M = momento resultante · f = plano de cargas perpendicular a M · "
            "n = eje neutro, conjugado de f · β = ángulo entre f y n · "
            "M·senβ = componente utilizada en la fórmula de un término."
        )

    # =====================================================
    # EJERCICIO GUIADO
    # =====================================================
    if modo_oblicua == "Ejercicio guiado":
        st.markdown("### Ejercicio guiado")

        if tipo_ob == "Sección L":
            e1, e2, e3 = st.columns(3)
            with e1:
                r1 = st.radio(
                    "1. En la sección L, ¿x-y son necesariamente principales?",
                    ["Sí", "No"],
                    key="obl_q_l1"
                )
            with e2:
                r2 = st.radio(
                    "2. ¿Qué herramienta usamos para hallar u-v?",
                    ["Círculo de Mohr–Land", "Solo el baricentro", "Diagrama de corte"],
                    key="obl_q_l2"
                )
            with e3:
                r3 = st.radio(
                    "3. Una vez ubicado el eje neutro, ¿qué hacemos con M?",
                    ["Lo proyectamos sobre n", "Lo anulamos", "Usamos solamente Mx"],
                    key="obl_q_l3"
                )

            if st.button("Mostrar corrección", key="obl_corregir_l"):
                st.success(
                    f"Respuestas: 1) No · 2) Círculo de Mohr–Land · "
                    f"3) Lo proyectamos sobre n. "
                    f"Tu resultado: {sum([r1=='No', r2=='Círculo de Mohr–Land', r3=='Lo proyectamos sobre n'])}/3."
                )
        else:
            e1, e2, e3 = st.columns(3)
            with e1:
                resp_tipo = st.radio(
                    "1. ¿Qué tipo de flexión hay?",
                    ["Flexión simple", "Flexión oblicua", "Sin flexión"],
                    key="obl_q_tipo"
                )
            with e2:
                resp_en = st.radio(
                    "2. El eje neutro:",
                    [
                        "Pasa por G",
                        "No pasa por G",
                        "Siempre coincide con x"
                    ],
                    key="obl_q_en"
                )
            with e3:
                resp_signo = st.radio(
                    "3. σ positiva representa:",
                    ["Tracción", "Compresión", "Tensión nula"],
                    key="obl_q_signo"
                )

            if st.button("Mostrar corrección", key="obl_corregir"):
                score = sum([
                    resp_tipo == tipo_estado,
                    resp_en == "Pasa por G",
                    resp_signo == "Tracción"
                ])
                st.success(f"Resultado: {score}/3.")

    # =====================================================
    # CAMPO DE TENSIONES
    # =====================================================
    st.markdown("### Distribución de tensiones en la sección")

    fig, ax = plt.subplots(figsize=(4.8, 3.7))

    if tipo_ob == "Rectangular maciza":
        xmin, xmax = -b_ob/2, b_ob/2
        ymin, ymax = -h_ob/2, h_ob/2

        x_course = np.linspace(xmin, xmax, 240)
        y_course = np.linspace(ymin, ymax, 260)
        Xc, Yc = np.meshgrid(x_course, y_course)
        mask_shape = np.ones_like(Xc, dtype=bool)

    elif tipo_ob == "Circular maciza":
        R = d_ob/2.0
        xmin, xmax = -R, R
        ymin, ymax = -R, R

        x_course = np.linspace(xmin, xmax, 250)
        y_course = np.linspace(ymin, ymax, 250)
        Xc, Yc = np.meshgrid(x_course, y_course)
        mask_shape = (Xc**2 + Yc**2) <= R**2

    elif tipo_ob == "Sección T":
        xmin, xmax = -bf_ob/2, bf_ob/2
        ymin, ymax = -ybar_local, hT_ob-ybar_local

        x_course = np.linspace(xmin, xmax, 280)
        y_course = np.linspace(ymin, ymax, 300)
        Xc, Yc = np.meshgrid(x_course, y_course)

        Ylocal = Yc + ybar_local
        mask_shape = (
            ((Ylocal >= 0) & (Ylocal <= tf_ob) & (np.abs(Xc) <= bf_ob/2))
            |
            ((Ylocal >= tf_ob) & (Ylocal <= hT_ob) & (np.abs(Xc) <= tw_ob/2))
        )

    else:
        xmin = -xbar_local
        xmax = B_ob-xbar_local
        ymin = -ybar_local
        ymax = H_ob-ybar_local

        x_course = np.linspace(xmin, xmax, 300)
        y_course = np.linspace(ymin, ymax, 320)
        Xc, Yc = np.meshgrid(x_course, y_course)

        Xlocal = Xc + xbar_local
        Ylocal = Yc + ybar_local

        mask_shape = (
            ((Ylocal >= 0) & (Ylocal <= th_ob) &
             (Xlocal >= 0) & (Xlocal <= B_ob))
            |
            ((Xlocal >= B_ob-tv_ob) & (Xlocal <= B_ob) &
             (Ylocal >= th_ob) & (Ylocal <= H_ob))
        )

    # Campo de tensiones
    if tipo_ob == "Sección L":
        Yn_c = (
            -Xc*np.sin(theta_n_land)
            + Yc*np.cos(theta_n_land)
        )
        Sigma_raw = (
            -(Mn_Nm/In_ob)*(Yn_c/100.0)
        ) / 1e6

        # Variables auxiliares para otros tipos de sección.
        Uc = Xc
        Vc = Yc
    else:
        # Coordenadas principales del mallado
        Uc = Xc*ca + Yc*sa
        Vc = -Xc*sa + Yc*ca

        Sigma_raw = (
            (Mu_Nm/Iu_ob)*(Vc/100.0)
            - (Mv_Nm/Iv_ob)*(Uc/100.0)
        ) / 1e6

    Sigma = np.ma.array(Sigma_raw, mask=~mask_shape)

    # Transformación solo para representación gráfica:
    # +x del curso hacia izquierda y +y hacia abajo.
    Xp = -Xc
    Yp = -Yc

    # Representación de signos en el mapa de colores.
    # Para la sección L se invierte únicamente la variable de representación
    # para que la zona de compresión/tracción coincida con la convención gráfica
    # de la cátedra, sin alterar los valores calculados de sigma.
    Sigma_plot = -Sigma if tipo_ob == "Sección L" else Sigma

    contour = ax.contourf(
        Xp, Yp, Sigma_plot,
        levels=21,
        cmap="coolwarm",
        alpha=0.82
    )

    # Contorno geométrico
    if tipo_ob == "Circular maciza":
        tt = np.linspace(0, 2*np.pi, 400)
        ax.plot(R*np.cos(tt), R*np.sin(tt), linewidth=2.0)
    else:
        xo = [-p[0] for p in outline_course]
        yo = [-p[1] for p in outline_course]
        ax.plot(xo, yo, linewidth=2.0)

    cbar = fig.colorbar(contour, ax=ax, pad=0.03)
    cbar.set_label("σ [MPa]")

    # Ejes centroidales x-y
    ax.axhline(0, linestyle="--", linewidth=0.9)
    ax.axvline(0, linestyle="--", linewidth=0.9)

    escala_axes = 0.36*min(b_ob, h_ob)
    ax.annotate(
        "", xy=(-escala_axes, 0), xytext=(0, 0),
        arrowprops=dict(arrowstyle="->", linewidth=1.4)
    )
    ax.text(-escala_axes*1.06, 0.7, "+x", fontsize=8.5, ha="center")

    ax.annotate(
        "", xy=(0, -escala_axes), xytext=(0, 0),
        arrowprops=dict(arrowstyle="->", linewidth=1.4)
    )
    ax.text(0.7, -escala_axes*1.05, "+y", fontsize=8.5, va="center")

    ax.scatter([0], [0], s=28, zorder=7)
    ax.text(0.7, 0.7, "G", fontsize=9)

    # Para la sección L no se dibujan ejes principales:
    # la resolución se realiza mediante Mohr–Land y fórmula de un término.

    # Vector momento
    if M_ob > 1e-12:
        escala_vec = 0.32*min(b_ob, h_ob)
        uxM = Mx_ob/M_ob
        uyM = My_ob/M_ob
        ax.annotate(
            "",
            xy=(-uxM*escala_vec, -uyM*escala_vec),
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", linewidth=2.0),
            zorder=8
        )
        ax.text(
            -uxM*escala_vec*1.10,
            -uyM*escala_vec*1.10,
            "M",
            fontsize=9,
            ha="center"
        )

    # Eje neutro
    if tipo_ob == "Sección L":
        # Para la sección no simétrica se representa la dirección
        # obtenida gráficamente mediante Mohr–Land.
        Ln = 0.65*max(b_ob, h_ob)
        xn = np.cos(theta_n_land)*Ln
        yn = np.sin(theta_n_land)*Ln
        ax.plot(
            [xn, -xn], [yn, -yn],
            linewidth=2.25
        )
    elif np.any(mask_shape) and np.max(Sigma_plot) > 0 and np.min(Sigma_plot) < 0:
        ax.contour(
            Xp, Yp, Sigma_plot,
            levels=[0],
            linewidths=2.25
        )

    # Puntos críticos
    ax.scatter(
        [-x_t], [-y_t],
        s=90, marker="o",
        edgecolors="black", linewidths=1.1,
        zorder=10
    )
    ax.scatter(
        [-x_c], [-y_c],
        s=90, marker="s",
        edgecolors="black", linewidths=1.1,
        zorder=10
    )

    # -------------------------------------------------
    # Diagrama lineal de tensiones superpuesto a la sección
    # -------------------------------------------------
    if tipo_ob == "Sección L":
        theta_diag = theta_n_land
    else:
        if slope_en is None:
            theta_diag = np.pi/2
        else:
            theta_diag = np.arctan(slope_en)

    # t: dirección del eje neutro - n: dirección perpendicular al eje neutro
    tx_d = np.cos(theta_diag)
    ty_d = np.sin(theta_diag)
    nx_d = -np.sin(theta_diag)
    ny_d =  np.cos(theta_diag)

    def proj_diag(xc, yc):
        return xc*nx_d + yc*ny_d

    if tipo_ob == "Circular maciza":
        dist_pos_diag = d_ob / 2.0
        dist_neg_diag = d_ob / 2.0
    else:
        projs_diag = [proj_diag(xv, yv) for xv, yv in vertices_course]
        dist_pos_diag = max(projs_diag)
        dist_neg_diag = -min(projs_diag)

    dist_pos_diag = max(float(dist_pos_diag), 1e-6)
    dist_neg_diag = max(float(dist_neg_diag), 1e-6)

    # Valores didácticos: distancias extremas medidas perpendicularmente al E.N.
    yn_pos = dist_pos_diag
    yn_neg = dist_neg_diag

    # Pendiente única del diagrama (misma en ambos lados)
    # porque el módulo E no cambia.
    psi_draw = 0.5 * (
        abs(float(sigma_t_max)) / dist_pos_diag
        + abs(float(sigma_c_max)) / dist_neg_diag
    )

    sig_pos_draw = psi_draw * dist_pos_diag
    sig_neg_draw = -psi_draw * dist_neg_diag

    # Escala del ancho del diagrama sobre la figura
    sigma_max_draw = max(abs(sig_pos_draw), abs(sig_neg_draw), 1e-6)
    amp_scale = 0.18 * max(b_ob, h_ob) / sigma_max_draw

    # Punto de tensión nula sobre el eje neutro, desplazado un poco
    # para no tapar el baricentro.
    shift_t = 0.18 * max(b_ob, h_ob)
    z0x = shift_t * tx_d
    z0y = shift_t * ty_d

    # Eje del diagrama: perpendicular al eje neutro
    p_pos = np.array([z0x + nx_d * dist_pos_diag, z0y + ny_d * dist_pos_diag])
    p_neg = np.array([z0x - nx_d * dist_neg_diag, z0y - ny_d * dist_neg_diag])

    # Extremos de las tensiones:
    # apertura en dirección del eje neutro
    e_pos = p_pos + np.array([tx_d, ty_d]) * amp_scale * sig_pos_draw
    e_neg = p_neg + np.array([tx_d, ty_d]) * amp_scale * sig_neg_draw

    # Pasamos a coordenadas de ploteo (x_plot=-x, y_plot=-y)
    z0p = np.array([-z0x, -z0y])
    p_pos_p = np.array([-p_pos[0], -p_pos[1]])
    p_neg_p = np.array([-p_neg[0], -p_neg[1]])
    e_pos_p = np.array([-e_pos[0], -e_pos[1]])
    e_neg_p = np.array([-e_neg[0], -e_neg[1]])

    # Eje central del diagrama
    ax.plot(
        [p_neg_p[0], p_pos_p[0]],
        [p_neg_p[1], p_pos_p[1]],
        linestyle="--",
        linewidth=1.1,
        zorder=7
    )

    # Triángulos extremos
    ax.plot(
        [p_pos_p[0], e_pos_p[0]],
        [p_pos_p[1], e_pos_p[1]],
        linewidth=1.8,
        zorder=8
    )
    ax.plot(
        [p_neg_p[0], e_neg_p[0]],
        [p_neg_p[1], e_neg_p[1]],
        linewidth=1.8,
        zorder=8
    )

    # Recta única de pendiente constante
    ax.plot(
        [e_neg_p[0], z0p[0], e_pos_p[0]],
        [e_neg_p[1], z0p[1], e_pos_p[1]],
        linewidth=2.2,
        zorder=9
    )

    # Signos
    txt_pos = 0.5 * (p_pos_p + e_pos_p)
    txt_neg = 0.5 * (p_neg_p + e_neg_p)

    ax.text(
        txt_pos[0], txt_pos[1],
        "(+)", fontsize=8.5, fontweight="bold",
        ha="center", va="center"
    )
    ax.text(
        txt_neg[0], txt_neg[1],
        "(-)", fontsize=8.5, fontweight="bold",
        ha="center", va="center"
    )

    # Ajustar límites incluyendo también el diagrama lineal de tensiones,
    # para evitar que quede truncado cuando sobresale de la sección.
    margen = 0.08*max(b_ob, h_ob)

    x_candidates = [-xmax, -xmin]
    y_candidates = [-ymax, -ymin]

    try:
        x_candidates += [
            float(z0p[0]),
            float(p_pos_p[0]), float(p_neg_p[0]),
            float(e_pos_p[0]), float(e_neg_p[0]),
        ]
        y_candidates += [
            float(z0p[1]),
            float(p_pos_p[1]), float(p_neg_p[1]),
            float(e_pos_p[1]), float(e_neg_p[1]),
        ]
    except NameError:
        pass

    x_min_plot = min(x_candidates) - margen
    x_max_plot = max(x_candidates) + margen
    y_min_plot = min(y_candidates) - margen
    y_max_plot = max(y_candidates) + margen

    ax.set_xlim(x_min_plot, x_max_plot)
    ax.set_ylim(y_min_plot, y_max_plot)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(alpha=0.10)

    gc1, gc2, gc3 = st.columns([1.25, 1.7, 1.25])
    with gc2:
        st.pyplot(fig, width="stretch")

    lg1, lg2, lg3 = st.columns(3)
    with lg1:
        st.markdown(
            '<div class="small"><b>— Eje neutro</b></div>',
            unsafe_allow_html=True
        )
    with lg2:
        st.markdown(
            f'<div class="small"><b>● Máx. tracción:</b> {sigma_t_max:.3f} MPa</div>',
            unsafe_allow_html=True
        )
    with lg3:
        st.markdown(
            f'<div class="small"><b>■ Máx. compresión:</b> {sigma_c_max:.3f} MPa</div>',
            unsafe_allow_html=True
        )

    st.caption(
        "El diagrama lineal de tensiones se representa superpuesto a la sección, "
        "inclinado perpendicularmente al eje neutro."
    )

    # =====================================================
    # RESULTADOS
    # =====================================================
    # RESULTADOS
    # =====================================================
    st.markdown("### Resultados")

    r1, r2, r3, r4 = st.columns(4)

    if tipo_ob == "Sección L":
        card(r1, "β", f"{beta_deg:.2f}°")
        card(r2, "M·senβ", f"{M_sen_beta_ob:.3f} kN·m")
    else:
        card(r1, "Mx", f"{Mx_ob:.3f} kN·m")
        card(r2, "My", f"{My_ob:.3f} kN·m")

    card(r3, "σ tracción máx.", f"{sigma_t_max:.3f} MPa")
    card(r4, "σ compresión máx.", f"{sigma_c_max:.3f} MPa")

    p1, p2 = st.columns(2)
    with p1:
        st.markdown(
            f"""<div class="result-card">
            <div class="result-label">Máxima tracción</div>
            <div class="result-value">{max_name}</div>
            <div class="small">x = {x_t:.2f} cm · y = {y_t:.2f} cm</div>
            </div>""",
            unsafe_allow_html=True
        )
    with p2:
        st.markdown(
            f"""<div class="result-card">
            <div class="result-label">Máxima compresión</div>
            <div class="result-value">{min_name}</div>
            <div class="small">x = {x_c:.2f} cm · y = {y_c:.2f} cm</div>
            </div>""",
            unsafe_allow_html=True
        )

    yn1, yn2 = st.columns(2)
    card(yn1, "yₙ⁺", f"{yn_pos:.3f} cm")
    card(yn2, "yₙ⁻", f"{yn_neg:.3f} cm")

    st.caption(
        "yₙ⁺ e yₙ⁻ son las distancias extremas medidas perpendicularmente al eje neutro, "
        "utilizadas para calcular las tensiones máximas de tracción y compresión."
    )

    # =====================================================
    # RESOLUCIÓN DE LA FLEXIÓN
    # =====================================================
    if tipo_ob == "Sección L":
        st.markdown("### Fórmula de un término")

        st.write(
            "Para la sección no simétrica no se descompone el momento en ejes principales. "
            "Una vez obtenido el eje neutro mediante Mohr–Land, se proyecta el momento "
            "resultante sobre ese eje."
        )

        st.latex(r"\sigma=\frac{M\sin\beta}{I_n}\,y_n")

        fu1, fu2, fu3, fu4 = st.columns(4)
        card(fu1, "M", f"{M_ob:.3f} kN·m")
        card(fu2, "β", f"{beta_deg:.2f}°")
        card(fu3, "M·senβ", f"{M_sen_beta_ob:.3f} kN·m")
        card(fu4, "In", f"{In_cm4:,.1f} cm⁴")

        st.caption(
            "yn es la distancia algebraica perpendicular desde el punto considerado "
            "hasta el eje neutro."
        )

    else:
        st.markdown("### Superposición de efectos")
        st.write(
            "La flexión oblicua se interpreta como la superposición "
            "de los efectos de **Mx** y **My**."
        )
        st.latex(r"\sigma=\sigma_{M_x}+\sigma_{M_y}")

        Sigma_u_raw = ((Mu_Nm/Iu_ob)*(Vc/100.0))/1e6
        Sigma_v_raw = (-(Mv_Nm/Iv_ob)*(Uc/100.0))/1e6
        Sigma_tot_raw = Sigma_u_raw + Sigma_v_raw

        Sigma_u = np.ma.array(Sigma_u_raw, mask=~mask_shape)
        Sigma_v = np.ma.array(Sigma_v_raw, mask=~mask_shape)
        Sigma_tot = np.ma.array(Sigma_tot_raw, mask=~mask_shape)

        max_abs = max(
            float(np.max(np.abs(Sigma_u))),
            float(np.max(np.abs(Sigma_v))),
            float(np.max(np.abs(Sigma_tot))),
            1e-9
        )
        niveles = np.linspace(-max_abs, max_abs, 17)

        def mini_mapa_ob(title, data):
            fm, am = plt.subplots(figsize=(2.35, 2.15))
            am.contourf(
                Xp, Yp, data,
                levels=niveles,
                cmap="coolwarm",
                alpha=0.82
            )

            if tipo_ob == "Circular maciza":
                am.plot(R*np.cos(tt), R*np.sin(tt), linewidth=1.3)
            else:
                am.plot(xo, yo, linewidth=1.3)

            am.set_title(title, fontsize=8.3)
            am.set_aspect("equal", adjustable="box")
            am.set_xticks([])
            am.set_yticks([])
            am.set_xlim(-xmax-margen, -xmin+margen)
            am.set_ylim(-ymax-margen, -ymin+margen)
            return fm

        c1, c2, c3 = st.columns(3)

        with c1:
            fm1 = mini_mapa_ob("Solo Mx", Sigma_u)
            a, b, c = st.columns([0.18, 0.64, 0.18])
            with b:
                st.pyplot(fm1, width="stretch")

        with c2:
            fm2 = mini_mapa_ob("Solo My", Sigma_v)
            a, b, c = st.columns([0.18, 0.64, 0.18])
            with b:
                st.pyplot(fm2, width="stretch")

        with c3:
            fm3 = mini_mapa_ob("Resultado", Sigma_tot)
            a, b, c = st.columns([0.18, 0.64, 0.18])
            with b:
                st.pyplot(fm3, width="stretch")

    # =====================================================
    # EJE NEUTRO
    # =====================================================
    st.markdown("### Eje neutro")

    en1, en2 = st.columns(2)
    if slope_en is None:
        card(en1, "Orientación", "Vertical")
    else:
        card(en1, "Pendiente en x-y", f"{slope_en:.4f}")
    card(en2, "Ángulo respecto de x", f"{angle_en:.2f}°")

    if tipo_ob == "Circular maciza":
        st.info(
            "Como Ix = Iy, el eje neutro queda paralelo al momento resultante M "
            "y las tensiones extremas aparecen sobre un diámetro perpendicular a M."
        )
    elif tipo_ob == "Sección L":
        st.info(
            "En la sección L, el eje de fuerzas f es perpendicular al momento M. "
            "Mediante Mohr–Land se obtiene su eje conjugado n, que es el eje neutro. "
            "Luego se proyecta M sobre n y se aplica la fórmula de un término."
        )

    # =====================================================
    # INTERPRETACIÓN
    # =====================================================
    st.markdown("### Interpretación")

    if tipo_ob == "Rectangular maciza":
        st.write(
            "La sección posee dos ejes de simetría. Los ejes centroidales x-y son "
            "principales y las tensiones extremas aparecen en los vértices."
        )

    elif tipo_ob == "Circular maciza":
        st.write(
            "La sección posee infinitos ejes principales porque Ix = Iy. "
            "El eje neutro es paralelo al momento resultante y el diámetro de "
            "máxima tracción-compresión es perpendicular a M."
        )

    elif tipo_ob == "Sección T":
        st.write(
            "La sección posee un eje de simetría. Los ejes centroidales elegidos son "
            "principales, pero el baricentro no se encuentra a mitad de altura; por eso "
            "las distancias a las fibras extremas superior e inferior son diferentes."
        )

    else:
        st.write(
            "La sección L no posee ejes de simetría y presenta un producto de inercia "
            "distinto de cero. Con Mohr–Land se parte de Ix, Iy e Ixy para obtener el "
            "eje conjugado del eje de fuerzas f. Ese eje conjugado es el eje neutro n. "
            "La tensión se calcula luego con la fórmula de un término, proyectando M sobre n."
        )

    with st.expander("📘 Secuencia didáctica"):
        if tipo_ob == "Sección L":
            st.markdown(
                """
                **Sección no simétrica**

                1. Determinar el baricentro **G**.
                2. Calcular **Ix, Iy e Ixy** respecto de los ejes centroidales x-y.
                3. Dibujar **Ix verticalmente** y luego **Iy**.
                4. Desde el extremo de Ix llevar **Ixy**; si es positivo, hacia la derecha. El extremo es **P**.
                5. Trazar el **eje de fuerzas f**, perpendicular al vector momento **M**.
                6. Mediante el polo **P**, obtener el eje conjugado **n**, que es el eje neutro.
                7. Calcular **In** y proyectar **M** sobre **n** para obtener **Mn**.
                8. Aplicar la fórmula de un término: **σ = Mn·yn/In**.
                9. Localizar las tensiones máximas de tracción y compresión.
                """
            )
        else:
            st.markdown(
                """
                **Sección con eje(s) de simetría**

                1. Determinar el baricentro **G**.
                2. Identificar los ejes principales centroidales.
                3. Calcular los momentos de inercia correspondientes.
                4. Descomponer el momento aplicado.
                5. Superponer las tensiones.
                6. Determinar el eje neutro y los puntos críticos.
                """
            )
