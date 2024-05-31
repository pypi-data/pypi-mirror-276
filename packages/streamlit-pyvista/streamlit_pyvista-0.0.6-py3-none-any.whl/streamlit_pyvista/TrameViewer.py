import pyvista as pv
import argparse
from pyvista.trame.ui import plotter_ui
from trame.ui.vuetify3 import VAppLayout
from trame.widgets import vuetify3 as vuetify
from trame.widgets import html
from trame.decorators import TrameApp, change, controller

import logging
import os
import time, threading
import asyncio

from streamlit_pyvista.viewer import TrameBackend

root_logger = logging.getLogger("solidipes")
root_logger.propagate = True
root_logger.setLevel(logging.INFO)
if "FULL_SOLIDIPES_LOG" not in os.environ:
    root_logger.setLevel(logging.DEBUG)


@TrameApp()
class TrameViewer(TrameBackend):
    def __init__(self, mesh=None, plotter=None, server=None, port=8080, host="0.0.0.0"):
        self.slider_playing = False
        TrameBackend.__init__(self, mesh, plotter, server, port, host)

        self.setup_timer()
        self.loop = None

    def setup_timer(self):
        """ Set up the timer callback and timeout """
        self.timer_timeout = 0.25
        self.timer = threading.Thread(target=self.timer_callback)

    def setup_state(self):
        """ Set up all the state variables to initial values """
        self.state.is_full_screen = False
        self.state.mesh_representation = self.state.options[0] if self.state.options is not None else None
        self.state.warped_field = None

        # Option's dropdown
        self.state.options = [None]
        self.state.options_warp = [None]

        # Inputs
        self.state.warp_input = 0
        self.state.wireframe_on = True
        self.state.slider_value = 0
        self.state.play_pause_icon = "mdi-play"

    def timer_callback(self):
        """ This function is called on all timer tick and update the mesh viewed to animate a sequence of mesh
        playing """

        # The animation needs to stop when the server stop or if the animation was paused by the user
        while self.slider_playing and self.server.running:
            # Increment the counter while keeping it within the bound of the mesh sequence
            self.state.slider_value = (self.state.slider_value + 1) % self.sequence_bounds[1]
            # Call function on the main thread using thread safe method to update the server states and ui
            self.loop.call_soon_threadsafe(self.update_mesh_from_index, self.state.slider_value)
            self.loop.call_soon_threadsafe(self.server.force_state_push, "slider_value")

            time.sleep(self.timer_timeout)
        # After the animation was stopped, reset the timer
        self.timer = threading.Thread(target=self.timer_callback)

    @change("mesh_representation")
    def update_mesh_representation(self, mesh_representation, **kwargs):
        """ This function is automatically called when the state 'mesh_representation' is changed.
        This state is used to determine which vector field is shown """
        # Remove the scalar bar representing the last vector field shown
        self.clear_scalar_bars()

        # Replace the string input "None" with None
        if mesh_representation == "None":
            self.state.mesh_representation = None

        # Set all element of the mesh sequence with the same field shown
        for i in range(self.sequence_bounds[1]):
            if self.mesh_array is not None:
                self.mesh_array[i].set_active_scalars(self.state.mesh_representation)

        # Update ui elements
        self.update_mesh_from_index(self.state.slider_value)
        self.ui = self.build_ui()

    @change("wireframe_on")
    def update_wireframe_on(self, **kwargs):
        """ This function is automatically called when the state 'wireframe_on' is changed.
         This state is used to store whether we should show the wireframe of the mesh or the plain mesh. """
        self.replace_mesh(self.mesh)

    @change("slider_value")
    def slider_value_change(self, slider_value, **kwargs):
        """ This function is automatically called when the state 'slider_value' is changed.
         This state is used to store the frame to actually displayed in a sequence. """
        self.update_mesh_from_index(int(slider_value))
        self.state.warp_input = 0

    def clear_scalar_bars(self):
        """ Remove all the scalar bars shown on the plotter """
        if self.pl is None:
            return
        bar_to_remove = [key for key in self.pl.scalar_bars.keys()]
        [self.pl.remove_scalar_bar(title=key) for key in bar_to_remove]

    def clear_viewer(self):
        """ Reset the viewer and its related attribute to an empty viewer """
        self.clear_scalar_bars()
        self.state.slider_value = 0
        self.state.mesh_representation = None

    def replace_mesh(self, new_mesh):
        """
        Change the mesh displayed in the plotter and its related data
        Args:
            new_mesh: the new mesh to display
        """
        if new_mesh is None:
            return

        # set custom style
        kwargs_plot = {}
        if self.state.wireframe_on:
            kwargs_plot["style"] = "wireframe"

        # update mesh and set its active scalar field, as well as adding the scalar bar
        self.mesh = new_mesh

        # Set the active scalar and create it's scalar bar if it does not exist
        self.mesh.set_active_scalars(self.state.mesh_representation)

        self.pl.mapper = self.show_scalar_bar(self.state.mesh_representation)

        # Replace actor with the new mesh (automatically update the actor because they have the same name)
        self.actor = self.pl.add_mesh(self.mesh, style="wireframe" if self.state.wireframe_on else None,
                                      name="displayed_mesh", show_scalar_bar=True,
                                      scalar_bar_args={"mapper": self.pl.mapper})

    def show_scalar_bar(self, field=None):
        """
        Show the scalar bar associated with the field
        Args:
            field: The associated field of the bar that you want to show

        """
        if self.mesh_array is None:
            return

        # If the field is not specified try to get the actual field displayed in the plotter
        if field is None:
            field = self.state.mesh_representation
        if field is None:
            return

        # Get the bounds of the bar or compute it if it does not exist
        if self.bounds_scalar is None:
            self.computes_bounds_scalar()

        # Create the pyvista scalar bar
        bounds = self.bounds_scalar.get(field, None)
        if bounds is not None:
            self.pl.mapper.lookup_table.SetTableRange(bounds[0], bounds[1])
            self.pl.add_scalar_bar(self.state.mesh_representation)

        # Return the mapper to display the good max and min value on the bar
        return self.pl.mapper

    def update_ui(self):
        """ Force to redraw the ui """
        if self.mesh is not None and self.mesh.active_scalars is not None:
            self.pl.remove_scalar_bar()
        self.ui = self.build_ui()

    def option_dropdown(self):
        """ This function return the ui element displaying the mesh_representation dropdown """
        return vuetify.VSelect(
            v_model=("mesh_representation", "None"),
            items=("options", self.state.options),
            label="Representation",
            hide_details=True,
            dense=True,
            outlined=True,
            classes="pt-1",
        )

    def build_slider(self):
        """
        This function build the ui component containing the slider to select the frame displayed
        Returns: a row containing a play-pause button and a slider

        """
        row = html.Div(style='display:flex;justify-content:center;align-content:center;gap:20px;')
        with row:
            with vuetify.VBtn(
                    icon=True,
                    click=self.play_button
            ):
                vuetify.VIcon("{{ play_pause_icon }}")
            html.Div("{{ slider_value }}")
            vuetify.VSlider(
                ref="slider",
                label="",
                min=self.sequence_bounds[0],
                max=self.sequence_bounds[1] - 1,
                v_model=("slider_value", 8),
                step=1
            )
        return row

    @controller.set("play_button")
    def play_button(self):
        """ This function is called the play-pause button of the slider is played and manage the state
        of the timer that updates the frame displayed in a periodic manner. """
        if self.sequence_bounds[1] <= 1:
            root_logger.error("Impossible to start the sequence since it's a unique mesh")
            return

        # Invert the state of the play button and if it's playing start the timer updating frame at a fixed interval
        self.slider_playing = not self.slider_playing
        if self.slider_playing and not self.timer.is_alive():
            self.state.play_pause_icon = "mdi-pause"

            self.loop = asyncio.get_event_loop()
            self.timer.start()
        else:
            self.state.play_pause_icon = "mdi-play"
        self.update_ui()


    def build_mesh_control_layout(self):
        """
        This function return all the control part of the ui composed of:
            - The dropdown to select the vector field to display
            - The warp control
            - The slider controller
            - other various control
        Returns: a vuetify component representing all the control layout

        """
        layout = html.Div()
        with (layout):
            with vuetify.VRow(dense=True):
                # If there are options show the dropdown
                if self.state.options[0] is not None and len(self.state.options) > 1:
                    self.option_dropdown()
            vuetify.VCheckbox(v_model=("wireframe_on",), label="Wireframe on", id="wireframe_checkbox")
            # If the viewer display a sequence of mesh show the slider
            if self.sequence_bounds[1] > 1:
                self.build_slider()
        return layout

    def estimate_controller_height(self):
        """
        This function make an estimation of the size the component might required in the worst case
        Returns: The computed worst case height
        """
        # Get the worst dimension of any warper to find how many input would be required and add the height
        # of all these input to the default height
        if self.mesh_array is not None and self.state.mesh_representation is not None:
            ndim = self.mesh_array[0].get_array(self.state.mesh_representation).shape[1]
            return 30 * ndim, 9 * 30
        return 0.2 * self.height, 9 * 30

    def build_ui(self):
        """
        Build all the ui frontend with all different components
        Returns:
            a VAppLayout for the server
        """
        control_height = self.estimate_controller_height()[0]
        # Define some styling variables
        if not self.state.is_full_screen:
            plotter_height = self.height - 250
            plotter_height = f"{plotter_height}px"
            width = "100%"
        else:
            plotter_height = "100%"
            width = "100%"

        with VAppLayout(self.server) as layout:
            with layout.root:
                with html.Div(
                        style=f"height: {self.height}px ;width:{width}"):  # add the following arg: style="height: 100vh; width:100vw" to have the plotter taking all screen
                    with html.Div(ref="container", style=f"height:{plotter_height};padding: 0;"):
                        # Create the plotter section
                        with vuetify.VCol(style=f"height:{plotter_height};padding: 0;"):
                            # If the slider is playing we force the app to use remote rendering to avoid bug
                            # with local rendering
                            if self.slider_playing:
                                plotter_ui(self.pl, default_server_rendering=True, mode="server",
                                           style="width: 100%; height:100%;background-color: black;")
                            else:
                                plotter_ui(self.pl, default_server_rendering=True,
                                           style="width: 100%; height:100%;background-color: black;")
                    with vuetify.VCol(style=f"height:{control_height}px;padding: 0;width:100%;"):
                        # Create the whole control layout
                        self.build_mesh_control_layout()

        return layout

    @staticmethod
    def get_launch_path():
        return os.path.abspath(__file__)



if __name__ == "__main__":
    pv.start_xvfb()
    # Add command line argument and support
    parser = argparse.ArgumentParser(description='Launch a trame server instance')
    # Add the port argument that allow user to specify the port to use for the server from command line
    parser.add_argument('--port', type=int, help='Specify the port of the server')
    # Add --server flag that is used to specify whether to use the trame as only a server and block the
    # automatic open of a browser
    parser.add_argument('--server', action="store_true", help='Specify if the trame is opened as a server')
    args = parser.parse_args()
    mv = TrameViewer(port=args.port)
    mv.start_server()
