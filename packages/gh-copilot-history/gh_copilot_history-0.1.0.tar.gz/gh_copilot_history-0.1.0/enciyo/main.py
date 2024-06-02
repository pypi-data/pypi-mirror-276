import os

import click
import subprocess

import utils


@click.command()
@click.option('--port', default=9696, help='Running port')
@click.option('--debug', default=False, help='Debug mode')
@click.argument('project', type=click.Path(exists=True), required=False, default=f"{os.getcwd()}")
def process(port, debug, output):
    launch = "mitmdump" if not debug else "mitmweb"
    shell = f"{launch} -s addons/binding.py -p {port}"
    subprocess.run(shell, shell=True)
    utils.WORKSPACE = output

if __name__ == '__main__':
    process()
