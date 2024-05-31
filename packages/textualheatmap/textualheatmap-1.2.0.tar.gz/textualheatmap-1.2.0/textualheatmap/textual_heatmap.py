
import uuid
import json
import os.path as path
import IPython
from typing import TypedDict, Callable

web_assets_dir = path.join(path.dirname(path.realpath(__file__)), 'web_assets')

class TokenData(TypedDict):
    token: str
    meta: list[str]|None
    heat: list[float]

class TextualHeatmap:
    def __init__(self,
                 show_meta: bool = False,
                 facet_titles: list[str] = ['Heatmap'],
                 rotate_facet_titles: bool = False,
                 wrap_after_token: bool = True,
                 width: int = 600,
                 interactive: bool = True,
                 display_fn: Callable=IPython.display.display
    ):
        """Create interactive textual heatmaps for Jupiter notebooks.

        This is useful for PyTorch or pure TensorFlow. You should properly use
        `KerasLearningCurve` if you use keras.

        Line description: dict with the properties `name` and `color`.
        Axis description:

        Example:
            heatmap = TextualHeatmap(
                show_meta = True,
                facet_titles = ['LSTM', 'GRU']
            )
            heatmap.set_data([
                [{
                    "token": 'a',
                    "meta": ['and', 'africa', 'america'],
                    "heat": [1, 0, 0]
                }, {
                    "token": 'n',
                    "meta": ['and', 'anecdote', 'antelope'],
                    "heat": [0.3, 0.7, 0]
                }, {
                    "token": 'd',
                    "meta": ['and', 'andante', 'andosol'],
                    "heat": [0.2, 0.3, 0.5]
                }],
                [{
                    "token": 'a',
                    "meta": ['and', 'africa', 'america'],
                    "heat": [1, 0, 0]
                }, {
                    "token": 'n',
                    "meta": ['and', 'anecdote', 'antelope'],
                    "heat": [0.1, 0.9, 0]
                }, {
                    "token": 'd',
                    "meta": ['and', 'andante', 'andosol'],
                    "heat": [0.1, 0.1, 0.8]
                }]
            ])
            heatmap.highlight(1)

        Args:
            show_meta (bool, optional): The meta texts on top of each facet. Defaults to False.
            facet_titles (list[str], optional): The title on each facet. Defaults to ['Heatmap'].
            rotate_facet_titles (bool, optional): If true, the facet titles will be rotated 90deg. Defaults to False.
            wrap_after_token (bool, optional): If wrap is allowed after token, otherwise it's only after space and hypens. Defaults to True.
            width (int, optional): The width of the heatmap. Defaults to 600.
            interactive (bool, optional): Should the heatmap be interactive on mouseover.. Defaults to True.
            display_fn (Callable, optional): _description_. Defaults to IPython.display.display.
        """
        if not isinstance(width, int) or width <= 0:
            raise ValueError(f'width must be a positive number, was {width}')

        if not isinstance(show_meta, bool):
            raise ValueError('show_meta must be a boolean')

        if not isinstance(interactive, bool):
            raise ValueError('interactive must be a boolean')

        if not isinstance(facet_titles, list):
            raise ValueError('facet_titles must be a list')
        for facet_title_i, facet_title in enumerate(facet_titles):
            if not isinstance(facet_title, str):
                raise ValueError(f'facet_title["{facet_title_i}"] must a string')

        if not isinstance(rotate_facet_titles, bool):
            raise ValueError('rotate_facet_titles must be a boolean')

        # Store settings
        self._display = display_fn
        self._settings = {
            'id': str(uuid.uuid4()),
            'width': width,
            'showMeta': show_meta,
            'facetTitles': facet_titles,
            'rotateFacetTitles': rotate_facet_titles,
            'wrapAfterTokens': wrap_after_token,
            'interactive': interactive
        }

        # Prepear data containers
        self._data = []
        self._display(self._create_inital_html())
        self._data_element = self._display(
            IPython.display.Javascript('void(0);'),
            display_id=True
        )
        self._highlight_element = self._display(
            IPython.display.Javascript('void(0);'),
            display_id=True
        )

    def _create_inital_html(self):
        with open(path.join(web_assets_dir, 'textual_heatmap.css')) as css_fp, \
             open(path.join(web_assets_dir, 'textual_heatmap.js')) as js_fp:
            return IPython.display.HTML(
                f'<style>{css_fp.read()}</style>'
                f'<script>{js_fp.read()}</script>'
                f'<div id="{self._settings["id"]}" class="textual-heatmap"></div>'
                f'<script>'
                f'  window.setupTextualHeatmap({json.dumps(self._settings)});'
                f'</script>'
            )

    def set_data(self, data: list[list[TokenData]]):
        """Sets the data and render the heatmap.

        `data` is a list of `FacetData`. Each `FacetData` is a
        list of `TokenData`.

            TokenData = {"token": str, "meta": List[str], "heat": List[float], "format": bool}

        * The `token` is what is displayed in the main text window.
        * The `meta` is used if `show_meta` is set to `True` in `TextualHeatmap`. This is
            displayed above the main text window.
        * The `heat` is is a ratio from 0 to 1, that will map to a color. 0 meaning there
          is no heat, and 1 is full heat. The `heat` values does not have to sum to 1.
        * The `format` is used to indicate tokens that are not seen by the model. For example
          space charecters if word or sub-word tokenization is used. In this case,
        `meta` and `heat` have no meaning.

        Examples:
            data = [[
                { "token": "context", "meta": ["content", "concise", "context"], "heat": [0, 0.2] },
                { "token": " ", "format": True },
                { "token": "is", "meta": ["are", "that", "is"], "heat": [0.7, 0] }
            ]]

        Args:
            data (list[TokenData]): Heatmap data.
        """
        disp = IPython.display.HTML(
            f'<script>'
            f'  window.setDataTextualHeatmap({json.dumps(self._settings)}, {json.dumps(data)});'
            f'</script>'
        )
        self._data_element.update(disp)

    def highlight(self, index: int):
        """Select a token index to be highlighted on the heatmap.

        This will affect all facets in the heatmap.

        Args:
            index (int): The token index to highlight.
        """
        disp = IPython.display.HTML(
            f'<script>'
            f'  window.highlightTextualHeatmap({json.dumps(self._settings)}, {index});'
            f'</script>'
        )
        self._highlight_element.update(disp)
