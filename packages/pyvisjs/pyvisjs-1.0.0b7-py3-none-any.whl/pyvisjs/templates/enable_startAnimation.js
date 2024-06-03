// ---------------- START ANIMATION START ----------------------
data.network.once("afterDrawing", 
    function (ctx) {
        data.network.Zoom(data.pyvisjs.zoom_factor, data.pyvisjs.duration_ms)
    }
);
// ---------------- START ANIMATION END ----------------------