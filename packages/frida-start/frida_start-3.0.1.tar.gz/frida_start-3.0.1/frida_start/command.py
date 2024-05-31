#!/usr/bin/env python3

import argparse
import logging
import subprocess
import sys
import lzma
import pathlib
import time

import requests

from frida_start import __version__

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="[%(asctime)s] [%(name)s: %(levelname)s]: %(message)s",
)
log = logging.getLogger("frida-start")

try:
    from frida import __version__ as FRIDA_VERSION
except ImportError:
    log.error("Frida not found. Please run `pip install frida` to proceed.")
    sys.exit(1)

ADB_PATH = "adb"
DOWNLOAD_PATH = pathlib.Path.home() / ".frida-start"
CHUNK_SIZE = 1024 * 10
GETPROP_ARCHS = {
    "armeabi": "arm",
    "armeabi-v7a": "arm",
    "arm64-v8a": "arm64",
    "x86": "x86",
    "x86_64": "x86_64",
}


def get_connected_devices() -> dict[str, dict[str, str]]:
    cmd = f"{ADB_PATH} devices -l"
    output = (
        subprocess.check_output(cmd)
        .strip()
        .decode("utf-8")
        .replace("\r", "")
        .split("\n")
    )

    devices = set()
    for device in output[1:]:
        device = device.strip()
        if device != "":
            devices.add(tuple(device.split()))

    return {d[0]: {t.split(":")[0]: t.split(":")[1] for t in d[2:]} for d in devices}


def get_device_arch(transport_id: str) -> str:
    getprop_cmd = f"{ADB_PATH} -t {transport_id} shell getprop ro.product.cpu.abi"
    output = subprocess.check_output(getprop_cmd).lower().strip().decode("utf-8")
    if output not in GETPROP_ARCHS:
        raise RuntimeError("Could not determine device's arch")
    return GETPROP_ARCHS[output]


def get_download_url(arch: str) -> str:
    return f"https://github.com/frida/frida/releases/download/{FRIDA_VERSION}/frida-server-{FRIDA_VERSION}-android-{arch}.xz"


def download_and_extract(
    url: str, fpath: pathlib.Path, force_download: bool = False
) -> None:
    if fpath.is_file() and not force_download:
        log.info(f"Using {fpath.name} from downloaded cache")
        return

    fpath.parent.mkdir(exist_ok=True)
    data = None

    log.info(f"Downloading: {url}")
    req = requests.get(url, stream=True)
    req.raise_for_status()

    archive_path = fpath.with_suffix(".xz")

    req.raw.decode_content = True
    with open(archive_path, "wb") as fh:
        for chunk in req.iter_content(CHUNK_SIZE):
            fh.write(chunk)

    with lzma.open(archive_path) as fh:
        data = fh.read()

    archive_path.unlink()

    log.info(f"Writing file to {fpath}")
    fpath.write_bytes(data)


def push_and_execute(fpath: pathlib.Path, transport_id: str) -> None:
    push_cmd = [
        ADB_PATH,
        "-t",
        transport_id,
        "push",
        str(fpath),
        "/data/local/tmp/frida-server",
    ]
    chmod_cmd = [
        ADB_PATH,
        "-t",
        transport_id,
        "shell",
        "chmod 0755 /data/local/tmp/frida-server",
    ]
    kill_cmd = [
        ADB_PATH,
        "-t",
        transport_id,
        "shell",
        "su",
        "0",
        "killall",
        "frida-server",
    ]
    execute_cmd = [
        ADB_PATH,
        "-t",
        transport_id,
        "shell",
        "nohup",
        "su",
        "0",
        "/data/local/tmp/frida-server",
    ]

    res = subprocess.Popen(push_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res.wait()

    if res.returncode != 0:
        log.error(
            f"Could not push the binary to device. {res.stdout.read().decode()}{res.stderr.read().decode()}"
        )
        return

    log.info("File pushed to device successfully.")
    subprocess.Popen(chmod_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()

    log.info("Killing all frida-server on device.")
    subprocess.Popen(kill_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()

    log.info("Executing frida-server on device.")
    res = subprocess.Popen(execute_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(3)
    ret_code = res.poll()
    if ret_code is not None and ret_code != 0:
        decoded = res.stderr.readline().decode("utf-8")
        msg = f"Error executing frida-server. {decoded}"
        log.error(msg)
        raise RuntimeError(msg)
    res.kill()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--device-name", required=False)
    parser.add_argument(
        "-f", "--force", help="force download", action="store_true", default=False
    )
    parser.add_argument("-V", "--version", action="version", version=__version__)
    return parser.parse_args()


def main():
    args = parse_args()

    devices = get_connected_devices()
    if len(devices) == 0:
        log.error("No device found. Exiting.")
        return 1

    log.info("Devices: {}".format(", ".join(devices.keys())))

    if len(devices) != 1 and args.device_name is None:
        log.error("Multiple devices conected select one with -d")
        return 1
    elif args.device_name is not None and args.device_name not in devices:
        log.error(f"Device {args.device_name} not found")
        return 1

    if args.device_name is None:
        args.device_name = next(iter(devices.keys()), None)

    log.info(f"Current installed Frida version: {FRIDA_VERSION}")

    transport_id = devices[args.device_name]["transport_id"]
    arch = get_device_arch(transport_id=transport_id)
    log.info(f"Found arch: {arch}")

    url = get_download_url(arch)
    fpath = DOWNLOAD_PATH / f"frida-server-{FRIDA_VERSION}-android-{arch}"

    download_and_extract(url, fpath, args.force)
    push_and_execute(fpath, transport_id=transport_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
