# --coding: utf-8 --
from ctypes import *
import json
import atexit
import threading
import os
import inspect
import datetime
import time as t
import signal
import random

# cuts about .1 second on import or 30%
# from pymysql import connect as sql_connect
import base64

pskfunc = CDLL("libPSKFUNC.so")
# OXSCRIPT版本号信息
version = "V2.0.11"

pyfilepath = ''
start_time = 0
end_time = 0
def count_time(type = 0):
    global start_time
    global end_time
    if(type == 0):
        start_time = t.time()
    elif type == 1:
        end_time = t.time()
    else:
        return end_time - start_time
errorList = {
    "0": "no error!",
    "-3000": "port is disconnect!",
    "-3001": "send API version failed!",
    "-3002": "malloc failed!",
    "-3003": "port init failed!",
    "-3004": "receive data from printer failed!",
    "-3005": "receive data from lcd failed!",
    "-3006": "get port data send failed!",
    "-3007": "get port data failed!",
    "-3008": "set printer mode failed",
    "-3009": "set printer mode parameter error!",
    "-3010": "set printer direction failed!",
    "-3011": "set printer direction parameter error!",
    "-3012": "set cut page nums failed!",
    "-3013": "reset printer failed!",
    "-3014": "printer selfcheck page failed!",
    "-3015": "callback failed!",
    "-3016": "set print darkness failed!",
    "-3017": "set label height failed!",
    "-3018": "set label width failed!",
    "-3019": "set coordinate origin failed!",
    "-3020": "set print speed failed!",
    "-3021": "set print speed parameter failed!",
    "-3022": "text length parameter failed!",
    "-3023": "text direction parameter failed!",
    "-3024": "text font parameter failed!",
    "-3025": "text horizontal_multiplier parameter failed!",
    "-3026": "text style parameter failed!",
    "-3027": "print text failed!",
    "-3028": "print DATAMATRIX barcode failed!",
    "-3029": "print QR barcode failed!",
    "-3030": "print MaxiCode barcode failed!",
    "-3031": "print pdf417 barcode failed!",
    "-3032": "pdf417 parameter error!",
    "-3033": "print hanxin barcode failed!",
    "-3034": "print One-dimensional bar code failed!",
    "-3035": "One-dimensional bar code parameter error!",
    "-3036": "print graph failed!",
    "-3037": "the name of graph parameter error!",
    "-3038": "draw line failed!",
    "-3039": "draw white line failed!",
    "-3040": "draw rectangle failed!",
    "-3041": "print failed!",
    "-3042": "print num parameter error",
    "-3043": "feed page failed!",
    "-3044": "check page failed!",
    "-3045": "send data to lcd failed!",
    "-3046": "RFID failed!",
    "-3047": "RFID failed!",
    "-3048": "RFID failed!",
    "-3049": "RFID failed!",
    "-3050": "RFID write data mode input error!",
    "-3051": "RFID write input len para error!",
    "-3052": "download font name is null!",
}

with open("/mnt/user/logs/script.log", encoding="utf-8", mode="w") as logfile:
    logfile.write(str(datetime.datetime.now()))
    logfile.write("\n\n")


def debuglog(info):
    with open("/mnt/user/logs/script.log", encoding="utf-8", mode="a") as log:
        log.write('[' + str(datetime.datetime.now()) + ']' + str(info))
        log.write("\n\n")


# 用户连接数据库，执行sql语句包装函数


# def PTK_ExecuteSqlCmd(myhost, myuser, mypassword, mydatabase, cmd):
#     cnx = sql_connect(host=myhost, user=myuser,
#                           password=mypassword, database=mydatabase, charset='utf8')
#     cursor = cnx.cursor()
#     cursor.execute(cmd)
#     ret = cursor.fetchall()
#     cnx.commit()
#     cnx.close()
#     return ret

# 获取本函数库版本信息


def PTK_getVersion():
    # PTK_GetInfo = pskfunc.PTK_GetInfo  # 得到API函数库的版本信息
    # print('POSTEK pskfunc version ' + version)
    return version


def PTK_SetUnit(a):  # 设置输入单位，默认为0
    global unit
    if a == 1:
        unit = 1
    else:
        unit = 0


unit = 0
MM = 0
DOTS = 1


# 单位转换函数
def mmOrDots(a):  # 默认单位为mm
    global unit
    b = a
    if unit == 0:
        allinfo = PTK_GetPrinterInfo()
        # f = open("/mnt/user/config/settings/printerIdentify.json", "r")
        # rowdata = json.load(f)
        if allinfo["dpi"] == '203':
            b = int(a * 8)
        elif allinfo["dpi"] == '300':
            b = int(a * 11.8)
        elif allinfo["dpi"] == '600':
            b = int(a * 23.62)
        # f.close()
    else:
        b = int(a)
    return b

def getFilePath():
    calling_frame = inspect.stack()[-1]
    calling_file = calling_frame.filename
    return calling_file

def OpenPort():
    global pyfilepath
    pskfunc.OpenPort()
    # 创建标志文件代表端口开启
    if os.path.exists("/mnt/user/OXScript/sys") == False:
        os.mkdir("/mnt/user/OXScript/sys")
    if os.path.exists("/mnt/user/OXScript/sys/oxscriptPortOpen"):
        os.remove("/mnt/user/OXScript/sys/oxscriptPortOpen")
    os.system("touch /mnt/user/OXScript/sys/oxscriptPortOpen")

    pyfilepath = getFilePath()
    debuglog(pyfilepath)


# 关闭端口请见文件最下方（UI定义后方）


OpenPort()  # 自动打开端口
print("POSTEK OX Script Library Version " + PTK_getVersion())
GetErrState = pskfunc.GetErrState  # 获取最新errorcode
Check_State = pskfunc.Check_State  # 打印机连接状态


def PTK_GetErrorInfo():
    return errorList[str(GetErrState())]


# ===========================================================#
# 打开端口相关
# ===========================================================#
"""
typedef enum{
    PORT_UNDEF       = -1,
    PORT_SERIAL      = 0,//串口的数据环形缓冲区序号
    PORT_USBDEVICE   = 1,//USB DEVICE的数据环形缓冲区序号
    PORT_ETHERNET    = 2,//以太网口的数据环形缓冲区序号
    PORT_BLUETOOTH   = 3,//蓝牙的数据环形缓冲区序号
    PORT_WIFI        = 4,//WIFI的数据环形缓冲区序号
    PORT_PARALLEL    = 5,//并口的数据环形缓冲区序号
    PORT_WEBSOCK    = 6,//websocket的数据环形缓冲区序号
}PORT_Type_E;
"""

PORT_SERIAL = 0
PORT_USBDEVICE = 1
PORT_ETHERNET = 2
PORT_BLUETOOTH = 3
PORT_WIFI = 4
PORT_PARALLEL = 5
PORT_WEBSOCK = 6
PORT_USBHOST = 11
PORT_SCRIPT  = 12


def PTK_GetPortData(port, dataLen=1024, timeout=5000):
    isSkipLineEnd = False
    dataBuff = create_string_buffer(dataLen)
    lens = c_int(dataLen)
    if port < 0 or port > 12:
        return "input port error"
    if type(dataBuff) == str:
        bytes(dataBuff, "utf-8")
    if (
        pskfunc.PTK_GetPortData(
            dataBuff, byref(lens), c_bool(isSkipLineEnd), port, timeout
        )
        != 0
    ):
        return -1
    return bytes.decode(dataBuff.raw[0: lens.value])


def _is_utf8_encoded(string):
    try:
        string.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False
    except AttributeError:
        return False


def PTK_SendCmdToPrinter(cmd):
    if _is_utf8_encoded(cmd) or type(cmd) == bytes:
        cmd = bytes(cmd)
    else:
        if cmd.endswith("\r\n") == False:
            cmd = cmd + "\r\n"
        cmd = cmd.encode("utf-8")
    cc = create_string_buffer(cmd)
    len = sizeof(cc)
    if pskfunc.PTK_SendFormToPrinter(cc, len) != 0:
        return errorList[str(GetErrState())]
    return True


def PTK_WriteToSerial(dataBuff):
    dataSize = len(dataBuff)
    if type(dataBuff) == bytes:
        cmd = b"#DATA>SET" + str(dataSize).encode('utf-8') + \
        b";" + dataBuff
    elif type(dataBuff) == str:
        cmd = b"#DATA>SET" + str(dataSize).encode('utf-8') + \
        b";" + dataBuff.encode('utf-8')
    PTK_SendCmdToPrinter(cmd)


# ===========================================================#
# 获取打印机信息
# ===========================================================#

PTK_FeedBack = pskfunc.PTK_FeedBack  # 要求打印机立刻反馈错误报告

def PTK_GetCurrentStatus():
    PTK_SendCmdToPrinter(b"#OXScript;check;0;#End")
    dataBuff = create_string_buffer(1024)
    if(pskfunc.PTK_GetMainData(dataBuff) != 0):
        return -1
    cmd = dataBuff.raw[0:dataBuff.raw.index(b'\n')]
    info = cmd.split(b';')
    if len(info) < 12:
        return -2
    status = info[12]
    if status == b'\x00':
        return 'ready'
    elif status == b'\x08':
        return 'connecting'
    elif status == b'\x04':
        return 'printing'
    elif status == b'\x05':
        return 'deleting'
    elif status == b'\x06':
        return 'upgrading'
    elif status == b'\x07':
        return 'sleeping'
    elif status == b'\x57':
        return 'headopen'
    elif status == b'\x58':
        return 'pause'
    elif status == b'\xD5':
        return 'ribbonout'
    else:
        return 'get fail'

#OXScript;response;0;TX3wzh;TX3;300;TX3wzh.local.;2.0.5;ce:16:84:fa:29:32;1;0;0;#End
def PTK_GetPrinterInfo():
    allinfo = {"printerName": "",   #打印机名
               "printerType": "",   #打印机型号
               "dpi": "",           #dpi
               "domainName": "",    #打印机域名
               "printerMac": "",    #打印机mac地址
               "ethStatus": "",     #网口状态
               "usbStatus": "",     #usb状态
               "wifiStatus": "",     #WIFI状态
               "bleStatus": "",     #蓝牙状态
               "deviceSn": "",      #设备识别号
               }

    #查询网口状态
    pt = os.popen("ethtool eth0 | grep 'Link detected: no'")
    out = pt.readlines()
    if out:
        allinfo["ethStatus"] = False
    else:
        allinfo["ethStatus"] = True

    #获取所有信息
    cmd = b'#OXScript;check;0;#End\n'
    PTK_SendCmdToPrinter(cmd)
    ret = PTK_GetPortData(port = PORT_SCRIPT)
    retlist = ret.split(';')
    allinfo["printerName"] = retlist[3]
    allinfo["printerType"] = retlist[4]
    allinfo["dpi"] = retlist[5]
    allinfo["domainName"] = retlist[6]
    allinfo["printerMac"] = retlist[8]
    allinfo["usbStatus"] = (retlist[9] == '1')
    allinfo["wifiStatus"] = (retlist[10] == '1')
    allinfo["bleStatus"] = (retlist[11] == '1')
    allinfo["deviceSn"] = retlist[13]
    return allinfo

#读取通用IO的电平参数
def PTK_GetExternIOLevel(pinindex):
    if pinindex > 15 or pinindex < 0:
        debuglog('io read input para should be between 0 and 15')
        return -1
    cmd = b'#OXScript;readexternio;0;' + str(pinindex).encode('utf-8') + b';#End\n'
    PTK_SendCmdToPrinter(cmd)
    ret = PTK_GetPortData(port = PORT_SCRIPT)
    retlist = ret.split(';')
    if retlist[3] == '2':
        debuglog('io read timeout')
    return retlist[3]

# ===========================================================#
# 打印机设置
# ===========================================================#

BOTTOM_RIGHT = "T"
TOP_LEFT = "B"


def PTK_SetPrintDirection(direction: str) -> int:
    if pskfunc.PTK_SetDirection(c_char(direction.encode("utf-8"))) != 0:
        return errorList[str(GetErrState())]
    return True


def PTK_CutPage(number_of_labels=1, save_in_flash=False) -> int:
    if save_in_flash:
        if pskfunc.PTK_CutPageEx(c_uint(number_of_labels)) != 0:
            return errorList[str(GetErrState())]
    else:
        if pskfunc.PTK_CutPage(c_uint(number_of_labels)) != 0:
            return errorList[str(GetErrState())]
    return True


# def PTK_Reset() -> int:
#     if pskfunc.PTK_Reset() != 0:
#         return errorList[str(GetErrState())]
#     return True

class PTK_ExternalStorageDevice:
    def __init__(self, path):
        self.path = path
        pt = os.popen("ls -l /dev/disk/by-label/")
        namelist =pt.readlines()
        for name in namelist[1:]:
            if name.split(' ')[-1].split('/')[-1][0:-1] == path.split("/")[-1]:
                self.name = name.split(' ')[-3]
    
    def __str__(self): 
        return self.name

    def list_all_files(self):
        fileList = []
        for path , dir, files in os.walk(os.path.join(self.path)):
            if files != [] and path == self.path:
                for ff in files:
                    fileList.append(ff)
            elif files != []:
                for ff in files:
                    fileList.append(path[10+len(self.path.split('/')[2]):] + "/" + ff)
        return fileList

    def read_file(self, filename):
        if not os.path.exists(self.path + "/" + filename):
            print('File does not exist!')
            return 'File does not exist!'
        return open(self.path + "/" + filename, "rb")

    def write_file(self, filename, mode = 'w'):
        return open(self.path + "/" + filename, mode)
'''
函数名:PTK_GetExternalStorageDeviceList

返回值:PTK_ExternalStorageDevice类的实例化的列表

用法:

1.列出所有文件路径, 返回值为包含所有U盘路径的列表:PTK_GetExternalStorageDeviceList()[0].list_all_files()

2.读文件,输入文件路径,返回文件读取操作符:PTK_GetExternalStorageDeviceList()[0].read_file(filename = filename)

3.写文件,输入文件路径和操作文件模式,'w':重写模式,'a':追加模式,返回写入文件操作符:PTK_GetExternalStorageDeviceList()[0].write_file(filename = filename, mode='w')

4.文件操作类PTK_ExternalStorageDevice包含属性name为U盘的自定义名字,使用方法:PTK_GetExternalStorageDeviceList()[0].name
'''

def PTK_GetExternalStorageDeviceList():
    upanlist = []
    for path , dir, file in os.walk(os.path.join('/run/media')):
        if path == '/run/media':
            try:
                dir.remove('mmcblk2p1')
            except Exception as e:
                pass
            try:
                dir.remove('mmcblk2p2')
            except Exception as e:
                pass
            try:
                dir.remove('mmcblk2p3')
            except Exception as e:
                pass
            for name in dir:
                upanlist.append(PTK_ExternalStorageDevice(path + '/' + name))
            break
    return upanlist            

# ===========================================================#
# 标签设置
# ===========================================================#
def PTK_SetDarkness(darkness) -> int:
    if pskfunc.PTK_SetDarkness(c_uint(darkness)) != 0:
        return errorList[str(GetErrState())]
    return True


GAP_MODE = 0
SPECIAL_MODE = 1
BLACK_LINE_MODE = 2


def PTK_SetLabelHeight(height, mode=GAP_MODE, gapH=3) -> int:
    if mmOrDots(height) < 1 or mmOrDots(height) > 65535:
        debuglog("label height input error")
        return "label height input error"

    if mode == 0 and type(gapH) is int:
        gap = mmOrDots(gapH)
        if gap > 240 or gap < 0:
            debuglog("0 label gap height input error")
            return "label gap height input error"
    elif (mode == 1 or mode == 2) and type(gapH) is str:
        if gapH.find("+") != -1:
            nums = str.split("+")
            p1 = mmOrDots(nums[0])
            p2 = mmOrDots(nums[1])
            gap = str(p1) + "+" + str(p2)
        elif gapH.find("-") != -1:
            nums = str.split("-")
            p1 = mmOrDots(nums[0])
            p2 = mmOrDots(nums[1])
            gap = str(p1) + "-" + str(p2)
        if p1 > 240 or p1 < 0 or p2 > 240 or p2 < 0:
            debuglog("label gap height input error")
            return "label gap height input error"
        if mode == 2:
            gap = "B" + gap
    else:
        debuglog("label mode para or gapH para input error")
        return "label mode para or gapH para input error"

    if (
        pskfunc.PTK_SetLabelHeight(
            c_int(mmOrDots(height)), str(gap).encode("utf-8"))
        != 0
    ):
        return errorList[str(GetErrState())]
    return True


def PTK_SetLabelWidth(width: int) -> int:
    if pskfunc.PTK_SetLabelWidth(c_int(mmOrDots(width))) != 0:
        return errorList[str(GetErrState())]
    return True


def PTK_SetCoordinateOrigin(x=0, y=0):  # 设置标签坐标原点
    if pskfunc.PTK_SetCoordinateOrigin(x, y) != 0:
        return errorList[str(GetErrState())]
    return True


def PTK_SetPrintSpeed(speed) -> int:
    if speed < 0 or speed > 18:
        debuglog("speed para error")

    if pskfunc.PTK_SetPrintSpeed(str(speed).encode("utf-8")) != 0:
        return errorList[str(GetErrState())]
    return True


# ===========================================================#
# 打印文字
# ===========================================================#

NORMAL = "N"
REVERSE = "R"
SDRAM = 0
FLASH = 1

#直接使用PTK_DrawText，该函数可不开放
def PTK_CreatFont(location, fontname, downloadfontname):
    if location != 0 and location != 1:
        debuglog("PTK_CreatFont: Invalid value for location")
        return "PTK_CreatFont: Invalid value for location"
    if fontname < "A" and fontname > "Z":
        debuglog("PTK_CreatFont: Invalid value for fontname")
        return "PTK_CreatFont: Invalid value for fontname"

    if (
        pskfunc.PTK_CreatFont(
            location, c_char(fontname.encode("utf-8")
                             ), downloadfontname.encode("utf-8")
        )
        != 0
    ):
        return errorList[str(GetErrState())]
    return True


font_nums = 0
fontsList = {}


def PTK_DrawText(
    x_coordinate: float,
    y_coordinate: float,
    data: str,
    fonts="1",
    font_size=3,
    text_style="N",
    rotation=0,
) -> int:
    global font_nums
    global fontsList
    if len(fonts) == 1:
        if int(fonts) > 6:
            vertical = mmOrDots(font_size)
            hori = vertical
        else:
            hori = font_size
            vertical = font_size
    else:
        flag = 0
        for name in fontsList.keys():
            if name == fonts:
                font = fontsList["name"]
                flag = 1
        if flag == 0 and font_nums < 26:
            font = chr(font_nums + ord("A"))
            fontsList[fonts] = font
            font_nums += 1
        else:
            font = "A"
            fontsList[fonts] = font
            font_nums = 1
        PTK_CreatFont(1, font, fonts)
        fonts = font
        vertical = mmOrDots(font_size)
        hori = vertical

    if (
        pskfunc.PTK_DrawText(
            mmOrDots(x_coordinate),
            mmOrDots(y_coordinate),
            rotation,
            c_char(fonts.encode("utf-8")),
            hori,  # 宽度
            vertical,  # 高度
            c_char(text_style.encode("utf-8")),
            data.encode("utf-8"),
        )
        != 0
    ):
        return errorList[str(GetErrState())]
    return True


# ===========================================================#
# 打印二维码
# ===========================================================#


def PTK_DrawBar2D_DATAMATRIX(
    x_coordinate: float, y_coordinate: float, multiplier: int, data: str, rotation=0
) -> int:
    if multiplier < 1 or multiplier > 99:
        debuglog("PTK_DrawBar2D_DATAMATRIX: Invalid value for multiplier")
        return "PTK_DrawBar2D_DATAMATRIX: Invalid value for multiplier"
    if rotation != 0 and rotation != 1 and rotation != 2 and rotation != 3:
        debuglog("PTK_DrawBar2D_DATAMATRIX: Invalid value for rotation")
        return "PTK_DrawBar2D_DATAMATRIX: Invalid value for rotation"
    if (
        pskfunc.PTK_DrawBar2D_DATAMATRIX(
            mmOrDots(x_coordinate),
            mmOrDots(y_coordinate),
            0,
            0,
            rotation,
            multiplier,
            data.encode("utf-8"),
        )
        != 0
    ):
        return errorList[str(GetErrState())]
    return True


def PTK_DrawBar2D_QR(
    x_coordinate: float,
    y_coordinate: float,
    qr_version=0,
    rotation=0,
    multiplier=1,
    encode_mode=0,
    correction_level=0,
    masking=8,
    data="string",
):
    if multiplier < 1 or multiplier > 99:
        debuglog("PTK_DrawBar2D_QR: Invalid value for multiplier")
        return "PTK_DrawBar2D_QR: Invalid value for multiplier"
    if rotation != 0 and rotation != 1 and rotation != 2 and rotation != 3:
        debuglog("PTK_DrawBar2D_QR: Invalid value for rotation")
        return "PTK_DrawBar2D_QR: Invalid value for rotation"
    if (
        correction_level != 0
        and correction_level != 1
        and correction_level != 2
        and correction_level != 3
    ):
        debuglog("PTK_DrawBar2D_QR: Invalid value for correction_level")
        return "PTK_DrawBar2D_QR: Invalid value for correction_level"
    if qr_version < 0 or qr_version > 40:
        debuglog("PTK_DrawBar2D_QR: Invalid value for qr_version")
        return "PTK_DrawBar2D_QR: Invalid value for qr_version"

    if encode_mode < 0 or encode_mode > 4:
        debuglog("PTK_DrawBar2D_QR: Invalid value for encode_mode")
        return "PTK_DrawBar2D_QR: Invalid value for encode_mode"
    if (
        pskfunc.PTK_DrawBar2D_QR(
            mmOrDots(x_coordinate),
            mmOrDots(y_coordinate),
            0,
            qr_version,
            rotation,
            multiplier,
            encode_mode,
            correction_level,
            masking,
            data.encode("utf-8"),
        )
        != 0
    ):
        return errorList[str(GetErrState())]
    return True


UPS = 1
NOT_UPS = 0


def PTK_DrawBar2D_MaxiCode(
    x_coordinate: float, y_coordinate: float, is_ups_data: int, data: str, mode=4
) -> int:
    if mode < 2 or mode > 4:
        debuglog("PTK_DrawBar2D_MaxiCode: Invalid value for mode")
        return "PTK_DrawBar2D_MaxiCode: Invalid value for mode"
    if is_ups_data != 0 and is_ups_data != 1:
        debuglog("PTK_DrawBar2D_QR: Invalid value for is_ups_data")
        return "PTK_DrawBar2D_QR: Invalid value for is_ups_data"
    if (
        pskfunc.PTK_DrawBar2D_MaxiCode(
            mmOrDots(x_coordinate),
            mmOrDots(y_coordinate),
            mode,
            is_ups_data,
            data.encode("utf-8"),
        )
        != 0
    ):
        return errorList[str(GetErrState())]
    return True


def PTK_DrawBar2D_Pdf417(
    x_coordinate: float,
    y_coordinate: float,
    correction_level: int,
    px: int,
    py: int,
    encode_row: int,
    encode_column: int,
    t: int,
    data: str,
    rotation=0,
) -> int:
    if correction_level < 0 or correction_level > 8:
        debuglog("PTK_DrawBar2D_Pdf417: Invalid value for correction_level")
        return "PTK_DrawBar2D_Pdf417: Invalid value for correction_level"

    if px < 2 or px > 9:
        debuglog("PTK_DrawBar2D_Pdf417: Invalid value for px")
        return "PTK_DrawBar2D_Pdf417: Invalid value for px"

    if py < 4 or py > 99:
        debuglog("PTK_DrawBar2D_Pdf417: Invalid value for px")
        return "PTK_DrawBar2D_Pdf417: Invalid value for px"

    if encode_row < 3 or encode_row > 90:
        debuglog("PTK_DrawBar2D_Pdf417: Invalid value for maxrow")
        return "PTK_DrawBar2D_Pdf417: Invalid value for maxrow"

    if encode_column < 1 or encode_column > 30:
        debuglog("PTK_DrawBar2D_Pdf417: Invalid value for maxcolumn")
        return "PTK_DrawBar2D_Pdf417: Invalid value for maxcolumn"

    if t != 0 and t != 1:
        debuglog("PTK_DrawBar2D_Pdf417: Invalid value for t")
        return "PTK_DrawBar2D_Pdf417: Invalid value for t"

    if rotation != 0 and rotation != 1 and rotation != 2 and rotation != 3:
        debuglog("PTK_DrawBar2D_Pdf417: Invalid value for rotation")
        return "PTK_DrawBar2D_Pdf417: Invalid value for rotation"
    if (
        pskfunc.PTK_DrawBar2D_Pdf417(
            mmOrDots(x_coordinate),
            mmOrDots(y_coordinate),
            0,
            +0,
            correction_level,
            0,
            px,
            py,
            encode_row,
            encode_column,
            t,
            rotation,
            data.encode("utf-8"),
        )
        != 0
    ):
        return errorList[str(GetErrState())]
    return True


def PTK_DrawBar2D_HANXIN(
    x_coordinate: float,
    y_coordinate: float,
    multiplier: int,
    data: str,
    encoding=0,
    correction_level=0,
    masking=0,
    rotation=0,
) -> int:
    if multiplier < 0 or multiplier > 30:
        debuglog("PTK_DrawBar2D_HANXIN: Invalid value for multiplier")
        return "PTK_DrawBar2D_HANXIN: Invalid value for multiplier"
    if rotation != 0 and rotation != 1 and rotation != 2 and rotation != 3:
        debuglog("PTK_DrawBar2D_HANXIN: Invalid value for rotation")
        return "PTK_DrawBar2D_HANXIN: Invalid value for rotation"
    if correction_level < 0 or correction_level > 3:
        debuglog("PTK_DrawBar2D_HANXIN: Invalid value for correction_level")
        return "PTK_DrawBar2D_HANXIN: Invalid value for correction_level"
    if masking < 0 or masking > 3:
        debuglog("PTK_DrawBar2D_HANXIN: Invalid value for masking")
        return "PTK_DrawBar2D_HANXIN: Invalid value for masking"
    if encoding < 0 or encoding > 6:
        debuglog("PTK_DrawBar2D_HANXIN: Invalid value for encoding")
        return "PTK_DrawBar2D_HANXIN: Invalid value for encoding"
    if (
        pskfunc.PTK_DrawBar2D_HANXIN(
            mmOrDots(x_coordinate),
            mmOrDots(y_coordinate),
            0,
            0,
            encoding,
            multiplier,
            rotation,
            correction_level,
            masking,
            data.encode("utf-8"),
        )
        != 0
    ):
        return errorList[str(GetErrState())]
    return True


# ===========================================================#
# 打印一维条码
# ===========================================================#

NO_TEXT = "N"
TEXT = "B"


def PTK_DrawBarcode(
    x_coordinate: float,
    y_coordinate: float,
    barcode_type: str,
    wide_unit_width: float,
    barcode_height: float,
    data: str,
    human_readable=TEXT,
    narrow_unit_width=0.1,
    rotation=0,
) -> int:
    if rotation != 0 and rotation != 1 and rotation != 2 and rotation != 3:
        debuglog("PTK_DrawBarcode: Invalid value for rotation")
        return "PTK_DrawBarcode: Invalid value for rotation"
    if (
        pskfunc.PTK_DrawBarcode(
            mmOrDots(x_coordinate),
            mmOrDots(y_coordinate),
            rotation,
            barcode_type.encode("utf-8"),
            mmOrDots(narrow_unit_width),
            mmOrDots(wide_unit_width),
            mmOrDots(barcode_height),
            c_char(human_readable.encode("utf-8")),
            data.encode("utf-8"),
        )
        != 0
    ):
        return errorList[str(GetErrState())]
    return True


# ===========================================================#
# 打印图形
# ===========================================================#


def PTK_DrawGraphics(x, y, graphic_name):
    if pskfunc.PTK_DrawGraphics(x, y, graphic_name.encode("utf-8")) != 0:
        return errorList[str(GetErrState())]
    return True  # 写入标签：打印机里的指定pcx图形


def PTK_DrawGraphicsFromBytes(x, y, isbase64, graphic_data):
    if type(graphic_data) is bytes:
        if isbase64:
            graphic_data = base64.b64decode(graphic_data)
        size = len(graphic_data)
        rand = random.randint(100, 999)
        name = str(rand).encode()
        cmd = (
              b'\r\nGK"img' + name + b'"\r\n'
            + b'\r\nGM"img' + name + b'"'
            + str(size).encode()
            + b"\r\n"
            + graphic_data
            + b"\r\nGG"
            + str(mmOrDots(x)).encode()
            + b","
            + str(mmOrDots(y)).encode()
            + b',"img' + name + b'"' + b'\r\n'
        )
        PTK_SendCmdToPrinter(cmd)
    else:
        debuglog("输入图片数据格式错误，请输入二进制数据！")
        return False

    return True  # 写入标签：打印机里的指定pcx图形


# ===========================================================#
# 打印线条
# ===========================================================#


def PTK_DrawDiagonal(
    x_coordinate: float,
    y_coordinate: float,
    thickness: float,
    end_point_x: float,
    end_point_y: float,
) -> int:
    if (
        pskfunc.PTK_DrawDiagonal(
            mmOrDots(x_coordinate),
            mmOrDots(y_coordinate),
            mmOrDots(thickness),
            mmOrDots(end_point_x),
            mmOrDots(end_point_y),
        )
        != 0
    ):
        return errorList[str(GetErrState())]
    return True


def PTK_DrawRectangle(
    x_coordinate: float,
    y_coordinate: float,
    thickness: int,
    end_point_x: int,
    end_point_y: int,
) -> int:
    if (
        pskfunc.PTK_DrawRectangle(
            mmOrDots(x_coordinate),
            mmOrDots(y_coordinate),
            mmOrDots(thickness),
            mmOrDots(end_point_x),
            mmOrDots(end_point_y),
        )
        != 0
    ):
        return errorList[str(GetErrState())]
    return True


# ===========================================================#
# 开始打印标签
# ===========================================================#
PORT_SCRIPT = 3


def PTK_PrintLabel(number_of_label=1, number_of_copy=1, feedback_flag = 1, rifeedback_flag = 0, ribank = 0) -> int:
    global font_nums
    font_nums = 0
    if rifeedback_flag == 1:
        if pskfunc.PTK_SetRIDataback(10,ribank) != 0:
            return -1
    if feedback_flag == 1:
        if pskfunc.PTK_SetPortback(PORT_SCRIPT) != 0:
            return -1
    if pskfunc.PTK_PrintLabel(number_of_label, number_of_copy) != 0:
        return errorList[str(GetErrState())]
    return True


def PTK_PrintConfiguration() -> int:
    if pskfunc.PTK_PrintConfiguration() != 0:
        return errorList[str(GetErrState())]
    return True


def PTK_FeedMedia() -> int:
    if pskfunc.PTK_FeedMedia() != 0:
        return errorList[str(GetErrState())]
    return True


def PTK_MediaCalibration() -> int:
    if pskfunc.PTK_MediaDetect() != 0:
        return errorList[str(GetErrState())]
    return True


# ===========================================================#
# RFID打印标签
# ===========================================================#

#MR
def PTK_RFIDCalibrate():
    if pskfunc.PTK_RFIDCalibrate() == -1:
        return False
    return True

#新版本不需要
# def PTK_RWRFIDLabel(RWMode, WForm, StartBlock, WDataNum, WArea, data):
#     if (
#         pskfunc.PTK_RWRFIDLabel(
#             RWMode, WForm, StartBlock, WDataNum, WArea, data.encode("utf-8")
#         )
#         != 0
#     ):
#         return errorList[str(GetErrState())]
#     return True

'''
OperationMode: Specifies the action to be performed. 
0 - Unlock. Unlock the specified password or memory banks
1 - Lock. Lock the specified passwords or memory banks
2 - Permanently unlock. Permanently unlock the specified passwords or memory banks
3 - Permanently lock. Permanently lock the specified passwords or memory banks
4 - Set the kill password

OperationArea -> String: Specifies the selected passwords and/or memory banks to act. It is a 5-bit binary value.
Each bit represents a specific password or memory bank (Kill Password, Access Password, EPC, TID, USER). 
A value of 1 indicates selection, and 0 indicates unselection.

data -> String: Specifies a constant string for an Access Password or a Kill Password. It is a 4-byte
hexadecimal value.
'''

#RZ
def PTK_SetRFLabelPWAndLockRFLabel(OperationMode, OperationArea, data):
    if (
        pskfunc.PTK_SetRFLabelPWAndLockRFLabel(
            OperationMode, OperationArea.encode("utf-8"), data.encode("utf-8")
        )
        != 0
    ):
        return errorList[str(GetErrState())]
    return True

#RS
def PTK_SetRFID(
    ReservationParameters,
    ReadWriteLocation,
    ReadWriteArea,
    MaxErrNum,
    ErrProcessingMethod,
):
    if (
        pskfunc.PTK_SetRFID(
            ReservationParameters,
            ReadWriteLocation,
            ReadWriteArea,
            MaxErrNum,
            ErrProcessingMethod,
        )
        != 0
    ):
        return errorList[str(GetErrState())]
    return True

#RQ新机器不支持
# def PTK_SetRFIDCmdMode(flag):
#     if pskfunc.PTK_SetRFIDCmdMode(flag) != 0:
#         return errorList[str(GetErrState())]
#     return True


TID = 0
EPC = 1
TID_EPC = 2 #TID + EPC
USER = 3
TID_USER = 4 #TID + USER
RESERVED = 5
TID_RESERVED = 6 #TID + RESERVED


# def PTK_SetPortback(port=PORT_SCRIPT):
#     if pskfunc.PTK_SetPortback(port) != 0:
#         return -1
#     return True


def PTK_GetPrinterStatus():  # 获取打印机打印状态
    print("***PTK_GetPrinterStatus is depreciated***")
    print("Please Use PTK_GetPrintJobStatus instead")
    return PTK_GetPrinterStatus()
    
def PTK_GetPrintJobStatus():  # 获取打印机打印状态
    status = pskfunc.GetPrinterStatus()
    print(status)
    if status == 100000:
        return True
    else:
        return False

#RC+RR
def PTK_ReadRFID(block=TID, comm_mode=3, auto_foward=False, len=10):
    data = create_string_buffer(1024)
    lens = c_int(len)
    if auto_foward:
        if pskfunc.PTK_ReadRFID(block, comm_mode, 1, data, byref(lens)) != 0:
            return -1
    else:
        if pskfunc.PTK_ReadRFID(block, comm_mode, 0, data, byref(lens)) != 0:
            return -1
    return bytes.decode(data.raw[0: lens.value])

#RB
def PTK_SetEPCBlock(allnum, p1, p2, p3, p4, p5, p6):
    if PTK_SetEPCBlock(allnum, p1, p2, p3, p4, p5, p6) != 0:
        return errorList[str(GetErrState())]
    return True

HEX_WRITE = 0
ASCII_WRITE = 1
EPC_WRITE = 2

RESERVED_BLOCK = 0
EPC_BLOCK = 1
USER_BLOCK = 3

#RF1
def PTK_WriteRFID(data_mode, start_addr, len, block, data):
    if (
        pskfunc.PTK_WriteRFID(data_mode, start_addr, len,
                              block, data.encode("utf-8"))
        != 0
    ):
        return errorList[str(GetErrState())]
    return True

#RI example:RI1,0,10\n
def PTK_GetRfidTagData():
    dataLen = 4096
    dataBuff = create_string_buffer(dataLen)
    lens = c_int(dataLen)
    tagList = []
    while pskfunc.GetRITagData(dataBuff, byref(lens))== 0:
        tagList.append(bytes.decode(dataBuff.raw[0: lens.value]))
    return tagList

#开启记录RFID的TID功能日志
def PTK_RFIDLogInit():
    cmd = b"#UM>PL1\r\n"
    return PTK_SendCmdToPrinter(cmd)

#读取最近打印的RFID日志
def PTK_ReadRFIDLog(labelNums):
    path = '/mnt/user/logs/labelLog/labelLog.json'
    with open(path , 'r') as f:
        data = json.load(f)
    nums = data['labelCount'] if data['labelCount'] < labelNums else labelNums
    ret = []
    for label in data['recordList'][-nums:]:
        dd = {}
        for xx in label['itemList']:
            if xx['type'] == 16 and xx['subType'] == 517:
                dd['TID'] = xx['data']
            elif xx['type'] == 16 and xx['subType'] == 514:
                dd['RSSI'] = xx['data']
        ret.append(dd)
    return ret
    
#关闭记录RFID的TID功能日志
def PTK_RFIDLogClose():
    cmd = b"#UM>PL0\r\n"
    return PTK_SendCmdToPrinter(cmd)

# ===========================================================#
# LCD屏显示自定义变量
# ===========================================================#
"""
lcd的UI界面设计
"""
controllers = {}
requestId = 0
UI_elements = {
    "cmd": "init",
    "source": "script",
    "target": "lcd",
    "requestId": requestId,
    "isAutoRun": False,
}
total_page_num = 0
pages = []
currentPage = ""
startFlag = 0
onlyOnePageFlag = 0



class UI_element_controller:
    def __init__(self, onpressed, type):
        self.onpressed = onpressed
        self.type = type


# 定义小组件父类
class UIWidgets:
    def __init__(self, name, value, Onpressed):
        self.value = value
        self.name = name
        self.Onpressed = Onpressed
        self.id = 0
        self.enabled = True

    def execute_function(self):
        return self.Onpressed(self.value)

    # 用户改变lcd屏上小组件的值
    def update(self, value):
        global UI_elements
        global requestId

        self.value = value
        cmd = {}
        cmd["id"] = self.id
        cmd["value"] = str(value)

        UI_elements["requestId"] = requestId
        UI_elements["cmd"] = "postValue"
        UI_elements["data"] = cmd

        debuglog(json.dumps(UI_elements))
        requestId += 1
        pskfunc.PTK_WriteToLcd(json.dumps(UI_elements).encode("utf-8"))

    # 用户设置lcd屏上小组件的可交互
    def enable(self):
        global UI_elements
        global requestId

        self.enabled = True
        cmd = {}
        cmd["id"] = self.id
        cmd["value"] = True

        UI_elements["requestId"] = requestId
        UI_elements["cmd"] = "setEnabled"
        UI_elements["data"] = cmd

        debuglog(json.dumps(UI_elements))
        requestId += 1
        pskfunc.PTK_WriteToLcd(json.dumps(UI_elements).encode("utf-8"))

    # 用户设置lcd屏上小组件的不可交互
    def disable(self):
        global UI_elements
        global requestId

        self.enabled = False
        cmd = {}
        cmd["id"] = self.id
        cmd["value"] = False

        UI_elements["requestId"] = requestId
        UI_elements["cmd"] = "setEnabled"
        UI_elements["data"] = cmd

        debuglog(json.dumps(UI_elements))
        requestId += 1
        pskfunc.PTK_WriteToLcd(json.dumps(UI_elements).encode("utf-8"))


class PTK_UIButton(UIWidgets):
    def __init__(self, Onpressed, title="button", visible=True, enabled=True, name=""):
        self.type = "button"
        self.Onpressed = Onpressed
        self.title = title
        self.name = name
        self.value = "0"
        self.visible = visible
        self.enabled = enabled
        self.id = 0

    def return_json(self):
        return {
            "type": self.type,
            "id": self.id,
            "name": self.title,
            "visible": self.visible,
            "enabled": self.enabled,
        }

    def execute_function(self):
        return self.Onpressed()


class PTK_UIText(UIWidgets):
    def __init__(self, title="text", visible=True, enabled=True, name=""):
        self.type = "text"
        self.title = title
        self.name = name
        self.visible = visible
        self.enabled = enabled
        self.id = 0

    def return_json(self):
        return {
            "type": "text",
            "id": self.id,
            "name": self.title,
            "visible": self.visible,
            "enabled": self.enabled,
        }


class PTK_UITextBox(UIWidgets):
    def __init__(
        self, value="--", title="Textbox", visible=True, enabled=True, name=""
    ):
        self.type = "text"
        self.value = value
        self.title = title
        self.name = name
        self.visible = visible
        self.enabled = enabled
        self.id = 0

    def return_json(self):
        return {
            "type": "text",
            "id": self.id,
            "name": self.title,
            "value": self.value,
            "visible": self.visible,
            "enabled": self.enabled,
        }


class PTK_UIList(UIWidgets):
    def __init__(
        self,
        Onpressed,
        items=["Add Custom List Items", "0", "1"],
        title="list",
        value='0',
        valueType="int",
        valueMax="1",
        valueMin="0",
        visible=True,
        enabled=True,
        name="",
    ):
        self.type = "list"
        self.Onpressed = Onpressed
        self.items = items
        self.title = title
        self.name = name
        self.value = value
        self.valueType = valueType
        self.valueMax = valueMax
        self.valueMin = valueMin
        self.visible = visible
        self.enabled = enabled
        self.id = 0

    def return_json(self):
        return {
            "type": "list",
            "id": self.id,
            "items": self.items,
            "value": self.value,
            "visible": self.visible,
            "name": self.title,
            "valueType": self.valueType,
            "valueMax": self.valueMax,
            "valueMin": self.valueMin,
            "enabled": self.enabled,
        }

    def update_items(self, items, value = "-1"):
        global UI_elements
        global requestId

        self.items = items
        cmd = {}
        cmd["id"] = self.id
        self.value = value
        self.items = items
        cmd["value"] = value
        cmd["listItems"] = items

        UI_elements["requestId"] = requestId
        UI_elements["cmd"] = "postListItems"
        UI_elements["data"] = cmd

        debuglog(json.dumps(UI_elements))
        requestId += 1
        pskfunc.PTK_WriteToLcd(json.dumps(UI_elements).encode("utf-8"))



class PTK_UIInput(UIWidgets):
    def __init__(
        self,
        Onsubmit,
        Onchange="",
        title="input",
        value="0",
        valueType="double",
        valueMax="10.0",
        valueMin="-10.0",
        dotNum=1,
        visible=True,
        enabled=True,
        name="",
    ):
        self.type = "input"
        self.Onsubmit = Onsubmit
        self.Onchange = Onchange
        self.title = title
        self.name = name
        self.value = value
        self.valueType = valueType
        self.valueMax = valueMax
        self.valueMin = valueMin
        self.visible = visible
        self.dotNum = dotNum
        self.id = 0
        self.enabled = enabled
        self.keyboardType = 0

    def return_json(self):
        return {
            "type": "input",
            "id": self.id,
            "name": self.title,
            "value": self.value,
            "visible": self.visible,
            "valueType": self.valueType,
            "valueMax": self.valueMax,
            "valueMin": self.valueMin,
            "dotNum": self.dotNum,
            "enabled": self.enabled,
            "keyboardType": self.keyboardType
        }

    def execute_function(self):
        return self.Onsubmit(self.value)

    def changed_function(self):
        return self.Onchange(self.value)


class PTK_UIIncrement(UIWidgets):
    def __init__(
        self,
        Onchange="",
        title="increment",
        value="0",
        increments=1,
        visible=True,
        enabled=True,
        digitsPadding=1,
        name="",
    ):
        self.type = "inputnum"
        self.Onchange = Onchange
        self.title = title
        self.name = name
        self.value = value
        self.valueType = "int"
        self.valueMax = "10"
        self.valueMin = "0"
        self.visible = visible
        self.id = 0
        self.step = increments
        self.digitsPadding = digitsPadding
        self.enabled = enabled

    def return_json(self):
        return {
            "type": "inputnum",
            "id": self.id,
            "name": self.title,
            "value": self.value,
            "visible": self.visible,
            "valueType": self.valueType,
            "valueMax": self.valueMax,
            "valueMin": self.valueMin,
            "enabled": self.enabled,
            "valueMin": self.valueMin,
            "valueMax": self.valueMax,
            "digitsPadding": self.digitsPadding,
            "step": self.step
        }

    def execute_function(self):
        return self.Onchange(self.value)

class PTK_UICheckBox(UIWidgets):
    def __init__(
        self,
        Onpressed,
        title="checkbox",
        value="0",
        valueType="bool",
        valueMax="1",
        valueMin="0",
        visible=True,
        enabled=True,
        name="",
    ):
        self.type = "checkbox"
        self.Onpressed = Onpressed
        self.title = title
        self.name = name
        self.value = value
        self.valueType = valueType
        self.valueMax = valueMax
        self.valueMin = valueMin
        self.visible = visible
        self.id = 0
        self.enabled = enabled

    def return_json(self):
        return {
            "type": "checkbox",
            "id": self.id,
            "name": self.title,
            "value": self.value,
            "visible": self.visible,
            "valueType": self.valueType,
            "valueMax": self.valueMax,
            "valueMin": self.valueMin,
            "enabled": self.enabled,
        }

# 用户可调用切换UI page界面
def PTK_UIChangePage(pagenum):
    global UI_elements
    global requestId
    global pages
    global currentPage
    global total_page_num

    flag = 0
    UI_elements["cmd"] = "changePage"
    UI_elements["requestId"] = requestId

    if type(pagenum) == int:
        if pagenum < total_page_num:
            pagenum = "page_" + str(pagenum)
        else:
            debuglog("pagenum too big!")
            return -1
    elif type(pagenum) != str:
        debuglog("切换页面输入错误")

    for page in pages:
        if page.get(pagenum) != None:
            flag = 1
            currentPage = pagenum
            for value in page.values():
                UI_elements["data"] = value
    if flag == 0:
        debuglog("pagename is not exist!")
        return -1
    debuglog(json.dumps(UI_elements))

    requestId += 1
    pskfunc.PTK_WriteToLcd(json.dumps(UI_elements).encode("utf-8"))



def updatePage():
    global pages
    global controllers
    global currentPage
    for page in pages:
        if page.get(currentPage) != None:
            page[currentPage] = []
            for key, value in controllers[currentPage].items():
                if key[0:7] == 'Widget_':
                    page[currentPage].append(value.return_json())

#回复lcd关闭py文件
def responseLcdCmd(text,requestId):
    debuglog("responseLcdCmd")
    reply = {
        "cmd": "response",
        "source": "script",
        "target": "lcd",
        "data":"",
    }

    reply["rquestId"] = requestId
    reply["requestId"] = requestId
    reply["retCmd"] = text
    reply["retCode"] = 200

    debuglog(json.dumps(reply))

    pskfunc.PTK_WriteToLcd(json.dumps(reply).encode("utf-8"))

# 监听LCD消息并回调用户定义函数async
Notification_function = None
Notification_dismiss = None

def listenLcdmsg():
    lens = c_int(1024)
    dataBuff = create_string_buffer(1024)

    debuglog("监听lcd中")
    while 1:
        global controllers
        global currentPage
        global requestId
        global onlyOnePageFlag
        ret = pskfunc.PTK_GetLcdData(dataBuff, byref(lens), 5000)

        if ret == 0:
            debuglog("get lcd data:")
            changecmd = dataBuff.value.decode("utf-8")
            cmd = json.loads(changecmd)
            debuglog(cmd)
            if cmd["cmd"] == "setValue":
                debuglog('controller'+str(controllers))
                cmds = cmd["data"]
                debuglog(cmds)
                if onlyOnePageFlag == 1:
                    for widget in controllers.keys():
                        if widget == ("Widget_" + str(cmds["id"])):
                            if controllers[widget].type != "text":
                                controllers[widget].value = cmds["value"]
                                controllers[widget].execute_function()
                                debuglog("回调成功")
                else:
                    for widget in controllers[currentPage].keys():
                        if widget == ("Widget_" + str(cmds["id"])):
                            if controllers[currentPage][widget].type != "text":
                                controllers[currentPage][widget].value = cmds["value"]
                                controllers[currentPage][widget].execute_function()
                                debuglog("回调成功")
                    updatePage()
            elif cmd["cmd"] == "valueChanged":
                cmds = cmd["data"]
                debuglog(cmds)
                if onlyOnePageFlag == 1:
                    for widget in controllers.keys():
                        if widget == ("Widget_" + str(cmds["id"])):
                            if (
                                controllers[widget].type == "input"
                                and controllers[widget].Onchange != ""
                            ):
                                controllers[widget].value = cmds["value"]
                                controllers[widget].changed_function()
                                debuglog("input回调成功")
                else:
                    for widget in controllers[currentPage].keys():
                        if widget == ("Widget_" + str(cmds["id"])):
                            if (
                                controllers[currentPage][widget].type == "input"
                                and controllers[currentPage][widget].Onchange != ""
                            ):
                                controllers[currentPage][widget].value = cmds["value"]
                                controllers[currentPage][widget].changed_function()
                                debuglog("input回调成功")
                    updatePage()
            elif cmd["cmd"] == "killScript":
                global pyfilepath
                debuglog("script程序关闭")
                responseLcdCmd('killScript', cmd["requestId"])
                count_time()
                os.system("kill $(pidof python3 '%s')" % pyfilepath)
            elif cmd["cmd"] == "runScript":
                global startFlag
                startFlag = 1
                retcmd = {
                    "cmd": "response",
                    "source": "script",
                    "target": "lcd",
                    "retCmd": "runScript",
                    "retCode": 200,
                    "rquestId": cmd["rquestId"],
                }
                requestId += 1
                pskfunc.PTK_WriteToLcd(json.dumps(retcmd).encode("utf-8"))
                debuglog("运行script程序")
            elif cmd["cmd"] == "isAutoRun":
                path = "/mnt/user/OXScript/sys/autoFileList.json"
                files = {}
                if os.path.exists("/mnt/user/OXScript/sys") == False:
                    os.mkdir("/mnt/user/OXScript/sys")
                if cmd["data"]["isAutoRun"] == True:
                    # if os.access(path, os.F_OK):
                    #     with open(path, mode='r') as autofile:
                    #         files = json.loads(autofile.read())
                    #         for key in files['data'].keys():
                    #             if key == cmd['data']['fileName']:
                    #                 flag = 1
                    #                 files['data'][key] = cmd['data']['isAutoRun']
                    #         if flag == 0:
                    #             files['data'][cmd['data']['fileName']] = cmd['data']['isAutoRun']
                    #     with open(path, mode='w') as autofile:
                    #         autofile.write(json.dumps(files))
                    # else:
                    with open(path, mode="w") as autofile:
                        files["data"] = {}
                        files["data"][cmd["data"]["fileName"]] = cmd["data"][
                            "isAutoRun"
                        ]
                        autofile.write(json.dumps(files))
                else:
                    if os.access(path, os.F_OK):
                        with open(path, mode="r") as autofile:
                            files = json.loads(autofile.read())
                            if list(files["data"].keys())[0] == cmd["data"]["fileName"]:
                                files["data"][cmd["data"]["fileName"]] = False
                            with open(path, mode="w") as autofile:
                                autofile.write(json.dumps(files))
                debuglog("保存开机自动运行文件")
            elif cmd["cmd"] == "notificationFunClicked":
                debuglog("notificationFunClicked")
                global Notification_function
                Notification_function()
            elif cmd["cmd"] == "notificationClose":
                debuglog("notificationClose")
                global Notification_dismiss
                Notification_dismiss()
            else:
                # debuglog("waiting")
                pass





def startScript():
    while True:
        global startFlag
        if startFlag == 1:
            debuglog("程序开始运行！")
            return 0


def PTK_UIPage(*args):
    global total_page_num
    flag = 0
    if type(args[0]) is str:
        page_num = args[0]
    else:
        page_num = "page_" + str(total_page_num)
        flag = 1
    total_page_num += 1
    temp = {page_num: []}
    if flag == 1:
        temp[page_num].append(" ")
    for arg in args:
        if type(arg) is not str:
            index = args.index(arg)
            arg.id = index + flag
            temp[page_num].append(arg)
    return temp

def PTK_UINotification(bodyName, bodyInfo, level=1, display_funtion = None, onDismiss = None):
    cmd = {
        "cmd": "notification",
        "source": "script",
        "target": "lcd",
    }

    data = {
        "level":level,
        "bodyName": bodyName,
        "bodyInfo": bodyInfo,
        "buttonName": ''
    }

    if display_funtion != None:
        global Notification_function
        Notification_function = display_funtion
        data['buttonName'] = display_funtion.__name__

    if onDismiss != None:
        global Notification_dismiss
        Notification_dismiss = onDismiss

    cmd["data"] = data

    pskfunc.PTK_WriteToLcd(json.dumps(cmd).encode("utf-8"))

class PTK_UILodingAnimation():
    cmd = {
        "cmd": "loadingShow",
        "source": "script",
        "target": "lcd",
        "data":{
            "text":""
        }
    }
    def show(self, text):
        self.cmd["cmd"] = "loadingShow"
        self.cmd["data"]["text"] = text
        pskfunc.PTK_WriteToLcd(json.dumps(self.cmd).encode("utf-8"))

    def hide(self):
        self.cmd["cmd"] = "loadingHide"
        self.cmd["data"]["text"] = ""
        pskfunc.PTK_WriteToLcd(json.dumps(self.cmd).encode("utf-8"))

loading_animation = PTK_UILodingAnimation()

# UI初始化
def PTK_UIInit(*params, require_execute_confirmation=True):
    global UI_elements
    global requestId
    global controllers
    global pages
    global currentPage
    global onlyOnePageFlag

    debuglog('UI init begin\n')
    if type(params) == tuple and params.__len__() == 1:
        params = params[0]
        onlyOnePageFlag = 1
        for page in params.keys():
            pages.append({page: []})
            for element in params[page]:
                if element != " ":
                    pages[0][page].append(element.return_json())
                    if element.name != "":
                        controllers[element.name] = element
                    controllers["Widget_" + str(element.id)] = element
    else:
        onlyOnePageFlag = 0
        for param in params:
            for page_num in param.keys():
                pages.append({page_num: []})
                controllers[page_num] = {}
                for element in param[page_num]:
                    if element != " ":
                        pages[params.index(param)][page_num].append(
                            element.return_json()
                        )
                        if element.name != "":
                            controllers[page_num][element.name] = element
                        controllers[page_num]["Widget_" +
                                              str(element.id)] = element

    currentPage = list(pages[0].keys())[0]
    debuglog(currentPage)
    debuglog('pages:' + str(pages))

    UI_elements["fileName"] = getFilePath().split("/")[-1]
    path = "/mnt/user/OXScript/sys/autoFileList.json"

    if os.access(path, os.F_OK):
        with open(path, "r") as ff:
            jsondata = json.loads(ff.read())
            if (
                list(jsondata["data"].keys())[0] == UI_elements["fileName"]
                and jsondata["data"][UI_elements["fileName"]] == True
            ):
                UI_elements["isAutoRun"] = True
    for page in pages:
        if list(page.keys())[0] == currentPage:
            UI_elements["data"] = list(page.values())[0]

    debuglog('send to lcd' + str(json.dumps(UI_elements)))
    pskfunc.PTK_WriteToLcd(json.dumps(UI_elements).encode("utf-8"))
    requestId += 1

    # 启动小组件监听线程
    t1 = threading.Thread(target=listenLcdmsg)
    # t1.daemon = True
    t1.start()
    if require_execute_confirmation == True:
        t2 = threading.Thread(target=startScript)
        t2.start()
        t2.join()

    debuglog('UI init finished')
    return controllers

def CloseLcdUI():
    global requestId
    ccmd = '#OXScript;close;' + str(requestId) + ';#End\n'
    # global pyfilepath
    # cmd = {
    #     "cmd": "postInfo",
    #     "source": "script",
    #     "target": "lcd",
    #     "rquestId": requestId,
    #     "data":{
    #         "killScriptFile":""
    #     }
    # }
    # cmd['data']['killScriptFile'] = pyfilepath.split('/')[-1]
    # print(ccmd)
    requestId += 1
    PTK_SendCmdToPrinter(json.dumps(ccmd).encode("utf-8"))

# 脚本运行结束后自动关闭端口,同时检测是否需要写config文件
def ClosePort():
    print('Program closes automatically due to an unknown error')
    if os.path.exists("/mnt/user/OXScript/sys/oxscriptPortOpen"):
        os.remove("/mnt/user/OXScript/sys/oxscriptPortOpen")
    CloseLcdUI()
    pskfunc.ClosePort()
    # if(args.init == "True" and UI_Element_Num != 0):
    #     write_to_config_file()
    # else:
    #     pass

def handle_sigterm(signal,frame):  # 脚本强行终止执行语句
    # print("收到SIGTERM信号，执行部分代码...")
    global pyfilepath
    print("Program Terminating ...")
    # 在此处添加你想要执行的代码
    if os.path.exists("/mnt/user/OXScript/sys/oxscriptPortOpen"):
        os.remove("/mnt/user/OXScript/sys/oxscriptPortOpen")
    pskfunc.ClosePort()
    # print("代码执行完毕，终止程序")
    print("Program terminated by user, exited")
    debuglog("代码执行完毕，终止程序")
    count_time(1)
    debuglog(count_time(3))
    # 终止程序
    os.system("kill -9 $(pidof python3 '%s')" % pyfilepath)

signal.signal(signal.SIGTERM, handle_sigterm)

atexit.register(ClosePort)  # 脚本运行结束自动关闭端口


"""
版本修改记录
V1.0.0
1.发布的第一个版本
V2.0.0
1、修改库文件名称为ox_script
2、优化PTK_updateAllFormVariables替换\r\n问题
3、PTK_GetPrinterStatus问题修复
4、增加输入图片数据打印图片函数
5、修改PTK_UITextBox、PTK_UIChangePage、PTK_UICheckBox、PTK_UpdateAllFormVariables名称
6、UIButton按钮回调函数不带参数
7、增加自动寻找路径
8、修改上报lcd获取文件名函数
9、修改PTK_DrawDiagonal粗细参数可输入mm
10、修改关闭py文件通过进程号关闭
V2.0.1
1、增加串口写函数
2、修复PTK_GetPrinterStatus函数bug
3、修复多个界面时回调无效bug
4、将设置反馈端口函数放到打印函数中，且固定为反馈oxscript
5、多个页面的多个bug修复
6、UIList增加update_items方法更新选项值
7、增加PTK_UIIncrement小组件
8、修复关闭程序时执行bug
V2.0.2
1、增加回复lcd关闭py文件
2、增加显示告警功能
3、增加告警页面自定义按键回调
4、增加告警页面关闭回调
5、增加显示加载动画功能
V2.0.3
1、增加rfid写功能函数
2、修复无UI端口打开bug
3、修复文件名中有(),sh报错问题
4、修复特殊文件名运行出错bug
5、PTK_DrawGraphicsFromBytes可以支持单个文件打印多个图像
6、串口写入支持直接写ascii码值
7、debuglog优化增加时间戳
V2.0.4
1、增加获取打印机实时状态的函数PTK_GetCurrantStatus
2、PTK_GetPrinterStatus函数修正为PTK_GetPrintJobStatus
3、增加获取U盘路径函数PTK_GetExternalStorageDeviceList
V2.0.5
1、优化增加获取U盘自定义名字
2、修改反馈端口的类型定义问题
3、增加获取打印机详细信息函数PTK_GetPrinterInfo
V2.0.6
1、增加pdf转图片库
2、修复PTK_SetLabelHeight函数判断类型错误
V2.0.7
1、PTK_GetPrinterInfo增加获取设备识别号
2、注释PTK_SetRFIDCmdMode功能函数
3、修复PTK_RFIDCalibrate指令
4、注释PTK_RWRFIDLabel指令
5、修正PTK_PrintConfiguration函数名字
6、修复PTK_GetCurrantStatus函数
7、暂时不支持PTK_Reset()
8、直接使用PTK_DrawText，修复PTK_CreatFont函数，可不开放
V2.0.8
1、增加获取RI反馈数据的函数PTK_GetRfidTagData
2、PTK_PrintLabel可选是否FB反馈和RI反馈
3、修复PTK_SetRFLabelPWAndLockRFLabel()第二个参数是str类型输入并添加注释
4、PTK_RFIDCalibrate函数bug修复
5、增加RI指令的存储链表
6、PTK_GetRfidTagData返回tag列表
7、增加mqtt相关库函数
8、PTK_PrintLabel函数增加RI返回可选的区域
9、修复PTK_SendCmdToPrinter发送不同步问题
10、增加通用IO读取函数PTK_GetExternIOLevel
V2.0.9
1、修改PTK_PrintLabel函数返回值
2、修改PSKFUNC库的中文注释
3、新增yaml库
4、修复py文件异常关闭lcd屏UI未关闭问题
5、UI输入框增加设置键盘类型
V2.0.10
1、修复获取dpi失败问题
2、修复uilist的选项更新失败问题
3、修复PTK_GetExternIOLevel错误判断条件
4、增加websocket-client库
5、增加读取RFID日志的TID,RSSI的功能
V2.0.11
1、增加opentelemetry第三方库
2、修改PTK_GetCurrentStatus拼写错误
"""

