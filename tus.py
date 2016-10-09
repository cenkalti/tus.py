import os
import base64
import logging
import argparse

import requests

LOG_LEVEL = logging.INFO
DEFAULT_CHUNK_SIZE = 4 * 1024 * 1024
TUS_VERSION = '1.0.0'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TusError(Exception):
    pass


def _init():
    fmt = "[%(asctime)s] %(levelname)s %(message)s"
    h = logging.StreamHandler()
    h.setLevel(LOG_LEVEL)
    h.setFormatter(logging.Formatter(fmt))
    logger.addHandler(h)


def _create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=argparse.FileType('rb'))
    parser.add_argument('--chunk-size', default=DEFAULT_CHUNK_SIZE)
    parser.add_argument(
        '--authorization',
        help="Authorization header value to be sent with requests")
    return parser


def _cmd_upload():
    _init()

    parser = _create_parser()
    parser.add_argument('tus_endpoint')
    parser.add_argument('--file_name')
    parser.add_argument(
        '--metadata',
        action='append',
        help="A single key/value pair to be sent with the upload request."
        "Can be specified multiple times to send more than one key/value pair."
        "Key and value must be separated with space.")
    args = parser.parse_args()

    metadata = dict([x.split() for x in args.metadata])

    upload(
        args.file,
        args.tus_endpoint,
        chunk_size=args.chunk_size,
        file_name=args.file_name,
        authorization=args.authorization,
        metadata=metadata)


def _cmd_resume():
    _init()

    parser = _create_parser()
    parser.add_argument('file_endpoint')
    args = parser.parse_args()

    resume(
        args.file,
        args.file_endpoint,
        chunk_size=args.chunk_size,
        authorization=args.authorization)


def upload(file_obj,
           tus_endpoint,
           chunk_size=DEFAULT_CHUNK_SIZE,
           file_name=None,
           authorization=None,
           metadata=None):
    file_name = os.path.basename(file_obj.name)
    file_size = _get_file_size(file_obj)
    location = _create_file(
        tus_endpoint,
        file_name,
        file_size,
        authorization=authorization,
        metadata=metadata)
    resume(
        file_obj, location, chunk_size=chunk_size, authorization=authorization)


def _get_file_size(f):
    pos = f.tell()
    f.seek(0, 2)
    size = f.tell()
    f.seek(pos)
    return size


def _create_file(tus_endpoint,
                 file_name,
                 file_size,
                 authorization=None,
                 metadata=None):
    logger.info("Creating file endpoint")

    headers = {
        "Tus-Resumable": TUS_VERSION,
        "Upload-Length": str(file_size),
    }

    if authorization:
        headers["Authorization"] = authorization

    if metadata:
        l = [k + ' ' + base64.b64encode(v) for k, v in metadata.items()]
        headers["Upload-Metadata"] = ','.join(l)

    response = requests.post(tus_endpoint, headers=headers)
    if response.status_code != 201:
        raise TusError("Create failed: %s" % response)

    location = response.headers["Location"]
    logger.info("Location: %s", location)
    return location


def resume(file_obj,
           file_endpoint,
           chunk_size=DEFAULT_CHUNK_SIZE,
           authorization=None):
    file_size = _get_file_size(file_obj)
    offset = _get_offset(file_endpoint, authorization=authorization)
    while offset < file_size:
        file_obj.seek(offset)
        data = file_obj.read(chunk_size)
        offset = _upload_chunk(
            data, offset, file_endpoint, authorization=authorization)


def _get_offset(file_endpoint, authorization=None):
    logger.info("Getting offset")

    headers = {"Tus-Resumable": TUS_VERSION}

    if authorization:
        headers["Authorization"] = authorization

    response = requests.head(file_endpoint, headers=headers)
    response.raise_for_status()

    offset = _extract_offset(response)
    logger.info("Offset: %s", offset)
    return offset


def _upload_chunk(data, offset, file_endpoint, authorization=None):
    logger.info("Uploading chunk")

    headers = {
        'Content-Type': 'application/offset+octet-stream',
        'Upload-Offset': str(offset),
        'Tus-Resumable': TUS_VERSION,
    }

    if authorization:
        headers['Authorization'] = authorization

    response = requests.patch(file_endpoint, headers=headers, data=data)
    if response.status_code != 204:
        raise TusError("Upload chunk failed: %s" % response)

    offset = _extract_offset(response)
    logger.info("Offset: %s", offset)
    return offset


def _extract_offset(response):
    return int(response.headers["Upload-Offset"])
