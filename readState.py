import serial
import binascii,time

def hexShow(argv):        #十六进制显示 方法1
    try:
        result = ''  
        hLen = len(argv)  
        for i in range(hLen):  
            hvol = argv[i]
            hhex = '%02x'%hvol  
            result += hhex+' '  
            # print('hexShow:',result)
    except:
        pass
    return result

def bytes2int(inputdata:list, num:int):
    data_high = inputdata[num]
    data_low = inputdata[num + 1]
    data_int = data_high * 256 + data_low
    return data_int

def batteryHealth(temperature:int):
    if temperature < 0:
        return 6
    elif temperature <= 40 & temperature >= 0:
        return 1
    elif temperature >= 40:
        return 2
    else:
        return

def getState(com_name:str, baud_rate:int):
    ser = serial.Serial(com_name, baud_rate, timeout=0.1)
    # print('连接成功')
    # 发送请求数据
    state_req = 'DD A5 03 00 FF FD 77'
    request_data = bytes.fromhex(state_req)
    ser.write(request_data)
    # print('发送成功')
    response_data = ser.read(40)  # 根据您的数据长度调整读取的字节数
    if response_data:   # 如果读取结果非空，则输出
        # data= str(binascii.b2a_hex(response_data))[2:-1] #十六进制显示方法2
        data3 = hexShow(response_data)
        out_data = data3.split()
        # print(out_data, type(out_data), len(out_data))

        # 解析返回数据
        if out_data[2] == '00':
            print('ok')
            voltage = bytes2int(response_data, 4) / 100
            print('Current voltage: %.2f V' % voltage)
            current = bytes2int(response_data, 6) / 100
            print('Current current: %.2f A' % current)
            capacity = bytes2int(response_data, 8) / 100
            print('Current capacity: %.2f Ah' % capacity) 
            design_capacity = bytes2int(response_data, 10) / 100
            print('Design capacity: %.2f Ah' % design_capacity)
            temp_sensor = response_data[26]
            temperature1 = (bytes2int(response_data, 27) -2731) / 10
            temperature2 = (bytes2int(response_data, 29) -2731) / 10
            temperature = max(temperature1, temperature2)
            print('%d temp sensors detected. \n \
                Temperature1: %.2f C, Temperature2: %.2f C, Max temperature: %.2f C' \
                % (temp_sensor, temperature1, temperature2, temperature))
            percentage = response_data[23]
            print('Battery percentage: %.2f %%' % percentage)
            cellsNum = response_data[25]
            print('Battery cells: %d' % cellsNum)
    # 关闭串口连接
    else:
        pass
    ser.close()


def main(args=None):
    com_name = '/dev/battery'
    baud_rate = 9600
    voltage_list = getState(com_name, baud_rate)



if __name__ == '__main__':
    main()