def hexStringToByteArray(hexString):
    return bytearray.fromhex(hexString)


def readUInt16LE(bytes):
    value = (bytes[1] << 8) + bytes[0]
    return value & 0xFFFF


def readInt16LE(bytes):
    ref = readUInt16LE(bytes)
    return ref - 0x10000 if ref > 0x7FFF else ref


def readUInt32LE(bytes):
    value = (bytes[3] << 24) + (bytes[2] << 16) + (bytes[1] << 8) + bytes[0]
    return value & 0xFFFFFFFF


def decode(bytes):
    decoded = {}

    i = 0
    while i < len(bytes):
        channel_id = bytes[i]
        channel_type = bytes[i + 1]
        i += 2

        # BATTERY
        if channel_id == 0x01 and channel_type == 0x75:
            decoded["battery"] = bytes[i]
            i += 1
        # TEMPERATURE
        elif channel_id == 0x03 and channel_type == 0x67:
            decoded["temperature"] = readInt16LE(bytes[i : i + 2]) / 10
            i += 2
        # HUMIDITY
        elif channel_id == 0x04 and channel_type == 0x68:
            decoded["humidity"] = bytes[i] / 2
            i += 1
        elif channel_id == 0x20 and channel_type == 0xCE:
            point = {}
            point["timestamp"] = readUInt32LE(bytes[i : i + 4])
            point["temperature"] = readInt16LE(bytes[i + 4 : i + 6]) / 10
            point["humidity"] = bytes[i + 6] / 2

            if not "history" in decoded:
                decoded["history"] = []

            decoded["history"].append(point)
            i += 8
        else:
            break

    return decoded


def decodeHelper(hexString):
    byteArray = hexStringToByteArray(hexString)
    return decode(byteArray)
