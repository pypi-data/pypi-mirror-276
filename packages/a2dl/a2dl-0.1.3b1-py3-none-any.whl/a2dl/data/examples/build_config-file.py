import os, argparse

import a2dl.core.constants
import a2dl.core.library


def makeit():

    # Initialize the parser
    parser = argparse.ArgumentParser(
        description='Script to build a draw.io library')

    # Add arguments
    parser.add_argument('--target_dir', nargs='?', default='./test/Downloads', help='Path to write files to.')
    parser.add_argument('--win', action='store_true', help='Specify if running on Windows.')
    parser.add_argument('--config', default=a2dl.core.constants.get_package_data_path('examples/example.config.ini'),
                        help='Path to the configuration file.')
    # Parse the arguments
    args = parser.parse_args()

    # Set target directory
    TARGETPATH = args.target_dir.rstrip("/")
    CONFIG_FILE_PATH = os.path.abspath(args.config)

    a2dl.core.constants.logger.info(f'target directory: {TARGETPATH}')
    a2dl.core.constants.logger.info(f'config file path: {CONFIG_FILE_PATH}')

    # this does not work
    a2dl.core.constants.set_config_file_path(CONFIG_FILE_PATH)

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


    # convert adoc 2 library
    a2dllib = a2dl.core.library.Diaglibrary()
    a2dllib.image_base_path = './data/examples/images/'
    a2dllib.from_folder('./data/examples/docs/')
    a2dllib.write(f'{TARGETPATH}/build-library.xml')


if __name__ == '__main__':
    print('start')

    makeit()

    print('done')
