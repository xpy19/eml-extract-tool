#!/usr/bin/env python
# -*- coding: utf-8 -*-

import email
import logging
import os

import click

logging.basicConfig(level=logging.INFO)


def _extract_eml(file, output_dir):
    logging.info("start parse %s ......", file)

    with open(file, 'rb') as inf:
        msg = email.message_from_binary_file(inf)
        for part in msg.walk():
            if not part.is_multipart():
                name = part.get_filename()
                if name:
                    out_file = os.path.abspath(os.path.join(output_dir, name))
                    with open(out_file, 'wb') as o_stream:
                        o_stream.write(part.get_payload(decode=True))
                    logging.info('write attach file to %s', out_file)
                pass
            pass
        pass

    return


@click.command()
@click.option('--dir', '-d', type=click.STRING, required=True, help='Input .eml file directory')
@click.option('--output-dir', '-o', default='out', type=click.STRING, required=True, help='Output directory')
def cli(**kwargs):
    """Scan .eml file in directory and extract attach files"""
    input_dir = os.path.abspath(kwargs['dir'])
    output_dir = os.path.abspath(kwargs['output_dir'])
    logging.info("input  dir= %s", input_dir)
    logging.info("output dir= %s", output_dir)

    out_exist = os.path.isdir(output_dir)

    for base_dir, dirs, files in os.walk(input_dir):
        if not files:
            continue
        for f in files:  # type:str
            if not f.endswith('.eml'):
                continue
            if not out_exist:
                os.makedirs(output_dir)
                out_exist = True

            _extract_eml(os.path.join(base_dir, f), output_dir)
            pass
        pass

    return


if __name__ == '__main__':
    cli()
