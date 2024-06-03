import streamlit as st
from squice import DataLoaders as dl
from squice import VectorThree as v3
from squice import MtxInterpolator as mi
from squice import GridMaker as gm
from squice import SpaceTransform as sp
import plotly.graph_objs as go
import io
import numpy as np
import os
import uuid
import pandas as pd

st.set_page_config(
    page_title="squice",
    page_icon="app/static/squice.png",
    layout="wide",
)

st.title("SQUICE: Example")


def grid_navigate(cmd, spc, angle, distance):
    vcentral = spc.navigate(
        v3.VectorThree(abc=central), cmd, distance, angle_delta=angle
    )
    vlinear = spc.navigate(v3.VectorThree(abc=linear), cmd, distance, angle_delta=angle)
    vplanar = spc.navigate(v3.VectorThree(abc=planar), cmd, distance, angle_delta=angle)
    st.session_state["central"] = vcentral.to_coords_str()
    st.session_state["linear"] = vlinear.to_coords_str()
    st.session_state["planar"] = vplanar.to_coords_str()


def set_c_l_p(xx, yy, zz):
    st.session_state["central"] = f"({(xx-1)/2}, {(yy-1)/2}, {(zz-1)/2})"
    st.session_state["linear"] = f"({xx-1}, {(yy-1)/2}, {(zz-1)/2})"
    st.session_state["planar"] = f"({(xx-1)/2}, {yy-1}, {(zz-1)/2})"
    st.session_state["width"] = min(xx, yy, zz) - 1
    st.session_state["samples"] = 20  # min(xx,yy,zz)


def return_to_centre(matrix):
    xx, yy, zz = matrix.mtx.shape
    # if we haven't initted values then they need defaults
    if "return_centre" not in st.session_state:
        st.session_state["return_centre"] = False
        set_c_l_p(xx, yy, zz)
    # if we have a return to centre then we re-init certain values
    if st.session_state["return_centre"]:
        set_c_l_p(xx, yy, zz)
        st.session_state["return_centre"] = False


MY_MTX = None

tabData, tabAll, tabSlice = st.tabs(["data", "matrix", "slice"])  # , "chunk"])
with tabData:

    option = st.radio(
        "Data loaded from:",
        ["Manual", "NumpyFile", "Electron Density", "Electron Microscopy", "PDB/CIF"],
        horizontal=True,
    )
    if option == "Manual":
        mtx_txt = """[[[0,0,0],[0,3,0],[0,0,0]],
        [[0,0,0],[3,5,0],[0,0,0]],
        [[0,0,0],[0,0,1],[0,0,0]]]
        """
        data_str = st.text_area("Matrix", mtx_txt, height=200).strip()
        MY_MTX = dl.NumpyNow(data_str)
        MY_MTX.load()
    elif option == "NumpyFile":
        uploaded_file = st.file_uploader(
            "Upload numpy file", type="npy", accept_multiple_files=False
        )
        if uploaded_file is not None:
            # To read file as bytes:
            bytes_data = uploaded_file.getbuffer()
            filename = str(uuid.uuid4())
            with open(filename, "wb") as wb:
                wb.write(bytes_data)
            MY_MTX = dl.NumpyFile(filename)
            MY_MTX.load()
            if os.path.exists(filename):
                os.remove(filename)
            mtx_str = str(MY_MTX.mtx)

            # mtx_str = mtx_str.replace("\n"," ")
            # mtx_str = mtx_str.replace("\t"," ")
            while mtx_str.count("  ") > 0:
                mtx_str = mtx_str.replace("  ", " ")
            mtx_str = mtx_str.replace("]", "],")
            mtx_str = mtx_str.replace(",]", "]")
            mtx_str = mtx_str.replace(" [", "[")
            mtx_str = mtx_str.replace(" ", ",")
            mtx_str = mtx_str.replace(",]", "]")
            mtx_str = mtx_str.replace("]]],", "]]]")
            data_str = st.text_area("Matrix", mtx_str, height=200).strip()
            MY_MTX = dl.NumpyNow(data_str)
            MY_MTX.load()

    else:
        st.error("Apologies, only numpy data is currently implemented")

    # some display and save of data
    if MY_MTX is not None:

        # display the data
        cols = st.columns(3)
        with cols[0]:
            with st.popover("Show mtx data"):
                st.write(MY_MTX.mtx)

        filename = "matrix.npy"
        with cols[1]:
            filename = st.text_input("fname", filename, label_visibility="collapsed")
        with cols[2]:
            # save the data with an in-memory buffer
            with io.BytesIO() as buffer:
                # Write array to buffer
                np.save(buffer, MY_MTX.mtx)
                btn = st.download_button(
                    label="Download mtx",
                    data=buffer,  # Download buffer
                    file_name=filename,
                )
if MY_MTX is not None:

    with tabAll:
        st.write("### Raw matrix data")

        cols = st.columns(2)
        with cols[0]:
            chart_style = st.radio("Plot type", ["isosurface", "3dscatter"])

        with cols[1]:

            xs = []
            ys = []
            zs = []
            values = []
            minv = None
            maxv = None

            a, b, c = MY_MTX.mtx.shape
            for i in range(a):
                for j in range(b):
                    for k in range(a):
                        val = 0
                        if k < c:
                            val = MY_MTX.mtx[i][j][k]
                            if minv is None:
                                minv = val
                                maxv = val
                            else:
                                minv = min(minv, val)
                                maxv = max(maxv, val)
                        xs.append(i)
                        ys.append(j)
                        zs.append(k)
                        values.append(val)

            c0 = "rgba(119,136,153,0.6)"
            c1 = "rgba(240,248,255,0)"
            c2 = "rgba(100,149,237,0.5)"
            c3 = "rgba(220,20,60,0.9)"
            c4 = "rgba(100,0,0,1)"

            zero = 1 - (maxv / abs(maxv - minv))
            zer0 = max(0, zero)
            zer1 = max(zer0 * 1.5, 0.1)
            zer2 = max(zer0 * 1.9, 0.8)

            colorscale = [(0, c0), (zer0, c1), (zer1, c2), (zer2, c3), (1, c4)]

            data_iso = go.Isosurface(
                x=xs,
                y=ys,
                z=zs,
                value=values,
                colorscale=colorscale,
                showscale=True,
                showlegend=False,
                opacity=0.6,
                surface_count=20,
                caps=dict(x_show=False, y_show=False),
                isomin=minv,
                isomax=maxv,
            )

            dicdf = {}
            dicdf["x"] = []
            dicdf["y"] = []
            dicdf["z"] = []
            dicdf["v"] = []
            xx, yy, zz = MY_MTX.mtx.shape
            for i in range(xx):
                for j in range(yy):
                    for k in range(zz):
                        dicdf["x"].append(i)
                        dicdf["y"].append(j)
                        dicdf["z"].append(k)
                        v = MY_MTX.mtx[i][j][k]
                        dicdf["v"].append(v)
            df = pd.DataFrame.from_dict(dicdf)
            data_scatter = go.Scatter3d(
                x=df["x"],
                y=df["y"],
                z=df["z"],
                mode="markers",
                marker=dict(
                    color=df["v"], colorscale=colorscale, showscale=True, size=12
                ),
            )

            if chart_style == "isosurface":
                fig = go.Figure(data_iso)
            else:
                fig = go.Figure(data_scatter)

            # fig.update_xaxes(showticklabels=False, visible=False,scaleanchor="y", scaleratio=1)
            # fig.update_yaxes(showticklabels=False, visible=False,scaleanchor="x", scaleratio=1)
            fig.update_xaxes(
                showticklabels=False,
                visible=True,
                showline=False,
                linewidth=2,
                linecolor="black",
                mirror=True,
                scaleanchor="y",
                scaleratio=1,
                gridwidth=1,
                gridcolor="black",
            )
            fig.update_yaxes(
                showticklabels=False,
                visible=True,
                showline=False,
                linewidth=2,
                linecolor="black",
                mirror=True,
                scaleanchor="x",
                scaleratio=1,
                gridwidth=1,
                gridcolor="black",
            )
            fig.update_layout(
                width=600,
                height=600,
                plot_bgcolor="rgba(0,0,0,1.0)",
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False),
            )
            # Plot!
            st.plotly_chart(fig, use_container_width=False)

    with tabSlice:
        return_to_centre(MY_MTX)
        st.write("### Slice through the matrix")
        with st.expander("**Settings**", expanded=True):
            st.caption(
                """To define a slice through an orthogonal grid,
            we need to have 3 points to define a plane. These we will define as the points that are:
            - central - linear  - planar
            Additionally we need to know:
            - width of the slice
            - sample frequency
            The width can be considered the zoom; the sample frequence, the resolution.
            """
            )
            st.write(
                f"The dimensions of the data are: xx, yy, zz = {MY_MTX.mtx.shape} (Note the width is dim-1)"
            )
            central = st.session_state["central"]
            linear = st.session_state["linear"]
            planar = st.session_state["planar"]
            width = st.session_state["width"]
            samples = st.session_state["samples"]

            cols = st.columns([2, 2, 1, 3, 5])
            with cols[0]:
                interper = st.radio("Interpolator", ["Nearest", "Linear"], index=1)
            with cols[1]:
                extend = st.radio("Extending", ["None", "Periodic"], index=0).lower()
            with cols[2]:
                max_width = st.number_input(
                    "max width", 2 * max(MY_MTX.mtx.shape), key="maxw"
                )
                max_samples = st.number_input("max samples", 50, key="maxs")
            with cols[3]:
                width = st.slider(
                    "Width", 0, max_width, key="width_slider", value=width
                )
                samples = st.slider("Samples", 2, max_samples, value=samples)
                st.session_state["width"] = width
                st.session_state["samples"] = samples
            with cols[4]:
                st.caption("Enter points in the format (0,1, 1.2, 3.4)")
                params = {}
                params.setdefault("label_visibility", "collapsed")
                c1, c2 = st.columns([2, 5])
                c1.markdown("central: :red[*]")
                central = c2.text_input(".", central, **params)
                c1, c2 = st.columns([2, 5])
                c1.markdown("linear: :red[*]")
                linear = c2.text_input(".", linear, **params)
                c1, c2 = st.columns([2, 5])
                c1.markdown("planar: :red[*]")
                planar = c2.text_input(".", planar, **params)

        # interpolator
        if interper == "Linear":
            interp = mi.Linear(MY_MTX.mtx, wrap=extend)
        else:
            interp = mi.Nearest(MY_MTX.mtx, wrap=extend)

        # space transformer
        spc = sp.SpaceTransform(central, linear, planar)
        cols_plot = st.columns(2)
        with cols_plot[0]:
            # colsA = st.columns([1,2,1,2,1])
            # with colsA[1]:
            cols = st.columns([1, 1, 1, 1, 1])
            with cols[0]:
                angle = st.number_input("angle", 1)
                distance = st.number_input("distance", 0.1)
            with cols[1]:
                st.write("Navigate")
                if st.button(":arrow_left:", help="left"):
                    grid_navigate("LE", spc, angle, distance)

                if st.button(":arrows_counterclockwise:", help="anti-clockwise"):
                    grid_navigate("AC", spc, angle, distance)
            with cols[2]:
                st.write("in")
                if st.button(":arrow_up:", help="up"):
                    grid_navigate("UP", spc, angle, distance)
                if st.button(":arrow_down:", help="down"):
                    grid_navigate("DN", spc, angle, distance)

            with cols[3]:
                st.write("plane")
                if st.button(":arrow_right:", help="right"):
                    grid_navigate("RI", spc, angle, distance)
                if st.button(":arrows_clockwise:", help="clockwise"):
                    grid_navigate("CL", spc, angle, distance)

            # with colsA[3]:
            with cols[1]:
                st.write("Navigate")
                if st.button(":arrow_heading_up:", help="tilt over"):
                    grid_navigate("TO", spc, angle, distance)
                if st.button(":arrow_heading_down:", help="tilt under"):
                    grid_navigate("TU", spc, angle, distance)
            with cols[2]:
                st.write("out of")
                if st.button(":arrow_double_up:", help="forwards"):
                    grid_navigate("FW", spc, angle, distance)
                if st.button(":arrow_double_down:", help="backwards"):
                    grid_navigate("BA", spc, angle, distance)
            with cols[3]:
                st.write("plane")
                if st.button(":leftwards_arrow_with_hook:", help="tilt left"):
                    grid_navigate("TL", spc, angle, distance)
                if st.button(":arrow_right_hook:", help="tilt right"):
                    grid_navigate("TR", spc, angle, distance)

            # with colsA[2]:
            with cols[2]:
                st.write("Return to centre")
                max_width = 2 * max(MY_MTX.mtx.shape)
                width = max(MY_MTX.mtx.shape)
                if st.button(":black_square_for_stop:", help="return to centre"):
                    st.session_state["return_centre"] = True
                    return_to_centre(MY_MTX)

            # Get all the settings out of session state
            central = st.session_state["central"]
            linear = st.session_state["linear"]
            planar = st.session_state["planar"]
            width = st.session_state["width"]
            samples = st.session_state["samples"]

        with cols_plot[1]:
            # unit grid
            grid = gm.GridMaker()
            slice_grid = grid.get_unit_grid(width, samples)
            # get all vals from interpolator
            spc = sp.SpaceTransform(central, linear, planar)
            xyz_coords = spc.convert_coords(slice_grid)
            # print(xyz_coords)
            vals = interp.get_val_slice(xyz_coords)[:, :, 0]
            # print(vals)
            xc = v3.VectorThree(abc=central).A
            yc = v3.VectorThree(abc=central).B
            zc = v3.VectorThree(abc=central).C
            xs, ys = vals.shape

            hover_data = []
            for i in range(vals.shape[0]):
                hover_data_row = []
                for j in range(vals.shape[1]):
                    hvrV = xyz_coords.get(i, j)
                    hover_data_row.append(hvrV.to_coords_str())
                hover_data.append(hover_data_row)

            x = list(range(0, xs)) - xc
            y = list(range(0, ys)) - yc

            cs = [
                (0, "AliceBlue"),
                (0.2, "rgba(100,149,237,1)"),
                (0.9, "rgba(220,20,60,1)"),
                (1.0, "rgba(100,0,0,1)"),
            ]

            data_vals = go.Heatmap(
                z=vals,
                x=x,
                y=y,
                text=hover_data,
                colorscale=cs,
                showscale=True,
                hovertemplate="......%{z}<br>%{text}",
            )

            fig = go.Figure(data_vals)
            fig.update_xaxes(
                showticklabels=False,
                visible=True,
                showline=False,
                linewidth=2,
                linecolor="black",
                mirror=True,
                scaleanchor="y",
                scaleratio=1,
                gridwidth=1,
                gridcolor="black",
            )
            fig.update_yaxes(
                showticklabels=False,
                visible=True,
                showline=False,
                linewidth=2,
                linecolor="black",
                mirror=True,
                scaleanchor="x",
                scaleratio=1,
                gridwidth=1,
                gridcolor="black",
            )
            fig.update_layout(
                width=600,
                height=600,
                plot_bgcolor="rgba(0,0,0,1.0)",
                xaxis=dict(showgrid=True),
                yaxis=dict(showgrid=True),
            )
            # Plot!
            st.plotly_chart(fig, use_container_width=False)
