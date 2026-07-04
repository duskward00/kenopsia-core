from __future__ import annotations
import argparse
from .engine import run_collectors
from .report import render
from .version import PRODUCT_NAME, __version__


def main(argv=None):
    p=argparse.ArgumentParser(prog='kenopsia', description=f'{PRODUCT_NAME} system assessment')
    p.add_argument('--output-dir', default='reports')
    p.add_argument('--json-only', action='store_true')
    p.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    args=p.parse_args(argv)
    data=run_collectors()
    html, jsn=render(data, args.output_dir)
    print(f'{PRODUCT_NAME} {__version__}')
    print(f'Generated: {jsn}')
    if not args.json_only: print(f'Generated: {html}')
