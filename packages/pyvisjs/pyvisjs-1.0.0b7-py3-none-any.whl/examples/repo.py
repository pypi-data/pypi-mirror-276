from pyvisjs import Network, Options


options = Options("800px", "1300px")
options.edges.set(arrows="to")
options.pyvisjs \
    .set(title="pyvisjs code repo visualisation") \
    .set_startAnimation(zoom_factor=2, duration_ms=3000) \
    .set_filtering(
        enable_highlighting=True,
        node_filtering=["file_type", "file_ext", "label"],
        dropdown_auto_close=True,
    )

net = Network.from_dir(".", options)
net.show()