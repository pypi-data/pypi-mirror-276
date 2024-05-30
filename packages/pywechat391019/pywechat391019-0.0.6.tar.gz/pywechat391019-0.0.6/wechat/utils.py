import copy
import json
import os
import typing
import pathlib
import subprocess

import psutil
import xmltodict

BASE_DIR = pathlib.Path(__file__).resolve().parent

TOOLS = BASE_DIR / "tools"
START_WECHAT = TOOLS / "start-wechat.exe"
HOOK = TOOLS / "hook.exe"


def start_wechat() -> typing.Tuple[int, str]:
    result = subprocess.run(START_WECHAT, capture_output=True, text=True)
    code, output = result.stdout.split(",")
    return int(code), output


def hook(pid: int, ip: str, port: int, callback_url) -> None:
    subprocess.Popen(f"{HOOK} {pid} {ip}:{port} {callback_url}", stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)


def get_processes(process_name: str) -> typing.List[psutil.Process]:
    processes = []
    for process in psutil.process_iter():
        if process.name().lower() == process_name.lower():
            processes.append(process)
    return processes


def parse_xml(xml: str) -> dict:
    return xmltodict.parse(xml)


def parse_event(event: dict) -> dict:
    data = copy.deepcopy(event)
    for field in ["raw_msg"]:
        try:
            data["data"][field] = parse_xml(data["data"][field])
        except Exception:
            pass
    return data


def get_image_info(data: bytes) -> typing.Union[typing.Tuple[str, int], None]:
    if not data:
        raise Exception("data is empty!")

    JPEG = (0xFF, 0XD8, 0XFF)
    PNG = (0x89, 0x50, 0x4E)
    BMP = (0x42, 0x4D)
    GIF = (0x47, 0x49, 0x46)
    IMAGE_FORMAT_FEATURE = [JPEG, PNG, BMP, GIF]
    IMAGE_FORMAT = {0: "jpg", 1: "png", 2: "bmp", 3: "gif"}

    for i, FORMAT_FEATURE in enumerate(IMAGE_FORMAT_FEATURE):
        result = []
        image_feature = data[:len(FORMAT_FEATURE)]
        for j, format_feature in enumerate(FORMAT_FEATURE):
            result.append(image_feature[j] ^ format_feature)

        sum = result[0]
        for k in result:
            sum ^= k

        if sum == 0:
            return IMAGE_FORMAT[i], result[0]


def decode_image_data(data: bytes, key: int) -> bytes:
    image_data = []
    for byte in data:
        image_data.append(byte ^ key)
    return bytes(image_data)


def decode_image(src_file: str, output_path: str = ".") -> typing.Tuple[str, str]:
    src_file = pathlib.Path(src_file)
    output_path = pathlib.Path(output_path)
    dat_filename = src_file.name.replace(".dat", "")
    with open(src_file, "rb") as dat_file:
        data = dat_file.read()

    suffix, key = get_image_info(data)
    image_data = decode_image_data(data, key)

    image_filename = output_path / f"{dat_filename}.{suffix}"
    with open(image_filename, "wb") as f:
        f.write(image_data)

    return str(src_file.absolute()), str(image_filename.absolute())


class WeChatManager:

    def __init__(self):
        # remote port: 19001 ~ 37999
        # socket port: 18999 ~ 1
        # http port:   38999 ~ 57997
        self.filename = BASE_DIR / "wechat.json"
        if not os.path.exists(self.filename):
            self.init_file()
        else:
            self.clean()

    def init_file(self) -> None:
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump({
                "increase_remote_port": 19000,
                "wechat": []
            }, file)

    def read(self) -> dict:
        with open(self.filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    def write(self, data: dict) -> None:
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file)

    def refresh(self, pid_list: typing.List[int]) -> None:
        data = self.read()
        cleaned_data = []
        remote_port_list = [19000]
        for item in data["wechat"]:
            if item["pid"] in pid_list:
                remote_port_list.append(item["remote_port"])
                cleaned_data.append(item)

        data["increase_remote_port"] = max(remote_port_list)
        data["wechat"] = cleaned_data
        self.write(data)

    def clean(self) -> None:
        pid_list = [process.pid for process in get_processes("WeChat.exe")]
        self.refresh(pid_list)

    def get_remote_port(self) -> int:
        data = self.read()
        return data["increase_remote_port"] + 1

    def get_listen_port(self, remote_port: int) -> int:
        return 19000 - (remote_port - 19000)

    def get_port(self) -> typing.Tuple[int, int]:
        remote_port = self.get_remote_port()
        return remote_port, self.get_listen_port(remote_port)

    def add(self, pid: int, remote_port: int, server_port: int) -> None:
        data = self.read()
        data["increase_remote_port"] = remote_port
        data["wechat"].append({
            "pid": pid,
            "remote_port": remote_port,
            "server_port": server_port
        })
        self.write(data)
