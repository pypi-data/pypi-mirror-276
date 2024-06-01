import os
import subprocess

import click

from . import _env
from .util import set_logger


logger = set_logger(__name__)


@click.command()
@click.argument('file_name', type=str)
@click.option('-o', '--opt', is_flag=True, default=False, help='Using Optimized Hive conf.')
@click.option('-p', '--print', is_flag=True, default=False, help='Print header.')
def hive_cli(file_name: str, opt: bool, print: bool) -> None:
    """Execute Hive query and redirect the output to a CSV file."""
    if not os.path.isfile(f'{file_name}.hql'):
        logger.warning(f'{file_name}.hql not found.')
    elif _env.check_hive_env() != 0:
        logger.warning("Hive not found. Please install Hive and add it to your PATH.")
    else:
        conf = ''
        if opt:
            conf += (
                '-hiveconf hive.exec.parallel=true '
                '-hiveconf hive.input.format=org.apache.hadoop.hive.ql.io.CombineHiveInputFormat '
                '-hiveconf hive.hadoop.supports.splittable.combineinputformat=true '
                '-hiveconf mapreduce.map.memory.mb=4096 '
                '-hiveconf mapreduce.map.java.opts=-Xmx3072m '
                '-hiveconf mapreduce.reduce.memory.mb=4096 '
                '-hiveconf mapreduce.reduce.java.opts=-Xmx3072m '
                '-hiveconf hive.merge.mapfiles=true '
                '-hiveconf hive.merge.mapredfiles=true '
                '-hiveconf hive.merge.size.per.task=256000000 '
                '-hiveconf hive.merge.smallfiles.avgsize=256000000 '
                '-hiveconf hive.auto.convert.join=true '
                '-hiveconf hive.mapjoin.smalltable.filesize=25000000 '
            )
        if print:
            conf += '-hiveconf hive.cli.print.header=true '
        command = f'hive {conf}-f {file_name}.hql > {file_name}.csv'
        logger.info(f'Run `{command}`')

        try:
            res = subprocess.run(command, shell=True, text=True)
            if res.returncode != 0:
                logger.warning('Failed to execute query.')
                logger.error(f'Error: {res.stderr}')
                logger.error(f'returncode: {res.returncode}')
        except Exception as e:
            logger.error(f'An Error occurred: {e}')
