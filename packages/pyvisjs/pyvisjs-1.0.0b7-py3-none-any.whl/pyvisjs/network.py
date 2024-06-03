import os
from .base_dictable import BaseDictable
from .utils import open_file, save_file
from .node import Node
from .edge import Edge
from .options import Options
from jinja2 import Environment, PackageLoader, select_autoescape
from typing import List, Dict
from pathlib import Path

class Network(BaseDictable):
    """
    Network is a visualization to display networks consisting of nodes and edges. 
    The visualization is easy to use and supports custom shapes, styles, colors, sizes, images, and more. 
    The network visualization works smooth on any modern browser for up to a few thousand nodes and edges. 
    Network uses HTML canvas for rendering.
    """
    def __init__(self, name="Network", nodes:List[Node]=None, edges:List[Edge]=None, options:Options=None):
        only_use_data_attr = lambda attr: attr == "_data"
        super().__init__(attr_filter_func=only_use_data_attr)
        self.name = name
        self._initialize_data(nodes, edges, options)
        self.env = Environment(
            loader=PackageLoader("pyvisjs"),
            autoescape=select_autoescape()
        )
        self.env.globals.update(isinstance=isinstance)

    @property
    def options(self) -> Options:
        opt = self._data["options"]   
        return opt if isinstance(opt, Options) else None
    
    @options.setter
    def options(self, val:Options):
        self._data["options"] = val
    
    @property
    def nodes(self) -> List[Node]: 
        return self._data["nodes"]  
    
    @property
    def edges(self) -> List[Edge]: 
        return self._data["edges"]  

    def _initialize_data(self, nodes:List[Node]=None, edges:List[Edge]=None, options:Options=None):
        default_data = {"nodes": [], "edges": [], "options": {}}

        if nodes:
            default_data.update({
                "nodes": nodes,
            })

        if edges:
            default_data.update({
                "edges": edges,
            })

        if options:
            default_data["options"] = options

        self._data = default_data

    def __repr__(self):
        return f"Network(\'{self.name}\')"
    
    def add_node(self, id:str, label=None, color=None, shape="dot", size=None, cid=None, **kwargs):
        """
        Creates a Node with `id` and adds it to the nodes list. 
        Wont add node if the nodes list alredy contains a node with the same `id`.

        Parameters
        ----------
        id: str, default undefined
            The id of the node. The id is mandatory for nodes and they have to be unique. 
            Will be used as a node reference in edges

        label: str, default undefined
            Will be replaced with `str(id)` if undefined. 
            The label is the piece of text shown in or under the node, depending on the shape.
        
        color: str, default undefined, but if undefined, `'#97C2FC'` will be used by vis.js
            Could be value like `'#ffffff'` or `'red'`
        
        **kwargs: dict, optional
            Any key=value agruments could also be specified to push them into the underlying HTML template
        """
        if not [node.id for node in self.nodes if node.id == str(id)]:
            self.nodes.append(Node(id, label, color, shape, size, cid, **kwargs))

    def add_edge(self, fr0m:str, to:str, **kwargs):
        """Creates an Edge which connects two nodes using `fr0m` and `to` and adds it to the edges list.
        If you provide node ID which is not presented in the nodes list 
        such a node will be automatically created and added to the nodes list.
        
        Parameters
        ----------
        fr0m: str, default undefined
            Edges are between two nodes, one to and one from. This is where you define the from node. 
            You have to supply the corresponding node ID.
        
        to: str, default undefined
            Edges are between two nodes, one to and one from. This is where you define the to node. 
            You have to supply the corresponding node ID.

        **kwargs: dist, Optional
            Any key=value agruments could also be specified to push them into the underlying HTML template
        """
        self.add_node(fr0m)
        self.add_node(to)

        if not [edge.start for edge in self.edges if edge.start == str(fr0m) and edge.end == str(to)]:
            self.edges.append(Edge(fr0m, to, **kwargs))

    def to_dict(self):
        return super().to_dict()["_data"]

    def show(self, file_name:str=None):
        if file_name:
            self.render(open_in_browser=True, output_filename=file_name)
        else:
            self.render(open_in_browser=True)

    def render(self, open_in_browser=False, save_to_output=False, output_filename="default.html"):
        network_dict = self.to_dict()
        pyvisjs_options = None
        tables = None
        filtering_enabled = False
        dataTables_enabled = False

        if self.options:
            pyvisjs_options = self.options.pyvisjs.to_dict(nodes=self.nodes, edges=self.edges)
            filtering_enabled = pyvisjs_options["filtering_enabled"]
            dataTables_enabled = pyvisjs_options["dataTables_enabled"]

            # (todo) this part below probably could be moved somwhere
            tables = self.options.pyvisjs.dataTables
            for key in tables:
                table = tables[key]
                if "data" in table and table["data"] == "edges":
                    table["data"] = network_dict["edges"]
                elif "data" in table and table["data"] == "nodes":
                    table["data"] = network_dict["nodes"]
        
        template_filename = "container-template.html" if filtering_enabled or dataTables_enabled else "basic-template.html"

        html_output = self.env \
            .get_template(template_filename) \
            .render(
                data=network_dict,
                pyvisjs=pyvisjs_options or {},
                tables=tables or {}
            )

        if save_to_output or open_in_browser:
            file_path = save_file(output_filename, html_output)

        if open_in_browser:
            open_file(file_path)

        return html_output

    classmethod
    def from_transactions(cls):
        # (todo) from_transactions
        pass

    @classmethod
    def from_dir(cls, dir:str, options:Options=None):
        net = Network(options=options) if options else Network()

        for path, subdirs, files in os.walk(dir):
            if ".venv" not in path \
                and "__pycache__" not in path \
                and "cachedir.tag" not in path \
                and ".pytest_cache" not in path \
                and ".git" not in path \
                and "node_modules" not in path \
                and "egg-info" not in path:
                curr_dir = (Path(os.getcwd()).stem).replace("-", "\n")
                net.add_node(
                    id = path, 
                    label = curr_dir, 
                    shape = "circle",
                    color = "orange",
                    font = {"color": "black"},
                    file_type = "dir",
                    file_ext = "",
                )

                for name in subdirs:
                    full_name = os.path.join(path, name)
                    net.add_node(
                        id = full_name, 
                        label = name, 
                        shape = "circle",
                        color = "#4eba3f",
                        font = {"color": "black"},
                        file_type = "dir",
                        file_ext = "",
                    )            
                    net.add_edge(path, full_name, label=f"dir:{subdirs.index(name)}")

                for name in files:
                    full_name = os.path.join(path, name)
                    ext = Path(name).suffix

                    if ext == ".py":
                        (color, font_color) = ("#54bede", "black")
                    elif ext == ".md":
                        (color, font_color) = ("#F02B4B", "black")
                    elif ext == ".txt":
                        (color, font_color) = ("#DF7DEC", "black")
                    elif ext == ".html":
                        (color, font_color) = ("#8f2d56", "white")
                    elif ext == ".js":
                        (color, font_color) = ("#da7422", "black")
                    else:
                        (color, font_color) = (None, "black")

                    net.add_node(
                        id = full_name, 
                        label = name, 
                        shape = "box",
                        color = color,
                        file_type = "file",
                        file_ext = ext,
                        font = {"color": font_color},
                    )            
                    net.add_edge(path, full_name, label=f"file:{files.index(name)}")

        return net
            
    def __render_default_template(self, open_in_browser=False, save_to_output=False, output_filename="default.html"):
        return self.render(
            open_in_browser=open_in_browser,
            save_to_output=save_to_output,
            output_filename=output_filename)
    

    def __render_tom_template(self, open_in_browser=False, save_to_output=False, output_filename="default.html") -> str:
        """This method uses jinja to inject prepared data to `'templates\\container-template.html'` \n
        (for more info about the injected data see Notes section below).
        
        Parameters
        ----------
        open_in_browser: bool, default=False
            Resolved template will be saved as the `output_filename` and opened with `os.startfile`

        save_to_output: bool, default=False
            Resolved template will be just saved (not opened) as the `output_filename`

        output_filename: str, default=".\\default.html"
            Can be just a file name or have relative or absolute path

        enable_highlighting: bool, default=False
            - `true` - turns highlighting mode on, which means filtering in the tom-select control will highlight a part of the network - not hide it
            - `false` - turns highlighting mode off, which means filtering in the tom-select control will hide a part of the network - not highlight it
            This setting is not a standard vis.js option and injects to the template as the `enable_highlighting` key of the `pyvisjs` dict
        
        edge_filtering: str or list, default=None
            Enables edges filtering using predefined or dynamic edge attributes which means hiding all edges which do not satisfy filtering condition
            So for example you can:
            add a dynamic attribute "size" with 3 possible values ['S', 'M', 'L'] to the edges and 
            pass `edge_filtering="size"` to the `render_tom_template` method
            expecting resolved template to have `<select>` element with S/M/L options lookup
            which will filter all nodes connected with edges having selected option
            see example on `gitlab.com/22kittens/pyvisjs/examples/bluor.py`

        node_filtering: str or list, default=None
            Enables nodes filtering using predefined or dynamic node attributes which means hiding all nodes which do not satisfy filtering condition
            So for example you can:
            add a dynamic attribute "size" with 3 possible values ['S', 'M', 'L'] to the nodes and 
            pass `node_filtering="size"` to the `render_tom_template` method
            expecting resolved template to have `<select>` element with S/M/L options lookup
            which will filter all nodes having selected option
            see example on `gitlab.com/22kittens/pyvisjs/examples/bluor.py`

        dropdown_auto_close: bool, default=True
            Closes the autocomplete dropdown menu in the tom-select control after item selection, if `True`  
            Drop down menu stays open after item selection, if `False`
            This flag translates into the `tom_select.close()` call at the end of the `onChange` event (see `templates/init_tomSelect.js`)

        Notes
        -----
        The data injected will be:

        >>> .render(
        >>>     width=network_dict["options"].get("width", "100%"),
        >>>     height=network_dict["options"].get("height", "100%"),
        >>>     data=network_dict,
        >>>     pyvisjs={
        >>>         "enable_highlighting": enable_highlighting,
        >>>         "edge_filtering_lookup": edge_filtering_lookup,
        >>>         "node_filtering_lookup": node_filtering_lookup,
        >>>         "title": title,
        >>>         "dropdown_auto_close": dropdown_auto_close,
        >>>     },
        >>> )

        you can find more details about `edge_filtering_lookup` and `node_filtering_lookup` structure here `tests\\test_network.py\\test_network_render_template_edge_filtering_list`
        """          
        
         
        return self.render(
            open_in_browser=open_in_browser,
            save_to_output=save_to_output,
            output_filename=output_filename)
        
