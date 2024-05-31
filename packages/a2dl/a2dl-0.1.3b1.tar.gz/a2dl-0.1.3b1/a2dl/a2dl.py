# -*- coding: utf-8 -*-
"""
a2dl | (A)sciidoc(2D)rawio(L)ibrary | https://tigabeatz.net | MIT Licence

- Generates draw.io libraries from AsciiDoc-based descriptions.
- Updates icons within draw.io diagrams based on those libraries.

"""

from os.path import abspath, dirname, join
import glob

"""
TEST
"""
from .core.constants import DATADIR as DATADIR
from .core.constants import TEMPDIR as TEMPDIR

"""
CORE
"""

from .core.constants import GLOB_STRING as GLOB_STRING
from .core.constants import LINES2SKIP as LINES2SKIP
from .core.constants import ADOC_VARIABLE_IDENTIFIER as ADOC_VARIABLE_IDENTIFIER
from .core.constants import ADOC_ICON_IDENTIFIER as ADOC_ICON_IDENTIFIER
from .core.constants import ADOC_ICON_TITLE_IDENTIFIER as ADOC_ICON_TITLE_IDENTIFIER
from .core.constants import ADOC_ICON_MORE_IDENTIFIER as ADOC_ICON_MORE_IDENTIFIER

from .core.constants import HTML_TOOLTIP as HTML_TOOLTIP
from .core.constants import HTML_SECTION as HTML_SECTION
from .core.constants import HTML_WARNING as HTML_WARNING
from .core.constants import HTML_MORE_BASEURL as HTML_MORE_BASEURL
from .core.constants import HTML_MORE as HTML_MORE

from .core.constants import ICON_STYLE as ICON_STYLE
from .core.constants import IMAGE_STYLE as IMAGE_STYLE
from .core.constants import ARTICLE_TEMPLATE as ARTICLE_TEMPLATE

from .core.constants import IMAGES_PATH as IMAGES_PATH
from .core.constants import IMAGES_GLOB_STRING as IMAGES_GLOB_STRING
from .core.constants import IMAGES_WIDTH as IMAGES_WIDTH
from .core.constants import IMAGES_HEIGHT as IMAGES_HEIGHT
from .core.constants import IMAGES_ENFORCE_SIZE as IMAGES_ENFORCE_SIZE

from .core.constants import GRAPH_EDGE_STYLE as GRAPH_EDGE_STYLE
from .core.constants import GRAPH_BOX_STYLE as GRAPH_BOX_STYLE
from .core.constants import GRAPH_IMAGES_HEIGHT as GRAPH_IMAGES_HEIGHT
from .core.constants import GRAPH_IMAGES_WIDTH as GRAPH_IMAGES_WIDTH

from .core.constants import DIAGRAM_SETUP as DIAGRAM_SETUP
from .core.constants import GRAPH_VALUE_SCALES as GRAPH_VALUE_SCALES

from .core.constants import logging as logging
from .core.constants import logger as logger
from .core.constants import get_package_data_path as get_package_data_path
from .core.constants import cfg

from .core.icon import Diagicon as Diagicon
from .core.library import Diaglibrary as Diaglibrary
from .core.diagram import Diagdiagram as Diagdiagram

"""
File Format EXTENSIONS
"""
from .extensions.convert import to_pptx as to_pptx
from .extensions.convert import to_docx as to_docx
from .extensions.convert import to_ea as to_ea

"""
Helpers EXTENSIONS
"""
from .extensions.helpers import make_example as make_example
from .extensions.helpers import my_environment as my_environment
from .extensions.helpers import make_utf8 as make_utf8
from .extensions.helpers import packages_installed as packages_installed
"""
Graph EXTENSIONS
"""
from .extensions.relation import IconRelation as IconRelation
from .extensions.relation import IconRelations as IconRelations

"""
AI EXTENSIONS
ai based functions to generate diagrams, images, texts and icons.
"""
# from .extensions.constants import MODEL_GPU_TEXT as MODEL_GPU_TEXT
# from .extensions.constants import MODEL_CPU_TEXT as MODEL_CPU_TEXT
#
# from .extensions.constants import MODEL_GPU_TEXT2IMAGE as MODEL_GPU_TEXT2IMAGE
# from .extensions.constants import MODEL_CPU_TEXT2IMAGE as MODEL_CPU_TEXT2IMAGE
#
# from .extensions.ai import feed as feed

"""
CLI
"""
from .cli import cli as cli



"""
Logger
"""
logging.StreamHandler()


if __name__ == '__main__':
    cli()
