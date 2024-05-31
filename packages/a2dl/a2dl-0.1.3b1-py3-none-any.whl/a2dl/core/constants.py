import os
import logging
import importlib.resources
import configparser

# create logger
logger = logging.getLogger('a2dl')
logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
logger.addHandler(sh)


def get_package_data_path(filename: str, p: bool = False) -> str:
    if p:
        ref = importlib.resources.files('a2dl.data') / filename
        with importlib.resources.as_file(ref) as path:
            strpath = str(path)
        return strpath
    else:
        return f'data/{filename}'


# Add this function to set the configuration file path
def set_config_file_path(config_file_path: str):
    global config
    config = configparser.RawConfigParser()
    config.read(os.path.abspath(get_package_data_path(config_file_path)))
    print(vars(config))
    logger.info(f'Configuration file set to {os.path.abspath(get_package_data_path(config_file_path))}')

# todo: activate to test config file option
# set_config_file_path('default.config.ini')


def cfg(itm: str = None,
        val: str | int | list | bool | tuple | dict | tuple[float, float, float, float] = None,
        pre: str | int | list | bool | tuple | dict | tuple[float, float, float, float] = None,
        nnm: str = 'A2DL_') \
        -> str | int | list | bool | tuple | dict | tuple[float, float, float, float]:
    """

    Config priority:
    0) set config and an environment variable if itm and val are set
    1) set config by environment variables starting with "A2DL_" and append the constants name like "A2DL_WORKDIR"
    2) set config by file
    3) set config by code defaults

    -> returns the config value

    """
    cfg_val = None

    if itm and val:
        # set
        os.environ[itm] = val
        cfg_val = val
        logger.info(f'Configuration {itm} set to {cfg_val}')
        return os.environ[itm]

    elif itm and not val:
        # get from config
        try:
            # get from environment
            cfg_val = os.environ[f'{nnm}{itm}']
            logger.info(f'Configuration {itm} set from environment variable to {cfg_val}')
            return cfg_val
        except KeyError:
            logger.warning(f'Configuration {itm} not found in environment or file.')
            # todo: read from file here
            # get from file
            # cfg_val = config.get('DEFAULT', itm, fallback=None)
            # if cfg_val:
            #     logger.info(f'Configuration {itm} set from file to {cfg_val}')
            #     return cfg_val
            # else:
            #     logger.warning(f'Configuration {itm} not found in environment or file.')

    if pre and not cfg_val:
        # return default
        logger.info(f'Configuration {itm} set from code defaults to {pre}')
        return pre
    else:
        raise ValueError(f"configuration item '{itm}' not found and no default value given")

# todo: INI file might be a bad choice. need to parse the types individually. for now, everything is string.
ADOC_ENCODING = cfg('ADOC_ENCODING', pre='utf-8')  # 'utf-8' # cp1252 utf-8

dd = f'{os.getcwd()}/data'
DATADIR = os.path.abspath(cfg('DATADIR', pre=dd))
# print(f'INFO a2dl for test and examples, the data directory is set to: {DATADIR}')

td = f'{os.getcwd()}/../test'
TEMPDIR = os.path.abspath(cfg('DATADIR', pre=td))
# print(f'INFO a2dl for test and examples, the target directory is set to: {TEMPDIR}')

# The following string determines the file search pattern:
GLOB_STRING = cfg('GLOB_STRING', pre='**/*.adoc')  # Search for all adoc files recursively

# Detecting relevant lines in files can be customized with the following strings:
ADOC_VARIABLE_IDENTIFIER = cfg('ADOC_VARIABLE_IDENTIFIER', pre=[["==", "===", "====", "====="],
                                                                ":variable_name:"])  # Extract content afer each identifier until the next occurrence of i in [0]
ADOC_ICON_IDENTIFIER = cfg('ADOC_ICON_IDENTIFIER', pre=":icon_image_rel_path:")
ADOC_ICON_TITLE_IDENTIFIER = cfg('ADOC_ICON_TITLE_IDENTIFIER', pre=":icon_name:")
ADOC_ICON_MORE_IDENTIFIER = cfg('ADOC_ICON_MORE_IDENTIFIER', pre=':read_more:')
LINES2SKIP = cfg('LINES2SKIP', pre=['[quote', 'image::'])  # skips lines starting with

# Formatting of the Tooltip can be customized with the following strings:
HTML_TOOLTIP = cfg('HTML_TOOLTIP',
                   pre='<h1 class="dio_tooltip" >%name%</h1>')  # The HTML for each section will get appended to this string
HTML_SECTION = cfg('HTML_SECTION', pre='<h2 class="dio_tooltip" >{}</h2>%{}%')  # variable['title'], variable['name']
HTML_WARNING = cfg('HTML_WARNING', pre='<b class="dio_tooltip" >{}</b>')

# "read more" will be the last line in the html tooltip
HTML_MORE_BASEURL = cfg('HTML_MORE_BASEURL', pre='{}')  # 'or: use a base ur like https://example.com/{}
#      if articles details page share the same base url'
HTML_MORE = cfg('HTML_MORE', pre='<br> <a href="{}" target="_more">Image generated with Stable Diffusion</a>')

# Icon styling
ICON_STYLE = cfg('ICON_STYLE', pre="rounded=1;whiteSpace=wrap;html=1;")

# If sections include images as .png, these will be encoded and included. The image styling can be modified:
IMAGE_STYLE = cfg('IMAGE_STYLE',
                  pre='fillColor=none;rounded=1;shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/{},{};')  # The type and image data are set from the file

# Generator settings
ARTICLE_TEMPLATE = cfg('ARTICLE_TEMPLATE', pre='data/examples/docs/template_article.adoc')
IMAGES_PATH = cfg('IMAGES_PATH', pre='data/examples/images')
IMAGES_GLOB_STRING = cfg('IMAGES_GLOB_STRING', pre='**/*.png')
IMAGES_WIDTH = cfg('IMAGES_WIDTH', pre="70")
IMAGES_HEIGHT = cfg('IMAGES_HEIGHT', pre="70")
IMAGES_ENFORCE_SIZE = cfg('IMAGES_ENFORCE_SIZE', pre=True)

# Graph
# how shall the arrows look?
GRAPH_EDGE_STYLE = cfg('GRAPH_EDGE_STYLE',
                       pre="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;")
# style of a box, if a node is not found in a library
GRAPH_BOX_STYLE = cfg('GRAPH_BOX_STYLE', pre="rounded=1;whiteSpace=wrap;html=1;")
GRAPH_LAYOUT = cfg('GRAPH_LAYOUT', pre='spring')  # spiral, spectral, shell, circular, spring
GRAPH_SCALE = cfg('GRAPH_SCALE', pre=20)
GRAPH_CENTER = cfg('GRAPH_CENTER', pre=(500, 500))
GRAPH_IMAGES_WIDTH: str = cfg('GRAPH_IMAGES_WIDTH', pre="70")
GRAPH_IMAGES_HEIGHT: str = cfg('GRAPH_IMAGES_HEIGHT', pre="70")
GRAPH_VALUE_SCALES: tuple[float, float, float, float] = cfg('GRAPH_VALUE_SCALES', pre=(-1.0, 1.0, 0.0, 3000.0))

# Diagram
DIAGRAM_SETUP: dict = cfg('DIAGRAM_SETUP', pre={
    "dx": "1114",
    "dy": "822",
    "pageWidth": "1169",
    "pageHeight": "827"
})

# While updating a diagram, these attributes of used icons in a diagram will not get overwritten
EXCLUDE_ATTRIBS: list[str] = cfg('EXCLUDE_ATTRIBS', pre=['x', 'y', 'width', 'height', 'id', 'name'])
