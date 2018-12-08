#!/usr/bin/env python3
"""Create a new website project."""

import os
import sys
import argparse
import subprocess
import shutil


VERSION = "0.0"
VERBOSE = False
DEBUG = False


def main():
    args = parse_cmd_line()
    prepare_destination(args.destination)
    init_git()
    if not args.project_name:
        _, name = os.path.split(args.destination)
        args.project_name = name
    dprint('Using "%s" as project name.' % args.project_name)
    create_readme(args)
    copy_makefile(args)
    add_rollup_config(args)
    add_node_modules_link()
    add_src_files(args)


def parse_cmd_line():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--version', help='Print the version and exit.', action='version',
        version='%(prog)s {}'.format(VERSION))
    DebugAction.add_parser_argument(parser)
    VerboseAction.add_parser_argument(parser)
    parser.add_argument('destination', metavar="PROJECT_DIR",
                        help="Destination to build your new project in.")
    parser.add_argument('--project-name', default='',
                        help=("Use this to specify a project name in case "
                              "it differs from the given destination "
                              "directory."))
    return parser.parse_args()


def prepare_destination(destination):
    """Prepare the destination directory."""
    # if project directory already exists, exit cowardly
    if os.path.exists(destination):
        print('The destination already appears to exist. To ensure this '
              'script works correctly, please chose a destination that '
              'does not yet exist.')
        sys.exit(1)

    # make new project directory
    vprint('Making new project directory.')
    os.mkdir(destination)

    # change the current working directory into the new projcet dir
    dprint('Changing work-dir to destination directory.')
    os.chdir(destination)


def init_git():
    """Initialize a git repository and clone website as a submodule."""
    vprint('Initializing new git repository')
    run(['git', 'init'], 'Error encountered initializing git repository.')

    vprint('Adding website repo as submodule.')
    url = 'https://bitbucket.org/fret/website.git'
    run(['git', 'submodule', 'add', url, 'website'],
        'Error encountered adding git submodule.')

    vprint('Committing the new submodule into the repo.')
    run(['git', 'commit', '-m', 'Add website submodule.'],
        'Error encountered committing submodule.')


def create_readme(args):
    """Create an empty readme file for the new project."""
    bar = "=" * len(args.project_name)
    contents = "{}\n{}\n{}\n\nTODO: add your readme content here.\n".format(
        bar, args.project_name, bar)
    vprint('Writing a template README file for the project.')
    fname = "README.rst"
    with open(fname, 'w') as readme:
        readme.write(contents)

    vprint('Committing README to repository.')
    run(['git', 'add', fname], 'Failed to stage readme in repo.')
    run(['git', 'commit', '-m', 'Add readme template.'],
        'Failed to commit readme to repo.')


def copy_makefile(args):
    """Copy the project makefile from submodule into project repo."""
    vprint('Copying project makefile from submodule into project repo.')
    shutil.copyfile('website/project.mk', 'makefile')

    vprint('Committing makefile to repository.')
    run(['git', 'add', 'makefile'], 'Failed to stage makefile in repo.')
    run(['git', 'commit', '-m', 'Add project makefile template.'],
        'Failed to commit makefile to repo.')


def add_rollup_config(args):
    """Add a config file for rollup.js to the project repo."""
    vprint('Adding configuration file for rollup.js')
    original_js = 'website.js'
    project_js = '{}.js'.format(args.project_name)
    rollup_fname = 'rollup.config.js'
    with open('website/%s' % rollup_fname, 'r') as source:
        with open(rollup_fname, 'w') as output:
            line = source.readline()
            while line != '':
                if original_js in line:
                    output.write(line.replace(original_js, project_js))
                else:
                    output.write(line)
                line = source.readline()

    vprint('Committing makefile to repository.')
    run(['git', 'add', rollup_fname], 'Failed to stage rollup config in repo.')
    run(['git', 'commit', '-m', 'Add rollup.js configuration file.'],
        'Failed to commit rollup config to repo.')


def add_node_modules_link():
    """Add a link in the top level dir to the node_modules install dir."""
    dirname = 'node_modules'
    vprint('Creating node_modules link.')
    run(['ln', '-s', 'website/%s' % dirname, dirname],
        'Failed to create link to node_modules dir.')

    vprint('Committing node_modules link to repository.')
    run(['git', 'add', dirname], 'Failed to stage node_modules link in repo.')
    run(['git', 'commit', '-m', 'Add link to node_modules dir in submodule.'],
        'Failed to commit node_modules link to repo.')


def add_src_files(args):
    """Create the src dir and some starter files for the new project."""
    vprint('Creating src directory structure.')
    for directory in ['src', 'src/pages', 'src/css', 'src/js']:
        os.mkdir(directory)

    vprint('Adding main css file template.')
    css_file = "{}.scss".format(args.project_name)
    shutil.copyfile('website/src/css/website.scss', 'src/css/%s' % css_file)

    vprint('Adding main javascript file template.')
    js_file = "{}.js".format(args.project_name)
    shutil.copyfile('website/src/js/website.js', 'src/js/%s' % js_file)

    vprint('Adding index.html template.')
    replacements = [('website.css', "{}.css".format(args.project_name)),
                    ('website.js', js_file)]
    with open('website/src/pages/index.html', 'r') as source:
        with open('src/pages/index.html', 'w') as output:
            line = source.readline()
            while line != '':
                for old, new in replacements:
                    if old in line:
                        line = line.replace(old, new)
                output.write(line)
                line = source.readline()

    vprint('Committing new src files to repository.')
    run(['git', 'add', 'src'], 'Failed to stage src dir in repo.')
    run(['git', 'commit', '-m', 'Add template source files.'],
        'Failed to commit src dir to repo.')


def run(command, err_msg):
    """Run a command, optionally print the output and handle errors."""
    proc = subprocess.run(command, capture_output=True)
    if proc.returncode == 0:
        # vprint(proc.stdout.decode(), indent='. ')
        dprint(proc.stdout.decode())
    else:
        print(err_msg)
        print(proc.stdout.decode())
        print(proc.stderr.decode())
        sys.exit(1)


def dprint(msg):
    """Conditionally print a debug message."""
    if DEBUG:
        print('DBG: ' + msg.replace('\n', '\nDBG: '))


def vprint(msg, indent=''):
    """Conditionally print a verbose message."""
    if VERBOSE:
        print(indent + msg.replace('\n', '\n' + indent))


class DebugAction(argparse.Action):
    """Enable the debugging output mechanism."""

    sflag = '-d'
    flag = '--debug'
    help = 'Enable debugging output.'

    @classmethod
    def add_parser_argument(cls, parser):
        parser.add_argument(cls.sflag, cls.flag, help=cls.help, action=cls)

    def __init__(self, option_strings, dest, **kwargs):
        super(DebugAction, self).__init__(option_strings, dest, nargs=0,
                                          default=False, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print('Enabling debugging output.')
        global DEBUG
        DEBUG = True
        setattr(namespace, self.dest, True)


class VerboseAction(DebugAction):
    """Enable the verbose output mechanism."""

    sflag = '-v'
    flag = '--verbose'
    help = 'Enable verbose output.'

    def __call__(self, parser, namespace, values, option_string=None):
        print('Enabling verbose output.')
        global VERBOSE
        VERBOSE = True
        setattr(namespace, self.dest, True)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except SystemExit:
        sys.exit(0)
    except KeyboardInterrupt:
        print('...interrupted by user, exiting.')
        sys.exit(1)
    except Exception as exc:
        import traceback
        traceback.print_exc()
        sys.exit(1)
