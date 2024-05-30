import argparse
from .sra.parser import sra_object_generator
import urllib.request
import orjson
import gzip
import tempfile
from upath import UPath
import shutil

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL to parse")
    parser.add_argument("outfile", help="Output file")

    args = parser.parse_args()

    # while it is technically possible to stream from the URL
    # the safer way is to download the file first
    with tempfile.NamedTemporaryFile() as tmpfile:

        # download the file to a temporary file
        shutil.copyfileobj(UPath(args.url).open("rb"), tmpfile)
        # read the file and write to the output file
        tmpfile.seek(0)
        with gzip.open(tmpfile, 'rb') as fh:
            with UPath(args.outfile).open('wb', compression='gzip') as outfile:

                # iterate over the objects and write them to the output file
                for obj in sra_object_generator(fh):
                    outfile.write(orjson.dumps(obj.data) + b"\n")

if __name__ == "__main__":
    cli()