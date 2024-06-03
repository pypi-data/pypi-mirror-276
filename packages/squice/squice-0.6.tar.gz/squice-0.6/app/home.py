import streamlit as st

st.set_page_config(
    page_title="squice",
    page_icon="app/static/squice.png",
    layout="wide",
)

st.header("SQUICE")
st.write("**Visualise and interpolate numerical matrix data**")

st.write(
    """
*SQUICE* is a scientific data library for visualising and manipulating orthogonal
numerical matrices. These matrices can be any kind of numerical data, including data or
some kind of data in space.

The documentation for the library classes and functions can be found at
[pydoctor squice library doc](https://rachelalcraft.github.io/squice/)

Issues can be raised here
[squice github issues](https://github.com/RachelAlcraft/squice/issues)

The library is on pypi: [squice on pypi](https://pypi.org/project/squice/)

In addition to the ability to load or define 3d numpy matrices for the library, there
is provided a simple means to convert electron density/microscopy and protein
data into 3d matrices for visualisation as this was the motivating factor behind the
library.

This library was written under my split dual identity as a PhD student in Computational
Biology at Birkbeck (University of London) and as a Research Software Engineer at
 the Institute of Cancer Research.

The example page gives the ability to load or define matrix data and navigate
the data with slices and interpolation choices. All code is given so you can replicate
the functionality in your own scripts.

*The ethos of this
[scientific library structure](https://github.com/RachelAlcraft/app-lib-py)
is to use a functional app like
this to demonstrate the python library with all code given, democratising use of the
tool across user groups of different resources and expertise.*

---

With thanks to my supervisor at Birkbeck,
[Dr Mark Williams](https://www.bbk.ac.uk/our-staff/profile/8006855/mark-williams),
for his unfailing positive support despite my meandering.
"""
)

st.write(
    """
If you use this library either in the application or from the python library, please cite:
"""
)
st.write(
    """*Alcraft, R and Williams, M.A., SQUICE: A library for visualisation and
interpolation of numerical matrix data, 2024, doi:*"""
)
"---"
st.caption(
    """~~ ~~ ~~ Contact: [Rachel by email](mailto:raye.alcraft.dev@gmail.com),
:copyright: 2024 ~~ ~~ ~~"""
)
"---"
