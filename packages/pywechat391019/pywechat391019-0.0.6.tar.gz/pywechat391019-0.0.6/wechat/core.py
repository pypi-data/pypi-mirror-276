import binascii
import typing
import json
import socketserver
import threading
import traceback
import uuid

from multiprocessing import Process

import psutil
import pyee
import requests

from .logger import logger
from .events import ALL_MESSAGE
from .utils import WeChatManager, start_wechat, hook, get_processes


class ReqData:
    __response_message = None
    msg_type: int = 0
    request_data = None

    def __init__(self, msg_type, data):
        self.msg_type = msg_type
        self.request_data = data
        self.__wait_event = threading.Event()

    def wait_response(self, timeout=None):
        self.__wait_event.wait(timeout)
        return self.get_response_data()

    def on_response(self, message):
        self.__response_message = message
        self.__wait_event.set()

    def get_response_data(self):
        if self.__response_message is None:
            return None
        return self.__response_message["data"]


class RequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle(self):
        try:
            data = b""
            while True:
                chunk = self.request.recv(1024)
                data += chunk
                if len(chunk) == 0 or chunk[-2:] == b"0A":
                    break

            self.request.sendall("200 OK".encode())
            self.request.close()

            hex_data = data.split(b"\r\n\r\n", )[-1]
            wechat = getattr(self.server, "wechat")
            raw_data = binascii.unhexlify(hex_data).decode().rstrip("\n")
            logger.debug(raw_data)
            wechat.on_recv(json.loads(raw_data))

        except Exception:
            pass


class WeChat:

    def __init__(self, smart: bool = False):
        self.__req_data_cache = {}
        self.wechat_manager = WeChatManager()
        self.event_emitter = pyee.EventEmitter()
        self.remote_host = "127.0.0.1"
        self.server_host = "127.0.0.1"

        if smart:
            self.remote_port, self.server_port = 19088, 18999
            processes = get_processes("WeChat.exe")
            if not processes:
                code, output = start_wechat()
                if code == 1:
                    raise Exception(output)
                self.wechat = psutil.Process(int(output))
            else:
                self.wechat = processes[0]
        else:
            self.remote_port, self.server_port = self.wechat_manager.get_port()
            code, output = start_wechat()
            if code == 1:
                raise Exception(output)
            pid = int(output)
            self.wechat = psutil.Process(pid)

        self.api = f"http://127.0.0.1:{self.remote_port}/api/client/1"
        self.wechat_manager.add(self.wechat.pid, self.remote_port, self.server_port)
        self.client = Process(target=hook, args=(
        self.wechat.pid, self.remote_host, self.remote_port, f"http://{self.server_host}:{self.server_port}"))
        self.client.start()
        logger.info(f"API Server at {self.remote_host}:{self.remote_port}")

    def send(self, data: dict):
        return requests.post(self.api, data=binascii.hexlify(json.dumps(data, ensure_ascii=False).encode())).json()

    def send_sync(self, data: dict, timeout: int = 10):
        if data.get("trace") is None:
            data["trace"] = str(uuid.uuid4())

        req_data = ReqData(data["type"], data)
        self.__req_data_cache[data["trace"]] = req_data

        self.send(data)
        return req_data.wait_response(timeout)

    def on_event(self, data: dict):
        try:
            self.event_emitter.emit(str(ALL_MESSAGE), self, data)
            self.event_emitter.emit(str(data["type"]), self, data)
        except Exception:
            logger.error(traceback.format_exc())

    def on_recv(self, data: dict):
        if data.get("trace") is not None:
            req_data = self.__req_data_cache[data["trace"]]
            req_data.on_response(data)
            del self.__req_data_cache[data["trace"]]
        else:
            self.on_event(data)

    def handle(self, events: typing.Union[typing.List[str], str, None] = None, once: bool = False) -> typing.Callable[
        [typing.Callable], None]:
        def wrapper(func):
            listen = self.event_emitter.on if not once else self.event_emitter.once
            if not events:
                listen(str(ALL_MESSAGE), func)
            else:
                for event in events if isinstance(events, list) else [events]:
                    listen(str(event), func)

        return wrapper

    def refresh_qrcode(self):
        """刷新登录二维码"""
        data = {
            "type": 11087,
            "data": {}
        }
        return self.send(data)

    def logout(self):
        """退出登录"""
        data = {
            "type": 11104,
            "data": {}
        }
        return self.send(data)

    def exit(self):
        """退出微信"""
        data = {
            "type": 11105,
            "data": {}
        }
        return self.send(data)

    def get_self_info(self):
        """获取当前账号信息"""
        data = {
            "type": 11028,
            "data": {}
        }
        return self.send_sync(data)

    def get_contacts(self):
        """获取好友列表"""
        data = {
            "type": 11030,
            "data": {}
        }
        return self.send_sync(data)

    def get_contact(self, wxid: str):
        """获取好友信息"""
        data = {
            "type": 11029,
            "data": {
                "wxid": wxid
            }
        }
        return self.send_sync(data)

    def get_rooms(self, detail: int = 1):
        """获取群列表"""
        data = {
            "type": 11031,
            "data": {
                "detail": detail
            }
        }
        return self.send_sync(data)

    def get_room(self, room_wxid: str):
        """获取群信息"""
        data = {
            "type": 11125,
            "data": {
                "room_wxid": room_wxid
            }
        }
        return self.send_sync(data)

    def get_room_members(self, room_wxid: str):
        """获取群成员列表"""
        data = {
            "type": 11032,
            "data": {
                "room_wxid": room_wxid
            }
        }
        return self.send_sync(data)

    def get_public(self):
        """获取公众号列表"""
        data = {
            "type": 11033,
            "data": {}
        }
        return self.send_sync(data)

    def get_contact_by_protocol(self, wxid: str):
        """获取好友简要信息（协议）"""
        data = {
            "type": 11034,
            "data": {
                "wxid": wxid
            }
        }
        return self.send_sync(data)

    def get_room_member_by_net(self, room_wxid, wxid):
        """获取群成员信息"""
        data = {
            "type": 111035,
            "data": {
                "room_wxid": room_wxid,
                "wxid": wxid
            }
        }
        return self.send_sync(data)

    def send_text(self, to_wxid: str, content: str):
        """发送文本消息"""
        data = {
            "type": 11036,
            "data": {
                "to_wxid": to_wxid,
                "content": content
            }
        }
        return self.send(data)

    def send_room_at(self, to_wxid: str, content: str, at_list: typing.List[str]):
        """发送群at消息"""
        data = {
            "type": 11037,
            "data": {
                "to_wxid": to_wxid,
                "content": content,
                "at_list": at_list
            }
        }
        return self.send(data)

    def send_card(self, to_wxid: str, card_wxid: str):
        """发送名片消息"""
        data = {
            "type": 11038,
            "data": {
                "to_wxid": to_wxid,
                "card_wxid": card_wxid
            }
        }
        return self.send(data)

    def send_link(self, to_wxid: str, title: str, desc: str, url: str, image_url: str):
        """发送链接卡片消息"""
        data = {
            "type": 11039,
            "data": {
                "to_wxid": to_wxid,
                "title": title,
                "desc": desc,
                "url": url,
                "image_url": image_url
            }
        }
        return self.send(data)

    def send_image(self, to_wxid: str, file: str):
        """发送图片消息"""
        data = {
            "type": 11040,
            "data": {
                "to_wxid": to_wxid,
                "file": file
            }
        }
        return self.send(data)

    def send_file(self, to_wxid: str, file: str):
        """发送文件消息"""
        data = {
            "type": 11041,
            "data": {
                "to_wxid": to_wxid,
                "file": file
            }
        }
        return self.send(data)

    def send_video(self, to_wxid: str, file: str):
        """发送视频消息"""
        data = {
            "type": 11042,
            "data": {
                "to_wxid": to_wxid,
                "file": file
            }
        }
        return self.send(data)

    def send_emotion(self, to_wxid: str, file: str):
        """发送表情消息"""
        data = {
            "type": 11043,
            "data": {
                "to_wxid": to_wxid,
                "file": file
            }
        }
        return self.send(data)

    def send_xml(self, to_wxid: str, xml: str):
        """发送xml消息"""
        data = {
            "type": 11113,
            "data": {
                "to_wxid": to_wxid,
                "xml": xml
            }
        }
        return self.send(data)

    def send_pat(self, room_wxid: str, patted_wxid: str):
        """发送拍一拍消息"""
        data = {
            "type": 11250,
            "data": {
                "room_wxid": room_wxid,
                "patted_wxid": patted_wxid
            }
        }
        return self.send(data)

    def forward_msg(self, to_wxid: str, msg_id: str):
        """转发消息"""
        data = {
            "type": 11245,
            "data": {
                "to_wxid": to_wxid,
                "msgid": msg_id
            }
        }
        return self.send(data)

    def get_contact_detail_by_protocol(self, wxid: str):
        """获取好友详细信息（协议）"""
        data = {
            "type": 11174,
            "data": {
                "wxid": wxid
            }
        }
        return self.send_sync(data)

    def get_contacts_by_protocol(self, wxids: typing.List[str]):
        """获取多个好友信息（协议）"""
        data = {
            "type": 11174,
            "data": {
                "username_list": wxids
            }
        }
        return self.send_sync(data)

    def modify_contact_remark(self, wxid: str, remark: str):
        """修改好友备注"""
        data = {
            "type": 11063,
            "data": {
                "wxid": wxid,
                "remark": remark
            }
        }
        return self.send_sync(data)

    def delete_friend(self, wxid: str):
        """删除好友"""
        data = {
            "type": 11064,
            "data": {
                "wxid": wxid
            }
        }
        return self.send_sync(data)

    def accept_friend_request(self, encrypt_username: str, ticket: str, scene: int = 17):
        """同意好友请求"""
        data = {
            "type": 11065,
            "data": {
                "encryptusername": encrypt_username,
                "ticket": ticket,
                "scene": scene
            },
        }
        return self.send_sync(data)

    def search_friend(self, search: str):
        """搜索微信好友"""
        data = {
            "type": 11096,
            "data": {
                "search": search
            }
        }
        return self.send_sync(data)

    def add_friend(self, v1: str, v2: str, remark: str):
        """添加好友"""
        data = {
            "type": 11097,
            "data": {
                "v1": v1,
                "v2": v2,
                "remark": remark
            }
        }
        return self.send_sync(data)

    def add_friend_by_card(self, wxid: str, ticket: str, remark: str):
        """添加好友分享的名片"""
        data = {
            "type": 11062,
            "data": {
                "remark": remark,
                "source_type": 17,
                "wxid": wxid,
                "ticket": ticket
            }
        }
        return self.send_sync(data)

    def add_friend_by_room(self, room_wxid: str, wxid: str, remark: str):
        """添加群成员为好友"""
        data = {
            "type": 11062,
            "data": {
                "remark": remark,
                "source_type": 14,
                "wxid": wxid,
                "room_wxid": room_wxid
            }
        }
        return self.send_sync(data)

    def check_friend_status(self, wxid: str):
        """检查好友状态"""
        data = {
            "type": 11080,
            "data": {
                "wxid": wxid
            }
        }
        return self.send_sync(data)

    def get_room_by_protocol(self, wxid: str):
        """获取群信息（协议）"""
        data = {
            "type": 11174,
            "data": {
                "wxid": wxid
            }
        }
        return self.send_sync(data)

    def get_invitation_relationship(self, room_wxid: str):
        """获取群成员邀请关系"""
        data = {
            "type": 11134,
            "data": {
                "room_wxid": room_wxid
            }
        }
        return self.send_sync(data)

    def create_room(self, member_list: typing.List[str]):
        """创建群聊"""
        data = {
            "type": 11068,
            "data": member_list
        }
        return self.send(data)

    def create_room_by_protocol(self, member_list: typing.List[str]):
        """创建群聊（协议）"""
        data = {
            "type": 11246,
            "data": member_list
        }
        return self.send_sync(data)

    def add_room_member(self, room_wxid: str, member_list: typing.List[str]):
        """添加群成员"""
        data = {
            "type": 11069,
            "data": {
                "room_wxid": room_wxid,
                "member_list": member_list
            }
        }
        return self.send_sync(data)

    def invite_room_member(self, room_wxid: str, member_list: typing.List[str]):
        """邀请群成员"""
        data = {
            "type": 11070,
            "data": {
                "room_wxid": room_wxid,
                "member_list": member_list
            }
        }
        return self.send_sync(data)

    def remove_room_member(self, room_wxid: str, wxid: str):
        """移出群成员"""
        data = {
            "type": 11071,
            "data": {
                "room_wxid": room_wxid,
                "name": wxid
            }
        }
        return self.send_sync(data)

    def modify_room_name(self, room_wxid: str, name: str):
        """修改群名称"""
        data = {
            "type": 11072,
            "data": {
                "room_wxid": room_wxid,
                "name": name
            }
        }
        return self.send_sync(data)

    def modify_room_notice(self, room_wxid: str, notice: str):
        """修改群公告"""
        data = {
            "type": 11073,
            "data": {
                "room_wxid": room_wxid,
                "notice": notice
            }
        }
        return self.send_sync(data)

    def modify_room_member_nickname(self, room_wxid: str, nickname: str):
        """修改我在本群的昵称"""
        data = {
            "type": 11074,
            "data": {
                "room_wxid": room_wxid,
                "nickname": nickname
            }
        }
        return self.send_sync(data)

    def display_room_member_nickname(self, room_wxid: str, status: int = 1):
        """是否显示群成员昵称"""
        data = {
            "type": 11075,
            "data": {
                "room_wxid": room_wxid,
                "status": status
            }
        }
        return self.send_sync(data)

    def edit_address_book(self, room_wxid: str, status: int = 1):
        """保存/移出通讯录"""
        data = {
            "type": 11076,
            "data": {
                "room_wxid": room_wxid,
                "status": status
            }
        }
        return self.send_sync(data)

    def exit_room(self, room_wxid: str):
        """退出群聊"""
        data = {
            "type": 11077,
            "data": {
                "room_wxid": room_wxid
            }
        }
        return self.send_sync(data)

    def get_corporate_contacts(self):
        """获取企业联系人"""
        data = {
            "type": 11132,
            "data": {}
        }
        return self.send_sync(data)

    def get_corporate_rooms(self):
        """获取企业群"""
        data = {
            "type": 11129,
            "data": {}
        }
        return self.send_sync(data)

    def get_corporate_room_members(self, room_wxid):
        """获取企业微信群成员"""
        data = {
            "type": 11130,
            "data": {
                "room_wxid": room_wxid
            }
        }
        return self.send_sync(data)

    def cdn_init(self):
        """初始化CDN"""
        data = {
            "type": 11228,
            "data": {}
        }
        return self.send_sync(data)

    def cdn_upload(self, file_path):
        """CDN上传"""
        data = {
            "type": 11229,
            "data": {
                "file_type": 2,
                "file_path": file_path
            }
        }
        return self.send_sync(data)

    def cdn_download(self, file_id: str, aes_key: str, save_path: str, file_type: int = 2):
        """CDN下载"""
        data = {
            "type": 11230,
            "data": {
                "file_id": file_id,
                "file_type": file_type,
                "aes_key": aes_key,
                "save_path": save_path
            }
        }
        return self.send_sync(data)

    def cdn_download2(self, url: str, auth_key: str, aes_key: str, save_path: str):
        """企业微信CDN下载"""
        data = {
            "type": 11253,
            "data": {
                "url": url,
                "auth_key": auth_key,
                "aes_key": aes_key,
                "save_path": save_path
            }
        }
        return self.send_sync(data)

    def send_text_by_cdn(self, to_wxid, content):
        """发送文本消息（CDN）"""
        data = {
            "type": 11237,
            "data": {
                "to_wxid": to_wxid,
                "content": content
            }
        }
        return self.send_sync(data)

    def send_room_at_by_cdn(self, to_wxid, content, at_list=None, at_all=0):
        """发送群at消息（CDN）"""
        if at_all == 0:
            if not isinstance(at_list, list):
                raise TypeError("at_list must be a list.")

            data = {
                "type": 11240,
                "data": {
                    "to_wxid": to_wxid,
                    "content": content,  # {$@}
                    "at_list": at_list
                }
            }
        else:
            data = {
                "type": 11240,
                "data": {
                    "to_wxid": to_wxid,
                    "content": content,  # {$@}
                    "at_all": 1
                }
            }
        return self.send_sync(data)

    def send_image_by_cdn(self, to_wxid: str, file_id: str, file_md5: str, file_size: int, thumb_file_size: int,
                          crc32: int, aes_key: str):
        """发送图片消息（CDN）"""
        data = {
            "type": 11231,
            "data": {
                "aes_key": aes_key,
                "file_id": file_id,
                "file_md5": file_md5,
                "file_size": file_size,
                "thumb_file_size": thumb_file_size,
                "crc32": crc32,
                "to_wxid": to_wxid
            }
        }
        return self.send_sync(data)

    def send_video_by_cdn(self, to_wxid: str, file_id: str, file_md5: str, file_size: int, thumb_file_size: int,
                          aes_key: str):
        """发送视频消息（CDN）"""
        data = {
            "type": 11233,
            "data": {
                "aes_key": aes_key,
                "file_id": file_id,
                "file_md5": file_md5,
                "file_size": file_size,
                "thumb_file_size": thumb_file_size,
                "to_wxid": to_wxid
            }
        }
        return self.send_sync(data)

    def send_file_by_cdn(self, to_wxid: str, file_id: str, file_md5: str, file_size: int, file_name: str,
                         aes_key: str):
        """发送文件消息（CDN）"""
        data = {
            "type": 11235,
            "data": {
                "aes_key": aes_key,
                "file_id": file_id,
                "file_md5": file_md5,
                "file_name": file_name,
                "file_size": file_size,
                "to_wxid": to_wxid
            }
        }
        return self.send_sync(data)

    def send_link_card_by_cdn(self, to_wxid: str, title: str, desc: str, url: str, image_url: str):
        """发送链接卡片消息（CDN）"""
        data = {
            "type": 11236,
            "data": {
                "to_wxid": to_wxid,
                "title": title,
                "desc": desc,
                "url": url,
                "image_url": image_url
            }
        }
        return self.send_sync(data)

    def send_emotion_by_cdn(self, aes_key: str, file_id: str, file_md5: str, file_size: int, to_wxid: str):
        """发送表情消息（CDN）"""
        data = {
            "type": 11241,
            "data": {
                "aes_key": aes_key,
                "file_id": file_id,
                "file_md5": file_md5,
                "file_size": file_size,
                "to_wxid": to_wxid
            }
        }
        return self.send_sync(data)

    def send_emotion2_by_cdn(self, to_wxid: str, path: str):
        """发送表情消息2（CDN）"""
        data = {
            "type": 11254,
            "data": {
                "to_wxid": to_wxid,
                "path": path
            }
        }
        return self.send_sync(data)

    def send_mini_program_by_cdn(self, to_wxid: str, username: str, appid: str, appname: str, appicon: str, title: str,
                                 page_path: str, aes_key: str, file_id: str, file_md5: str, file_size: int):
        """发送小程序消息（CDN）"""
        data = {
            "type": 11242,
            "data": {
                "to_wxid": to_wxid,
                "username": username,
                "appid": appid,
                "appname": appname,
                "appicon": appicon,
                "title": title,
                "page_path": page_path,
                "file_id": file_id,
                "aes_key": aes_key,
                "file_md5": file_md5,
                "file_size": file_size
            }
        }
        return self.send_sync(data)

    def send_video_card_by_cdn(self, to_wxid: str, object_id: str, object_nonce_id: str, nickname: str, username: str,
                               avatar: str, desc: str, thumb_url: str, url: str):
        """发送视频号消息（CDN）"""
        data = {
            "type": 11243,
            "data": {
                "to_wxid": to_wxid,
                "object_id": object_id,
                "object_nonce_id": object_nonce_id,
                "nickname": nickname,
                "username": username,
                "avatar": avatar,
                "desc": desc,
                "thumb_url": thumb_url,
                "url": url
            }
        }
        return self.send_sync(data)

    def send_card_by_cdn(self, to_wxid: str, username: str, nickname: str, avatar: str):
        """发送名片消息（CDN）"""
        data = {
            "type": 11239,
            "data": {
                "to_wxid": to_wxid,
                "username": username,
                "nickname": nickname,
                "avatar": avatar
            }
        }
        return self.send_sync(data)

    def send_location_by_cdn(self, to_wxid: str, address: str, latitude: float, longitude: float, title: str):
        """发送位置消息（CDN）"""
        data = {
            "type": 11238,
            "data": {
                "to_wxid": to_wxid,
                "address": address,
                "latitude": latitude,
                "longitude": longitude,
                "title": title
            }
        }
        return self.send_sync(data)

    def revoke_msg_by_cdn(self, to_wxid: str, new_msg_id: str, client_msg_id: int, create_time: int):
        """撤回消息（CDN）"""
        data = {
            "type": 11244,
            "data": {
                "to_wxid": to_wxid,
                "client_msgid": client_msg_id,
                "create_time": create_time,
                "new_msgid": new_msg_id
            }
        }
        return self.send_sync(data)

    def send_xml_by_cdn(self, to_wxid: str, content: str):
        """发送xml消息（CDN）"""
        data = {
            "type": 11214,
            "data": {
                "to_wxid": to_wxid,
                "content": content
            }
        }
        return self.send_sync(data)

    def get_collections(self):
        """获取收藏列表"""
        data = {
            "type": 11109,
            "data": {}
        }
        return self.send_sync(data)

    def send_collection(self, to_wxid: str, local_id: int):
        """发送收藏消息"""
        data = {
            "type": 11110,
            "data": {
                "to_wxid": to_wxid,
                "local_id": local_id
            }
        }
        return self.send(data)

    def collect(self, msg_id: str):
        """收藏消息"""
        data = {
            "type": 11111,
            "data": {
                "msgid": msg_id
            }
        }
        return self.send(data)

    def get_tags(self):
        """获取标签列表"""
        data = {
            "type": 11142,
            "data": {}
        }
        return self.send_sync(data)

    def confirm_receipt(self, transfer_id: str):
        """确认收款"""
        data = {
            "type": 11066,
            "data": {
                "transferid": transfer_id
            }
        }
        return self.send(data)

    def add_tag(self, label_name: str):
        """添加标签"""
        data = {
            "type": 11137,
            "data": {
                "label_name": label_name
            }
        }
        return self.send_sync(data)

    def delete_tag(self, label_id: int):
        """删除标签"""
        data = {
            "type": 11138,
            "data": {
                "label_id": label_id
            }
        }
        return self.send_sync(data)

    def modify_tag(self, label_id: int, label_name: str):
        """修改标签"""
        data = {
            "type": 11139,
            "data": {
                "label_id": label_id,
                "label_name": label_name
            }
        }
        return self.send(data)

    def add_tags_to_contact(self, wxid: str, label_id_list: str):
        """批量给用户加标签"""
        data = {
            "type": 11140,
            "data": {
                "wxid": wxid,
                "labelid_list": label_id_list
            }
        }
        return self.send_sync(data)

    def get_contact_tags(self, wxid):
        """获取联系人所有标签"""
        data = {
            "type": 11141,
            "data": {
                "wxid": wxid
            }
        }
        return self.send_sync(data)

    def voice_to_text(self, msg_id: str):
        """语音消息转文本"""
        data = {
            "type": 11112,
            "data": {
                "msgid": msg_id
            }
        }
        return self.send_sync(data)

    def open_chat(self, to_wxid: str):
        """切换当前会话"""
        data = {
            "type": 11090,
            "data": {
                "to_wxid": to_wxid
            }
        }
        return self.send(data)

    def clear_chat_history(self):
        """清除聊天记录"""
        data = {
            "type": 11108,
            "data": {}
        }
        return self.send(data)

    def set_disturb(self, wxid: str, status: int):
        """开启/关闭消息免打扰"""
        data = {
            "type": 11078,
            "data": {
                "wxid": wxid,
                "status": status
            }
        }
        return self.send_sync(data)

    def pin_chat(self, wxid: str, status: int):
        """置顶/取消置顶聊天"""
        data = {
            "type": 11079,
            "data": {
                "wxid": wxid,
                "status": status
            }
        }
        return self.send(data)

    def get_mini_program_code(self, appid: str):
        """获取小程序授权code"""
        data = {
            "type": 11136,
            "data": {
                "appid": appid
            }
        }
        return self.send_sync(data)

    def get_moments(self, max_id: str = "0"):
        """获取朋友圈"""
        data = {
            "type": 11145,
            "data": {
                "max_id": max_id
            }
        }
        return self.send_sync(data)

    def get_friend_moments(self, username, first_page_md5="", max_id: str = "0"):
        """获取好友朋友圈"""
        data = {
            "type": 11150,
            "data": {
                "username": username,
                "first_page_md5": first_page_md5,
                "max_id": max_id
            }
        }
        return self.send_sync(data)

    def comment_moment(self, object_id: str, content: str):
        """评论"""
        data = {
            "data": {
                "object_id": object_id,
                "content": content
            },
            "type": 11146
        }
        return self.send_sync(data)

    def like_moment(self, object_id: str):
        """点赞"""
        data = {
            "data": {
                "object_id": object_id
            },
            "type": 11147
        }
        return self.send_sync(data)

    def post_moment(self, object_desc: str):
        """发朋友圈"""
        data = {
            "type": 11148,
            "data": {
                "object_desc": object_desc
            }
        }
        return self.send_sync(data)

    def upload_image(self, image_path: str):
        """上传图片"""
        data = {
            "type": 11149,
            "data": {
                "path": image_path
            }
        }
        return self.send_sync(data)

    def init_video_account(self):
        """视频号初始化"""
        data = {
            "type": 11160,
            "data": {}
        }
        return self.send_sync(data)

    def search_video_account(self, query: str, scene: int, last_buff: str = ""):
        """视频号搜索"""
        data = {
            "type": 11161,
            "data": {
                "query": query,
                "last_buff": last_buff,
                "scene": scene
            }
        }
        return self.send_sync(data)

    def get_video_account_user_page(self, username: str, last_buff: str = ""):
        """视频号用户主页"""
        data = {
            "type": 11170,
            "data": {
                "username": username,
                "last_buff": last_buff
            }
        }
        return self.send_sync(data)

    def view_video_details(self, object_id: str, object_nonce_id: str, last_buff: str = ""):
        """查看视频详细信息(包含评论)"""
        data = {
            "type": 11169,
            "data": {
                "object_id": object_id,
                "object_nonce_id": object_nonce_id,
                "last_buff": last_buff
            }
        }
        return self.send_sync(data)

    def follow_video_blogger(self, username: str):
        """关注博主"""
        data = {
            "type": 11167,
            "data": {
                "username": username
            }
        }
        return self.send_sync(data)

    def like_video(self, object_id: str, object_nonce_id: str):
        """视频号点赞"""
        data = {
            "type": 11168,
            "data": {
                "object_id": object_id,
                "object_nonce_id": object_nonce_id
            }
        }
        return self.send_sync(data)

    def get_message_session_id(self, to_username: str, role_type: int):
        """获取私信sessionId"""
        data = {
            "type": 11202,
            "data": {
                "to_username": to_username,
                "roleType": role_type
            }
        }
        return self.send_sync(data)

    def send_private_message(self, to_username: str, session_id: str, content: str):
        """发送私信"""
        data = {
            "type": 11203,
            "data": {
                "to_username": to_username,
                "session_id": session_id,
                "content": content
            }
        }
        return self.send_sync(data)

    def create_virtual_nickname(self, nickname: str, head_img_url: str):
        """创建虚拟昵称"""
        data = {
            "type": 11194,
            "data": {
                "nickname": nickname,
                "headimg_url": head_img_url
            }
        }
        return self.send(data)

    def switch_virtual_nickname(self, role_type: int):
        """切换虚拟昵称"""
        data = {
            "type": 11195,
            "data": {
                "role_type": role_type
            }
        }
        return self.send(data)

    def delete_virtual_nickname(self):
        """删除虚拟昵称"""
        data = {
            "type": 11197,
            "data": {}
        }
        return self.send(data)

    def enter_live_room(self, object_id: str, live_id: str, object_nonce_id: str):
        """进入直播间"""
        data = {
            "type": 11162,
            "data": {
                "object_id": object_id,
                "live_id": live_id,
                "object_nonce_id": object_nonce_id
            }
        }
        return self.send_sync(data)

    def get_live_room_online_users(self, object_id: str, live_id: str, object_nonce_id: str):
        """获取直播间在线人员"""
        data = {
            "type": 11172,
            "data": {
                "object_id": object_id,
                "live_id": live_id,
                "object_nonce_id": object_nonce_id,
                "last_buff": ""
            }
        }
        return self.send_sync(data)

    def get_live_room_updates(self):
        """获取直播间变动信息(人气，实时发言等)"""
        data = {
            "type": 11163,
            "data": {}
        }
        return self.send_sync(data)

    def speak_in_live_room(self, content: str):
        """直播间发言"""
        data = {
            "type": 11164,
            "data": {
                "content": content
            }
        }
        return self.send_sync(data)

    def like_in_live_room(self, count):
        """直播间点赞"""
        data = {
            "type": 11185,
            "data": {
                "count": count
            }
        }
        return self.send_sync(data)

    def get_live_room_shelves(self, live_username: str, request_id: str):
        """获取直播间货架"""
        data = {
            "type": 11186,
            "data": {
                "live_username": live_username,
                "request_id": request_id
            }
        }
        return self.send_sync(data)

    def get_shelf_product_details(self, appid: str, request_id: str, product_id: str, real_appid: str,
                                  live_username: str):
        """获取货架商品详细信息"""
        data = {
            "type": 11187,
            "data": {
                "appid": appid,
                "request_id": request_id,
                "product_id": product_id,
                "live_username": live_username,
                "real_appid": real_appid
            }
        }
        return self.send_sync(data)

    def get_a8key(self, url: str, scene: int):
        """A8Key接口"""
        data = {
            "type": 11135,
            "data": {
                "url": url,
                "scene": scene
            }
        }
        return self.send_sync(data)

    def set_auto_accept_friend(self, auto: int):
        """自动同意好友申请"""
        data = {
            "type": 10081,
            "data": {
                "auto": auto
            }
        }
        return self.send(data)

    def set_auto_accept_wcpay(self, auto: int):
        """自动同意好友转账"""
        data = {
            "type": 10082,
            "data": {
                "auto": auto
            }
        }
        return self.send(data)

    def set_auto_accept_room(self, auto: int):
        """自动同意加群邀请"""
        data = {
            "type": 10083,
            "data": {
                "auto": auto
            }
        }
        return self.send(data)

    def set_auto_accept_card(self, auto: int):
        """自动加名片"""
        data = {
            "type": 10084,
            "data": {
                "auto": auto
            }
        }
        return self.send(data)

    def decode_image(self, src_file: str, dest_file: str):
        """解密图片"""
        data = {
            "type": 10085,
            "data": {
                "src_file": src_file,
                "dest_file": dest_file
            }
        }
        return self.send(data)

    def exec_sql(self, sql: str, db: int):
        """执行SQL命令"""
        data = {
            "type": 11027,
            "data": {
                "sql": sql,
                "db": db
            }
        }
        return self.send_sync(data)

    def run(self):
        try:
            logger.info(f"Listen Server at {self.server_host}:{self.server_port}")
            server = socketserver.ThreadingTCPServer((self.server_host, self.server_port), RequestHandler)
            server.wechat = self
            server.serve_forever()
        except (KeyboardInterrupt, SystemExit):
            self.client.terminate()
            self.wechat.terminate()
