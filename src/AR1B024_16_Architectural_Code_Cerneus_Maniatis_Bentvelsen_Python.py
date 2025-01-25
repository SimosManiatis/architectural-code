# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import streamlit as st
import pyvista as pv
import pydeck as pdk
from geopy.geocoders import Nominatim
from pywavefront import Wavefront
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
bus_stop_coordinates = {
    "Zuidpoort": (52.0081424175603, 4.3635562683087015),
    "Hugo van Rijkenlaan": (52.01328656142907, 4.36780232122377),
    "Christiaan Huygensweg": (52.00393768709406, 4.376025611345895),}

def create_3d_object_viewer(object_path, mtl_path=None):
    if mtl_path:
        mesh = Wavefront(object_path, parse=True, strict=True, encoding="iso-8859-1")
        plotter = pv.Plotter()
        plotter.add_mesh(mesh.vertices, faces=mesh.triangles, color='white')
        plotter.background_color = [0.055, 0.066, 0.090]
        plotter.show()
    else:
        mesh = pv.read(object_path)
        if mesh.point_data and 'Colors' in mesh.point_data:
            colors = mesh.point_data['Colors']
            plotter = pv.Plotter()
            plotter.add_mesh(mesh, color='white', show_scalar_bar=False)
            plotter.background_color = [0.055, 0.066, 0.090]
            plotter.show()
        else:
            plotter = pv.Plotter()
            plotter.add_mesh(mesh, color='white', show_scalar_bar=False)
            plotter.background_color = [0.055, 0.066, 0.090]
            plotter.show()

def generate_user_input_form_code(params):
    return "_".join(params.values())

def create_pydeck_map(latitude, longitude):
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=[{'latitude': latitude, 'longitude': longitude}],
        get_position="[longitude, latitude]",
        get_color="[227, 101, 29, 150]",
        get_radius=7.5,)
    view_state = pdk.ViewState(latitude=latitude, longitude=longitude, zoom=17.5)
    deck = pdk.Deck(layers=[layer], initial_view_state=view_state)
    return deck
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def main():
    st.markdown(
        """
        <style>
            .app-container {
                max-width: 2000px;
                padding: 10px;
                background-color: rgba(255, 255, 255, 0.15);
                border-radius: 10px;}
            .thank-you {
                margin-top: 645px; /* Add margin space above the text */}
        </style>
        """,
        unsafe_allow_html=True,)

    st.markdown("<div class='app-container'>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-family: Futura; color: #ffffff; text-align: left;'><span style='color: #E3651D;'>Architectural </span>Code . . .</h1>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-family: Futura; font-size: 20px; color: #E3651D; text-align: left;'><span style='color: #ffffff;'>Pre-Parametric </span>Design</h1>", unsafe_allow_html=True)
    st.sidebar.write("Please fill in the user-input form to retrieve an optimized bus stop design.")
    submitted = False

    col1, col2 = st.columns(2)
    with col1:
        Give_City = st.selectbox(label="City", options=["Delft"])
        Give_Bus_Stop = st.selectbox(label="Bus stop", options=["Zuidpoort", "Hugo van Rijkenlaan", "Christiaan Huygensweg"])
        Give_Shape_Walls = st.selectbox(label="Shape walls", options=["Rectangle", "Ellipse"])
        Give_Shape_Roof = st.selectbox(label="Shape roof", options=["Concave", "Convex"])
        Give_Wind = st.selectbox(label="Wind (1 = high wind cover, 2 = average wind cover, 3 = low wind cover)", options=["1", "2", "3"])
        Give_View = st.selectbox(label="View (1 = high transparency, 2 = average transparency, 3 = low transparency)", options=["1", "2", "3"])

    with col2:
        st_container_map = st.empty()
        selected_bus_stop_coordinates = bus_stop_coordinates[Give_Bus_Stop]
        latitude, longitude = selected_bus_stop_coordinates
        st_container_map.pydeck_chart(create_pydeck_map(latitude, longitude))

    with st.form(key="my_form"):
        submit_button = st.form_submit_button(label="Submit")
        submitted = submit_button
    st_container_3d = st.empty()

    if submitted:
        selected_bus_stop_coordinates = bus_stop_coordinates[Give_Bus_Stop]
        latitude, longitude = selected_bus_stop_coordinates
        object_params = {
            "Give_City": Give_City,
            "Give_Bus_Stop": Give_Bus_Stop,
            "Give_Shape_Walls": Give_Shape_Walls,
            "Give_Shape_Roof": Give_Shape_Roof,
            "Give_Wind": Give_Wind,
            "Give_View": Give_View,}
        user_input_form_code = generate_user_input_form_code(object_params)
        object_path = rf"D:\3.0 Technische Universiteit Delft\MSc Building Technology\Leerjaar 1\Kwartaal 01\AR1B024 Computational Design - 5 ECTS\3.0 Design\3.2 Python\{user_input_form_code}.stl"
        create_3d_object_viewer(object_path)
    st.markdown("</div>", unsafe_allow_html=True)
    st.sidebar.markdown("<div class='thank-you'>Thank you for using our bus stop design application!</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------