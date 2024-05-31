import os, argparse


if __name__ == '__main__':
    """
        Config Monkey Patch
    """
    import a2dl.core.constants

    # a2dl.core.constants.logging.getLogger('a2dl').addHandler(a2dl.core.constants.logging.NullHandler())
    # a2dl.core.constants.logger.setLevel("INFO")

    # Formatting of the Tooltip can be customized with the following strings:
    a2dl.core.constants.HTML_TOOLTIP = '<h1 class="a2dl_tooltip">%name%</h1>' \
                                       '<h2 class="a2dl_tooltip" >Description</h2><p>%Description%</p>' \
                                       '<h2 class="a2dl_tooltip" >Example</h2><p>%Example%</p>'

    # "read more" will be the last line in the html tooltip
    a2dl.core.constants.HTML_MORE_BASEURL = ''
    a2dl.core.constants.HTML_MORE = '<br> <a href="{}" target="_more">Read More...</a>'

    # use .core.constants ICON_STYLE to style icons without images

    # If sections include images as .png, these will be encoded and included. The image styling can be modified:
    a2dl.core.constants.IMAGE_STYLE = '' \
                                      "fillColor=none;rounded=1;shape=image;verticalLabelPosition=bottom;" \
                                      "labelBackgroundColor=default;verticalAlign=top;aspect=fixed;" \
                                      "imageAspect=0;sketch=1;hachureGap=4;jiggle=2;curveFitting=1;" \
                                      "strokeWidth=1;fontFamily=Architects Daughter;" \
                                      "fontSource=https%3A%2F%2Ffonts.googleapis.com%2Fcss%3Ffamily%3DArchitects%2BDaughter;" \
                                      "fontSize=20;imageBorder=default;image=data:image/{},{};"  # The type and image data are set from the file

    # set the icon size in pixel
    a2dl.core.constants.IMAGES_WIDTH = "150"
    a2dl.core.constants.IMAGES_HEIGHT = "150"

    # Initialize the parser
    parser = argparse.ArgumentParser(
        description='Script to prepare a target directory and set environment for Windows.')

    # Add arguments
    parser.add_argument('target_dir', nargs='?', default='../test/Downloads', help='Path to write files to.')
    parser.add_argument('--win', action='store_true', help='Specify if running on Windows.')

    # Parse the arguments
    args = parser.parse_args()

    # Set target directory
    TARGETPATH = args.target_dir.rstrip("/")

    a2dl.core.constants.logger.info(f'target directory: {TARGETPATH}')

    # Check if Windows flag is set
    if args.win:
        a2dl.core.constants.logger.info('running on Windows')
        os.environ["PYTHONUTF8"] = "1"
        a2dl.core.constants.ADOC_ENCODING = 'windows-1252'
    else:
        a2dl.core.constants.logger.info('not running on Windows.')

    # Prepare target directory
    try:
        # os.system(f'rm {TARGETPATH} -rf')
        os.system(f'mkdir -p {TARGETPATH}')
    except Exception as e:
        a2dl.core.constants.logger.error(f'{e}')

    """
        Due to Monkey Patch, import this AFTER setting the configuration
    """
    import a2dl.core.library

    # convert adoc 2 library
    a2dllib = a2dl.core.library.Diaglibrary()
    a2dllib.image_base_path = './data/examples/images/'
    a2dllib.from_folder('./data/examples/docs/')
    a2dllib.write(f'{TARGETPATH}/build-library.xml')

