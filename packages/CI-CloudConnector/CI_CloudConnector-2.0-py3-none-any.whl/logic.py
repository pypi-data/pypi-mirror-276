
import logging, time, datetime, sys, os, socket, configparser, random, tzlocal, glob, fnmatch
import platform
from datetime import datetime

from cpppo.server.enip import address, client  # for EtherNet/IP communication

VER = "2.0"

TagsDefenitionFileName = "TagsDefenition.txt"
TagsValuesFileName = "[NEW]TagsValues"
TagsValueDir = "TagValues"
HomeDir = "CI_LC"
GetTagsFromServerMinRateSeconds = 10
GetCloudVersionFromServerMinRateSeconds = 10
g_VerifySSL = False  # True = do not allow un verified connection , False = Allow

# config
cfg_server_address = ""
cfg_username = ""
cfg_password = ""
cfg_max_files = ""
cfg_log_level = ""


sugestedUpdateVersion = ""
configFile = "config.ini"
ScanRateLastRead = {}
currentToken = ""
g_connectorTypeName = ""
g_lastGetTagsFromServer = None
g_lastGetCloudVersionFromServer = None
g_app_log = None

def enum(**enums):
    return type("Enum", (), enums)

TagStatus = enum(Invalid=10, Valid=20)

def initialize_log(log_level=""):

    global VER
    global g_app_log
    try:
        if g_app_log:
            return

        default_log_level = logging.WARNING
        if log_level == "DEBUG":
            default_log_level = logging.DEBUG
        if log_level == "INFO":
            default_log_level = logging.INFO
        if log_level == "ERROR":
            default_log_level = logging.ERROR

        from logging.handlers import RotatingFileHandler

        log_formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s"
        )
        log_file = "CI_CloudConnector.log"
        log_handler = RotatingFileHandler(
            log_file,
            mode="a",
            maxBytes=5 * 1024 * 1024,
            backupCount=7,
            encoding=None,
            delay=0,
        )
        log_handler.setFormatter(log_formatter)

        app_logger = logging.getLogger("root")
        app_logger.setLevel(default_log_level)
        app_logger.addHandler(log_handler)
        log_handler.doRollover()

        app_logger.critical("initialize_log DONE")
        g_app_log = app_logger

    except Exception as ex:
        print("Error in initialize_log " +  str(ex))


# ============================
def read_last_rows_from_log(maxNumberOfRows=10):
    log_file_path = "CI_CloudConnector.log"
    last_rows = []
    i = maxNumberOfRows
    for line in reversed(open(log_file_path, "r").readlines()):
        last_rows.append(line.rstrip())
        i = i - 1
        if i <= 0:
            return last_rows
    return last_rows


# ============================
def setLogLevel(lvl):
    try:
        if str(lvl) in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]:
            lvl = logging.getLevelName(str(lvl))

    except Exception as inst:
        print("Error in setLogLevel", inst)


# ============================
def ci_print(msg, level=""):
    global g_app_log
    try:
        if level == "DEBUG":
            g_app_log.debug(msg)
        elif level == "INFO":
            g_app_log.info(msg)
        elif level == "ERROR":
            g_app_log.error(msg)
        else:
            g_app_log.warning(msg)

        # print(level+"::"+msg)
    except Exception as inst:
        g_app_log.warning("Main Exception :: " + inst)


# ============================
def SendLogToServer(log):

    try:
        print("send ::") + log
        ret = addCloudConnectorLog(log, datetime.now)
    except:
        return



# ============================
def handleError(message, err):
    try:
        err_desc = str(err)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        srtMsg = (
            message
            + " , "
            + str(err_desc)
            + " , "
            + str(exc_type)
            + " , "
            + str(fname)
            + " , "
            + str(exc_tb.tb_lineno)
        )
        # print(message, err_desc, exc_type, fname, exc_tb.tb_lineno)
        ci_print(srtMsg, "ERROR")
    except Exception as errIgnore:
        ci_print("Error in handleError " + str(errIgnore), "ERROR")


# ============================
def getAliveFile():

    ret = None
    try:
        fileName = "/" + HomeDir + "/lc_pid.txt"
        # read alive file
        f = open(fileName, "r")
        ret = json.load(f)
        # print 'getAliveFile file=' + str(ret)
    except Exception as inst:
        handleError("Error in getAliveFile", inst)
    return ret


# ============================

import os
import configparser

def initialize_config(overwrite=False):

    global cfg_server_address
    global cfg_username
    global cfg_password
    global cfg_max_files
    global cfg_log_level

    try:
        file_path = f"/{HomeDir}/{configFile}"

        log_levels_info = " , other options (DEBUG , INFO , WARNING , ERROR)"

        if os.path.exists(file_path) and not overwrite:
            config = configparser.ConfigParser()
            config.read(file_path)

            cfg_server_address = config.get("Server", "Address")
            cfg_username = config.get("Server", "username")
            cfg_password = config.get("Server", "password")
            cfg_max_files = config.get("Server", "maxFiles")
            log_level = config.get("Logging", "Level", fallback=cfg_log_level)

            initialize_log(log_level)

            ci_print(f"Server Address: {cfg_server_address}", "INFO")
            ci_print(f"Username: {cfg_username}", "INFO")
            ci_print(f"Password: {cfg_password}", "INFO")
            ci_print(f"Max Files: {cfg_max_files}", "INFO")
            ci_print(f"VERSION: {getLocalVersion()}")

        else:
            ci_print(f"Config not found or overwrite is True, creating new one in {file_path}", "INFO")
            config = configparser.ConfigParser()
            config.add_section("Server")
            config.add_section("Logging")

            def get_input(prompt, current_value):
                value = input(prompt + f" (Currently: {current_value}): ")
                return value if value else current_value

            cfg_server_address = get_input("Enter Server Address (e.g., https://localhost:63483)", cfg_server_address)
            cfg_username = get_input("Enter new user name", cfg_username)
            cfg_password = get_input("Enter password", cfg_password)
            cfg_max_files = get_input("Enter Max Files", cfg_max_files)
            cfg_log_level = get_input(f"Enter Logging Level {log_levels_info}", cfg_log_level)

            config.set("Server", "Address", cfg_server_address)
            config.set("Server", "username", cfg_username)
            config.set("Server", "password", cfg_password)
            config.set("Server", "maxFiles", cfg_max_files)
            config.set("Logging", "Level", cfg_log_level)


            with open(file_path, "w") as configfile:
                config.write(configfile)

            initialize_config()  # Reload the config after updating

    except Exception as inst:
        handleError("Error in initialize_config", inst)




# ============================
def reboot():

    try:
        if platform.system() == "Windows":
            ci_print("Reboot not supported on Windows.", "INFO")
            #subprocess.run(["shutdown", "/r", "/t", "0"], check=True)
        else:
            ci_print("Reboot not supported on !Windows.", "INFO")
            #os.system("sudo reboot")
    except Exception as ex:
        handleError("Error in reboot", ex)



# Cloud Functions
# ============================
import requests
import json

cfg_server_address = "your_server_address"
g_VerifySSL = True
currentToken = ""
cfg_username = "your_username"
cfg_password = "your_password"


def get_cloud_token():

    global cfg_server_address
    global g_VerifySSL
    global currentToken

    if currentToken:
        return currentToken

    url = f"{cfg_server_address}/api/CloudConnector/Token"

    try:
        response = requests.post(
            url,
            data={
                "grant_type": "password",
                "username": cfg_username,
                "password": cfg_password,
            },
            headers={
                "User-Agent": "python",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            verify=g_VerifySSL,
        )

        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.text

        jsonData = json.loads(data)
        token = jsonData.get("access_token", "")

        if token:
            currentToken = token

    except requests.exceptions.RequestException as e:
        handleError("Error getting Token", e)
        token = ""
    except json.JSONDecodeError as e:
        handleError("Error decoding token response", e)
        token = ""
    except KeyError as e:
        handleError("Token not found in response", e)
        token = ""

    return token


# ============================
# make http request to cloud if fails set currentToken='' so it will be initialized next time
# ============================
def ciRequest(url, data, postGet="get", method="", token=""):
    print(f"{datetime.now()}, START CIRequest {method}, VERSION: {VER}")

    ans = {}
    ans["isOK"] = False
    global currentToken
    ansIsSucessful = False
    try:
        if token == "":
            print("Skipping " + method + " - no Token")
            ans["isOK"] = False
            return ans;
        else:
            if postGet == "post":
                response = requests.post(
                    url,
                    data,
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "text/plain",
                        "Authorization": "bearer %s" % token,
                    },
                    verify=g_VerifySSL,
                )
            else:
                response = requests.get(
                    url,
                    data=None,
                    headers={"Authorization": "bearer %s" % token},
                    verify=g_VerifySSL,
                )

            if response.status_code == 403:
                currentToken = ""
            ansIsSucessful = True
    except Exception as err:
        handleError("Error in ciRequest " + method, err)
        currentToken = ""
        ansIsSucessful = False

    ans["isOK"] = ansIsSucessful
    ans["response"] = response
    return ans



# ============================
def get_cloud_version():

    global GetCloudVersionFromServerMinRateSeconds
    global g_lastGetCloudVersionFromServer
    global currentToken
    global VER
    global sugestedUpdateVersion

    if currentToken == "":
        currentToken = get_cloud_token()

    token = currentToken

    tags = None

    try:
        now = datetime.now()
        getVersionTimePass = 0

        if g_lastGetCloudVersionFromServer:
            getVersionTimePass = (now - g_lastGetCloudVersionFromServer).total_seconds()

        if getVersionTimePass == 0 or getVersionTimePass > GetCloudVersionFromServerMinRateSeconds:

            # print "update pid file for watchdog"
            # do after clock settings because some times the machine loads with old clock and trigger watchdog

            # print "handleNewRequests"
            handleNewRequests()

            # print 'getting version from server'

            g_lastGetCloudVersionFromServer = datetime.now()
            ip_address = socket.gethostbyname(socket.gethostname())
            url = f"{cfg_server_address}/api/CloudConnector/GetVersion/?version={VER}&IpAddress={ip_address}"

            ret = ciRequest(url, None, "get", "getCloudVersion", token)
            response = ret["response"]

            if not ret["isOK"]:
                return ""

            ans = json.loads(response.text)
            update_to_version = ans[0]

            sugestedUpdateVersion = update_to_version

            if bool(update_to_version) != "" and bool(update_to_version != VER):
                ci_print(f"Local Version: {VER} but Server suggests Other Version: {update_to_version}", "INFO")

    except Exception as err:
        print(str(err))
        handleError("Error getting Version from cloud", err)
        sugestedUpdateVersion = ""

    return sugestedUpdateVersion


# ============================
def get_cloud_tags(token=""):

    global g_lastGetTagsFromServer
    global GetTagsFromServerMinRateSeconds

    tags = None

    try:
        IpAddress = socket.gethostbyname(socket.gethostname())
        url = f"{cfg_server_address}/api/CloudConnector/GetTags/"

        tags = None

        now = datetime.now()
        getTagsTimePass = 0

        if g_lastGetTagsFromServer:
            getTagsTimePass = (now - g_lastGetTagsFromServer).total_seconds()

        if getTagsTimePass == 0 or getTagsTimePass > GetTagsFromServerMinRateSeconds:
            ret = ciRequest(url, None, "get", "getCloudTags", token)
            if ret and ret["isOK"] == True:
                response = ret["response"]
                g_lastGetTagsFromServer = datetime.now()
                ans = json.loads(response.text)
                arranged_tags = arrange_tags_by_scan_time(ans["Tags"])
                tags = {"Tags": arranged_tags}

                with open(TagsDefenitionFileName, "w") as f:
                    json.dump(tags, f)

            else:
                ci_print("Failed to retrieve Tags from Cloud server", "WARNING")
    except Exception as inst:
        print(str(inst))
        handleError("Error getting tags from cloud", inst)
        tags = None

    if tags == None:
        tags = getTagsDefenitionFromFile()

    return tags


# ============================
def arrange_tags_by_scan_time(tags):
    ans = {}

    try:
        for index in range(len(tags)):
            scan_rate = tags[index]["ScanRate"]

            if scan_rate in ans:
                tagsListPerScanRate = ans[scan_rate]
            else:
                ans[scan_rate] = []

            ans[scan_rate].append(tags[index])
    except Exception as err:
        handleError("Error arranging tags by scan time", err)
    return ans


# ============================
def printTags(tags):
    try:
        ci_print(str(tags))

        for tag in tags:
            tag_id = tag.get("TagId", "")
            tag_name = tag.get("TagName", "")
            tag_address = tag.get("TagAddress", "")
            scan_rate = tag.get("ScanRate", "")

            msg = f"Tag Id: {tag_id}, TagName: {tag_name}, TagAddress: {tag_address}, ScanRate: {scan_rate}"
            ci_print(msg, "INFO")

    except Exception as inst:
        handleError("Error in printTags", inst)


# ============================
def setCloudTags(tagValues, token=""):
    print('setCloudTags')
    global TagStatus
    updatedSuccessfully = False
    try:
        # url = HTTP_PREFIX + '://'+cfg_server_address+'/api/CloudConnector/SetCounterHistory/'
        url = cfg_server_address + "/api/CloudConnector/SetCounterHistory/"

        payload = []
        for index in range(len(tagValues)):
            TagId = tagValues[index]["TagId"]
            timeStamp = str(tagValues[index]["time"])

            value = tagValues[index]["value"]
            status = TagStatus.Invalid
            if str(tagValues[index]["status"]) == "20":
                status = TagStatus.Valid


            tagVal = {
                "TagId": TagId,
                "TimeStmp": timeStamp,
                "StatusCE": status,
                "Value": value,
            }
            payload.append(tagVal)

        ci_print('setCloudTags: ' + str(payload), "INFO")
        ret = ciRequest(url, json.dumps(payload), "post", "setCloudTags", token)
        response = ret["response"]

        updatedSuccessfully = response.status_code == 200

    except Exception as inst:
        handleError("Error setting tags in cloud", inst)
        return False

    return updatedSuccessfully


# ============================
def sendLogFileToCloud(numberOfRows=10, timestamp="", requestId=""):

    try:
        requestId = str(requestId)
        lines = read_last_rows_from_log(numberOfRows)
        for line in lines:
            # print "line:" + line
            addCloudConnectorLog(line, timestamp, str(requestId))
    except Exception as inst:
        handleError("sendLogFileToCloud: Error setting tags in cloud", inst)
        return False


# ============================
def addCloudConnectorLog(log, timeStamp="", requestId=""):

    global currentToken
    if timeStamp == "":
        timeStamp = datetime.now()
    updatedSuccessfully = False

    token = currentToken
    if token == "":
        print("no token skip addCloudConnectorLog", "INFO")
        return
    try:
        url = cfg_server_address + "/api/CloudConnector/SetCounterLog/"

        payload = []
        logData = {"Log": log, "TimeStamp": str(timeStamp), "RequestId": requestId}
        payload.append(logData)
        # print str(payload)
        ret = ciRequest(url, json.dumps(payload), "post", "SetConnectorLog", token)
        response = ret["response"]

        # print (response.text)
        # logging.info('setCloudTags response = ' + str(response) + ' : ' + response.text )
        # print '==' + str(response.status_code)
        updatedSuccessfully = response.status_code == 200

    except Exception as inst:
        handleError("Exception in addCloudConnectorLog", inst)
        return False

    return updatedSuccessfully


# ============================
def getCloudConnectorRequests():

    global currentToken
    token = currentToken


    ans = None
    try:
        url = cfg_server_address + "/api/CloudConnector/GetCloudConnectorRequests/"
        ret = ciRequest(url, None, "get", "GetCloudConnectorRequests", token)
        # print "ret=" + str(ret)
        response = ret["response"]
        if ret["isOK"] == True:
            ans = json.loads(response.text)
    except Exception as inst:
        handleError("Error getting requests from cloud", inst)
        ans = None

    return ans


# ============================
def updateCloudConnectorRequests(requestId, status):

    global currentToken
    updatedSuccessfully = False

    token = currentToken
    if token == "":
        ci_print("no token skip updateCloudConnectorRequests", "WARNING")
        return
    try:
        url = (
            cfg_server_address
            + "/api/CloudConnector/SetCounterRequestStatus/?requestId="
            + str(requestId)
            + "&status="
            + str(status)
        )
        # print "url="+url
        ret = ciRequest(url, "", "post", "SetCounterRequestStatus", token)
        response = ret["response"]

        print(response.text)
        # logging.info('setCloudTags response = ' + str(response) + ' : ' + response.text )
        # print '==' + str(response.status_code)
        updatedSuccessfully = response.status_code == 200

    except Exception as inst:
        handleError("Exception in addCloudConnectorLog", inst)
        # handleError("Error setting tags in cloud", inst)
        return False

    return updatedSuccessfully


# get requests from cloud and handle it
# ============================
def handleNewRequests():

    try:
        requests = getCloudConnectorRequests()
        if requests:

            for request in requests:
                try:
                    # print 'request[Type]=' + str(request['Type'])
                    if request["Type"] == 1:  # send logs
                        # print "Handling request " + str(request)
                        requestData = json.loads(request["Data"])
                        rownCount = requestData["Rows"]
                        ret = updateCloudConnectorRequests(request["Id"], 2)  # in process
                        requestData = json.loads(request["Data"])
                        # print "--------request['Id']===" + str(request['Id'])
                        sendLogFileToCloud(rownCount, "", request["Id"])
                        ret = updateCloudConnectorRequests(request["Id"], 3)  # Done
                    if request["Type"] == 2:  # change logs level
                        ci_print(
                            "Handling change log level request " + str(request), "INFO"
                        )
                        requestData = json.loads(request["Data"])
                        newLogLevel = requestData["Level"]
                        ret = updateCloudConnectorRequests(request["Id"], 2)  # in process
                        setLogLevel(newLogLevel)
                        ret = updateCloudConnectorRequests(request["Id"], 3)  # Done
                    if request["Type"] == 3:  # reboot
                        ci_print("Handling reboot request " + str(request), "INFO")
                        ret = updateCloudConnectorRequests(request["Id"], 3)  # Done
                        reboot()
                except Exception as innerinst:
                    print("error handling request ") + str(innerinst)
                    handleError("Error setting tags in inner handleNewRequests", innerinst)
    except Exception as inst:
        handleError("Error in handleNewRequests", inst)
        return False


# ============================
# PLC Functions
# ============================
def fill_Invalids(tagsDefenitions, values):

    global TagStatus

    retValues = []
    try:
        time = str(datetime.now(tzlocal.get_localzone()))
        valuesDict = {}
        ci_print("start fill_Invalids", "INFO")
        # prepare values dictionery
        for val in values:
            # print "val" + str(val)
            # print "val[u'TagId']=" + str(val[u'TagId'])
            valuesDict[val["TagId"]] = val
        # print "valuesDict="+str(valuesDict)
        for tagdef in tagsDefenitions:
            TagId = tagdef["TagId"]
            # print "tagdef" + str(tagdef)
            if TagId in valuesDict:
                retValues.append(valuesDict[TagId])
            else:
                tagAddress = tagdef["TagAddress"]
                val = {
                    "TagAddress": tagAddress,
                    "TagId": TagId,
                    "time": time,
                    "value": None,
                    "status": TagStatus.Invalid,
                }
                retValues.append(val)
        # print "=============="
        # print str(retValues)
    except Exception as inst:
        handleError("Error in fill_Invalids", inst)

    return retValues


# ippp
# ============================
def readEtherNetIP_Tags(tags_definitions):

    global TagStatus
    ci_print("start readEtherNetIP_Tags", "INFO")
    ans = []

    arranged_tags = arrange_tags_by_plc(tags_definitions)

    try:

        for plc_address, tags_def_list in arranged_tags.items():
            tags = [tag_def["TagAddress"] for tag_def in tags_def_list]
            ci_print("readEtherNetIP_Tags: Read tags " + str(tags), "DEBUG")

            with client.connector(host=plc_address, port=address[1], timeout=1.0) as connection:
                operations = client.parse_operations(tags)
                failures, transactions = connection.process(
                    operations=operations,
                    depth=1,
                    multiple=0,
                    fragment=False,
                    printing=False,
                    timeout=1.0,
                )

            #host = plc_address  # Controller IP address
            #port = address[1]  # default is port 44818
            #depth = 1  # Allow 1 transaction in-flight
            #multiple = 0  # Don't use Multiple Service Packet
            #fragment = False  # Don't force Read/Write Tag Fragmented
            #timeout = 1.0  # Any PLC I/O fails if it takes > 1s
            #printing = False  # Print a summary of I/O

            ci_print("transactions " + str(transactions), "INFO")
            ci_print("failures " + str(failures), "INFO")


            # client.close()
            # sys.exit( 1 if failures else 0 )

            for index, tag_def in enumerate(tags_def_list):
                tag_address = tag_def["TagAddress"]
                try:
                    if transactions[index]:
                        tag_id = int(tag_def["TagId"])
                        value = transactions[index][0]
                        time = str(datetime.now(tzlocal.get_localzone()))
                        ci_print("get register tagAddress=" + str(tag_address) + " value=" + str(value), "INFO")
                        val = {
                            "TagAddress": tag_address,
                            "TagId": tag_id,
                            "time": time,
                            "value": value,
                            "status": TagStatus.Valid,
                        }
                        ans.append(val)
                    else:
                        ci_print("Error reading Tag " + tag_address, "INFO")
                except ValueError:
                    handleError("Error reading tag value " + tag_address, ValueError)

        ci_print("End Read readEtherNetIP Tag", "INFO")
    except Exception as inst:
        handleError("Error in readEtherNetIP_Tags", inst)

    return fill_Invalids(tags_definitions, ans)


def arrange_tags_by_plc(tags_definitions):

    arranged_tags = {}

    for tag_def in tags_definitions:
        plc_address = tag_def.get("PlcIpAddress")
        if plc_address:
            if plc_address not in arranged_tags:
                arranged_tags[plc_address] = []
            arranged_tags[plc_address].append(tag_def)

    return arranged_tags

# ============================
def readModBusTags(tags_definitions):

    ans = []

    arranged_tags = arrange_tags_by_plc(tags_definitions)

    try:
        ci_print("Start Read ModBus Tag", "INFO")

        for plc_address in arranged_tags:
            maxOffset = 0
            for p in arranged_tags[plc_address]:
                offset = int(p.TagAddress)
                maxOffset = max(maxOffset, offset)

            from pymodbus.client import ModbusTcpClient as ModbusClient

            client = ModbusClient(plc_address, port=502)
            client.connect()

            rr = client.read_input_registers(0, maxOffset)  # 30000
            ci_print(str(rr.registers), "INFO")


            for index in range(len(plc_address)):
                try:
                    offset = int(plc_address[index]["TagAddress"]) - 1
                    TagId = int(plc_address[index]["TagId"])

                    value = rr.registers[offset]
                    time = str(datetime.now(tzlocal.get_localzone()))
                    ci_print("get register offset=" + str(offset) + " value=" + str(value), "INFO")
                    val = {
                        "TagAddress": offset,
                        "TagId": TagId,
                        "time": time,
                        "value": value,
                        "status": TagStatus.Valid,
                    }
                    ans.append(val)
                    # ans.update({offset:[offset,CounterId,datetime.now(),value]})
                except ValueError:
                    ci_print(
                        "Error reading tag value " + plc_address[index]["TagAddress"],
                        "DEBUG",
                    )

            client.close()

        ci_print("End Read ModBus Tag", "INFO")
        return ans
    except Exception as inst:
        handleError("error reading modbus", inst)
        return fill_Invalids(tags_definitions, ans)


# ============================
def readSimulation_Tags(tags_definitions):

    ans = []
    arranged_tags = arrange_tags_by_plc(tags_definitions)

    ci_print("Start Read readSimulation_Tags", "INFO")


    try:

        for plc_address, tags_def_list in arranged_tags.items():
            for index, tag_def in enumerate(tags_def_list):
                try:
                    TagId = int(tag_def.get("TagId"))
                    value = random.uniform(-10, 10)
                    time = str(datetime.now(tzlocal.get_localzone()))
                    val = {
                        "TagId": TagId,
                        "time": time,
                        "value": value,
                        "status": TagStatus.Valid,
                    }
                    ans.append(val)
                    ci_print(f"PLC Address: {plc_address}, TagId: {TagId}, value: {value} ScanRate: {tag_def.get('ScanRate')}")


                except (ValueError, TypeError) as e:
                    ci_print(f"Error processing tag definition: {e}")


        ci_print("End Read readSimulation_Tags", "INFO")
    except Exception as inst:
        handleError("Error in readSimulation_Tags", inst)

    return ans


# ============================
def printTagValues(tagValues):
    ci_print("Count " + str(len(tagValues)) + " Tags", "INFO")
    for index in range(len(tagValues)):
        ci_print(str(tagValues[index]), "INFO")


# ============================
def getLocalVersion():
    return VER


# ============================
def getServerSugestedVersion():
    return sugestedUpdateVersion


# ============================
# Tag Files Functions
# ============================
def writeTagsDefenitionToFile(tags):

    try:

        f = open(TagsDefenitionFileName, "w")
        json.dump(tags, f)
        f.close()
        return
    except Exception as inst:
        handleError("Error in writeTagsDefenitionToFile", inst)


# ============================
def getTagsDefenitionFromFile():

    try:
        f2 = open(TagsDefenitionFileName, "r")
        tags = json.load(f2)
        f2.close()
        return tags
    except Exception as inst:
        handleError("Error in getTagsDefenitionFromFile", inst)


# ============================
def delTagsDefenitionFile():

    try:
        os.remove(TagsDefenitionFileName)
        return
    except Exception as inst:
        handleError("Error in delTagsDefenitionFile", inst)


# ============================
def getTagsValuesFromFile(fileName):

    try:
        f2 = open(fileName, "r")
        vals = json.load(f2)
        f2.close()

        return vals
    except Exception as inst:
        handleError("Error in getTagsValuesFromFile", inst)


# ============================
def saveValuesToFile(values, fileName):

    try:
        numOfFiles = len(
            fnmatch.filter(os.listdir("/" + HomeDir + "/" + TagsValueDir), "*.txt")
        )

        if numOfFiles < 10000:
            if fileName == "":
                fileName = (
                    TagsValuesFileName
                    + datetime.now().strftime("%Y%m%d-%H%M%S%f")
                    + ".txt"
                )
            # fileName = "./" + TagsValueDir + '/' + fileName
            fileName = "/" + HomeDir + "/" + TagsValueDir + "/" + fileName

            # write tags to file
            f = open(fileName, "w")
            json.dump(values, f)
            f.close()
            time.sleep(1)  # prevent two files in same ms
        else:
            ci_print("Too many files in folder!!!", "WARNING")
    except Exception as inst:
        handleError("Error in saveValuesToFile", inst)

# ============================
def handleValuesFile(fileName, token=""):

    try:
        values = getTagsValuesFromFile(fileName)
        isOk = setCloudTags(values, token)
        if isOk:
            os.remove(fileName)
            return True
        else:
            # errFile = replaceFileName(fileName,"ERR")
            errFile = fileName.replace("/[NEW]", "/ERR/[ERR]")
            os.rename(fileName, errFile)
    except Exception as inst:
        handleError("Error in handleValuesFile", inst)
    return False

# ============================
def handleAllValuesFiles(token=""):

    try:
        i = 0
        dirpath = "/" + HomeDir + "/" + TagsValueDir + "/"
        filesSortedByTime = [
            s for s in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, s))
        ]
        filesSortedByTime.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))

        for file in filesSortedByTime:
            if file.endswith(".txt") and file.startswith("[NEW]"):
                i = i + 1
                handleValuesFile("/" + HomeDir + "/" + TagsValueDir + "/" + file, token)


    except Exception as inst:
        ci_print("Error handleAllValuesFiles " + str(inst))


# ============================
def create_directories_if_missing():
    try:
        # Create HomeDir if missing

        dirName = "/" + HomeDir + "/"
        d = os.path.dirname(dirName)

        home_dir_path = os.path.join("/", HomeDir)
        if not os.path.exists(home_dir_path):
            os.makedirs(home_dir_path)
            ci_print(f"Created directory: {home_dir_path}", "INFO")

        # Create TagsValueDir if missing
        tags_value_dir_path = os.path.join(home_dir_path, TagsValueDir)
        if not os.path.exists(tags_value_dir_path):
            os.makedirs(tags_value_dir_path)
            ci_print(f"Created directory: {tags_value_dir_path}", "INFO")

        # Create ERR directory inside TagsValueDir if missing
        err_dir_path = os.path.join(tags_value_dir_path, "ERR")
        if not os.path.exists(err_dir_path):
            os.makedirs(err_dir_path)
            ci_print(f"Created directory: {err_dir_path}", "INFO")

    except Exception as e:
        ci_print(f"Error in create_directories_if_missing: {e}")


# ============================
# Remove oldest file
# ============================
def removeOldestFile():

    global cfg_max_files

    try:
        dirName = "/" + HomeDir + "/" + TagsValueDir + "/"
        dir = os.path.dirname(dirName)
        if os.path.exists(dir):
            list_of_files = glob.glob(dirName + '*.txt')
            num_of_files = len(list_of_files)
            maxFiles = int(cfg_max_files)

            if maxFiles < num_of_files & num_of_files > 0:
                # In case more than one file is exceeding cfg_max_files.
                # Used for initial case where num of files is much bigger than config MaxFiles.
                for x in range(maxFiles, num_of_files):
                    oldest_file = min(list_of_files, key=os.path.getctime)
                    os.remove(oldest_file)
                    list_of_files.remove(oldest_file)

    except Exception as inst:
        handleError("Error in removeOldestFile", inst)


def arrange_by_connector_type(tags_def):
    arranged_tags = {}

    for tag in tags_def:
        connector_type = tag.get('connectorTypeName', '')  # Provide a default value if key doesn't exist
        if connector_type not in arranged_tags:
            arranged_tags[connector_type] = []
        arranged_tags[connector_type].append(tag)

    return arranged_tags

# ============================
# Main Loop
# ============================
def Main():

    global ScanRateLastRead
    global currentToken
    try:

        if currentToken == "":
            currentToken = get_cloud_token()
        # currently must get tags from cloud to init server before setting values
        tagsDefScanRatesAns = get_cloud_tags(currentToken)
        tagsDefScanRates = tagsDefScanRatesAns["Tags"]

        for scanRate in tagsDefScanRates:

            if scanRate in (None, 'null'):
                continue

            scanRateInt = int(scanRate)
            scanRateStr = str(scanRate)
            diff = 0
            if scanRateStr in ScanRateLastRead:
                now = datetime.now()
                diff = (now - ScanRateLastRead[scanRateStr]).total_seconds()
                # print ('diff = -------' + str(diff))


            if diff + 3 > scanRateInt or diff == 0:


                tagsDef = tagsDefScanRates[scanRate]
                arranged_tags = arrange_by_connector_type(tagsDef)

                for connector_type in arranged_tags:
                    print(connector_type)
                    values = None
                    if connector_type == "Simulation":
                        values = readSimulation_Tags(arranged_tags[connector_type])
                    if connector_type == "Modbus":
                        values = readModBusTags(arranged_tags[connector_type])
                    if connector_type == "Ethernet/IP":
                        values = readEtherNetIP_Tags(arranged_tags[connector_type])
                        if values == []:
                            ci_print("Ethernet Empty values ::1", "ERROR")
                            values = readEtherNetIP_Tags(arranged_tags[connector_type])
                            if values == []:
                                time.sleep(0.1)
                                ci_print("Ethernet Empty values ::1", "ERROR")
                                values = readEtherNetIP_Tags(arranged_tags[connector_type])
                                if values == []:
                                    time.sleep(1)
                                    ci_print("Ethernet Empty values ::2", "ERROR")
                                    values = readEtherNetIP_Tags(arranged_tags[connector_type])

                    #if len(values) > 0:
                    #    ci_print(f'ScanRate: {scanRate}, DIFF: {diff}, Values: {values}')
                    #else:
                    #    ci_print(f'ScanRate: {scanRate}, DIFF: {diff}, No Values')

                    if values:
                        saveValuesToFile(values, "")
                        removeOldestFile()

                        now = datetime.now()
                        ScanRateLastRead[scanRateStr] = now


        if currentToken != "":
            handleAllValuesFiles(currentToken)
        else:
            ci_print("No Token, skipping upload step", "WARNING")
    except Exception as inst:
        handleError("Error in Main", inst)
        currentToken = ""



