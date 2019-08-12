# -*- coding: utf-8 -*-
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import json
import logging
from docopt import docopt, DocoptExit

from discodoc import __appname__, __version__
from discodoc.core import DiscodocCommand
from discodoc.util import normalize_options, setup_logging

log = logging.getLogger(__name__)


def run():
    """
    discodoc - create hardcopy-like documents from Discourse content easily

    Usage:
      discodoc <url> [--format=<format>] [--renderer=<renderer>] [--path=<output-path>] [--api-key=<api-key>] [--debug]
      discodoc --version
      discodoc (-h | --help)

    Options:
      --format=<format>                 Output format.
                                        Use any format of pandoc, e.g. pdf, epub. [Default: pdf]
      --renderer=<renderer>             Output renderer.
                                        When using --format=pdf, choose --renderer=latex|beamer|context|ms|html5
                                        When using --format=html, choose --renderer=s5|slidy|slideous|dzslides|revealjs
                                        The default is to use the "pdflatex" renderer for creating PDF documents.
                                        For HTML documents, the renderer is optional.
      --path=<path>                     Output directory. Defaults to the current working directory.
      --api-key=<api-key>               Discourse API key. Can also be obtained through environment
                                        variable "DISCOURSE_API_KEY".
      --version                         Show version information
      --debug                           Enable debug messages
      -h --help                         Show this screen

    Examples::

        # Define URL.
        export TOPIC_URL=https://community.hiveeyes.org/t/anleitung-aufbau-und-installation-des-sensor-kits-grune-platine/2443

        # Generate PDF document from all posts of given topic.
        # This uses the default "pdflatex" renderer.
        discodoc "$TOPIC_URL" --format=pdf

        # Generate PDF document using the "wkhtmltopdf" renderer.
        discodoc "$TOPIC_URL" --format=pdf --renderer=html

        # Generate PDF slideshow using the "beamer" latex package.
        discodoc "$TOPIC_URL" --format=pdf --renderer=beamer

        # Generate HTML presentation/slideshow using reveal.js.
        # https://github.com/hakimel/reveal.js
        discodoc "$TOPIC_URL" --format=html --renderer=revealjs

        # Generate HTML presentation/slideshow using S5.
        # https://meyerweb.com/eric/tools/s5/
        discodoc "$TOPIC_URL" --format=html --renderer=s5

    """

    name = '{__appname__} {__version__}'.format(**globals())

    # Parse command line arguments
    options = normalize_options(docopt(run.__doc__, version=name))

    # Setup logging
    debug = options.get('debug')
    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    setup_logging(log_level)

    # Debugging
    log.debug('Options: {}'.format(json.dumps(options, indent=4)))

    # Run command, optionally multiple times.
    command = DiscodocCommand(options)
    results = command.run()
