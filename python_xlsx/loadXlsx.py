import xlrd
import collections


def read_excel(file, by_name):
    ttt = returnmaxrow(file,by_name)
    data = xlrd.open_workbook(file)
    sheet = data.sheet_by_name(by_name)

    Check_obtain = 'DEVICE_'

    # Primary = sheet.cell(i, 5)
    # if (sheet.cell(i - j, 5).value == ""):
    #     j += 1
    # else:
    #     Primary = sheet.cell(i - j, 5).value
    #     break
    # AccessoryType = sheet.cell(i,6)
    # if (sheet.cell(i - j, 6).value == ""):
    #     j += 1
    # else:
    #     AccessoryType = sheet.cell(i - j, 6).value
    #     break
    # BT_BUILTIN_NREC = sheet.cell(i,7)
    # if (sheet.cell(i - j, 7).value == ""):
    #     j += 1
    # else:
    #     BT_BUILTIN_NREC = sheet.cell(i - j, 7).value
    #     break
    # BT_WBS = sheet.cell(i,ttt)
    # if(Primary == '-' and AccessoryType == '-' and BT_BUILTIN_NREC == '-' and BT_WBS == '-'):
    #     Dict.setdefault(key, []).append('PARAM::NONE')
    # if(Primary !='-'):
    #     Dict.setdefault(key, []).append('PARAM::')
    #

    Comma = ','
    Dict = {}
    for i in range(6, sheet.nrows):
        replace_value = sheet.cell(i, 1).value
        for j in range(ttt):
            if(sheet.cell(i-j,1).value == ""):
                j+=1
            else:
                replace_value = sheet.cell(i-j,1).value
                break

        if (Check_obtain in replace_value):
            key = sheet.cell(i, sheet.ncols - 1).value
            key = str(key)
            #逗号处理开始
            if(Comma in key):
                list1=str(key).split(',')
                for v in range(2):
                    key = int(list1[v])
                    if("DEVICE_IN_DEFAULT" in replace_value ):
                        list2 = str(replace_value).split("\n")
                        Android_device = list2[0]
                    else:Android_device = replace_value

                    Dict.setdefault(key, []).append('AUDIO_' + Android_device)
                    for j in range(ttt):
                        if (sheet.cell(i - j, 2).value == ""):
                            j += 1

                        else:

                            replace_value = sheet.cell(i - j, 2).value
                            break
                    Inputsource = replace_value
                    if (Inputsource == '-'):
                        Dict.setdefault(key, []).append('AUDIO_SOURCE_DEFAULT')

                    elif (Inputsource == 'Other'):
                        Dict.setdefault(key, []).append('AUDIO_SOURCE_DEFAULT')
                    else:
                        Dict.setdefault(key, []).append(Inputsource)

                    for j in range(ttt):
                        if (sheet.cell(i - j, 4).value == ""):
                            j += 1

                        else:

                            replace_value = sheet.cell(i - j, 4).value
                            break
                    Channel_Configuration = replace_value
                    if (Channel_Configuration != '-'):
                        Dict.setdefault(key, []).append("AUDIO_CHANNEL_IN_" + Channel_Configuration)
                    if (Channel_Configuration == '-'):
                        Dict.setdefault(key, []).append("AUDIO_CHANNEL_IN_MONO")

                    # Primary = sheet.cell(i, 5).value
                    # if(Primary != '-'):
                    #    d.setdefault(key, []).append("PARAM::"Primary)

                    SOMC_Platform_Device = sheet.cell(i, 9).value

                    Dict.setdefault(key, []).append(SOMC_Platform_Device)
                    #逗号处理结束

            else:
                key = round(float(key))
                if ("DEVICE_IN_DEFAULT" in replace_value):
                    list2 = str(replace_value).split("\n")
                    Android_device = list2[0]

                else:
                    Android_device = replace_value
                Dict.setdefault(key, []).append('AUDIO_' + Android_device)
                for j in range(ttt):
                    if (sheet.cell(i - j, 2).value == ""):
                        j += 1

                    else:

                        replace_value = sheet.cell(i - j, 2).value
                        break
                Inputsource = replace_value
                if (Inputsource == '-'):
                    Dict.setdefault(key, []).append('AUDIO_SOURCE_DEFAULT')

                elif (Inputsource == 'Other'):
                    Dict.setdefault(key, []).append('AUDIO_SOURCE_DEFAULT')
                else:
                    Dict.setdefault(key, []).append(Inputsource)

                for j in range(ttt):
                    if (sheet.cell(i - j, 4).value == ""):
                        j += 1

                    else:

                        replace_value = sheet.cell(i - j, 4).value
                        break
                Channel_Configuration = replace_value
                if (Channel_Configuration != '-'):
                    Dict.setdefault(key, []).append("AUDIO_CHANNEL_IN_" + Channel_Configuration)
                if (Channel_Configuration == '-'):
                    Dict.setdefault(key, []).append("AUDIO_CHANNEL_IN_MONO")

                # Primary = sheet.cell(i, 5).value
                # if(Primary != '-'):
                #    d.setdefault(key, []).append("PARAM::"Primary)

                SOMC_Platform_Device = sheet.cell(i, 9).value
                Dict.setdefault(key, []).append(SOMC_Platform_Device)


    print(Dict)
            #print()

def returnmaxrow(file,by_name):
    data = xlrd.open_workbook(file)
    sheet = data.sheet_by_name(by_name)
    ttt = 0
    for kk in sheet.merged_cells:
        a, b, c, d = kk
        u = b - a
        if (u > ttt): ttt = u
    return ttt
if __name__ == '__main__':
    read_excel('/home/CORPUSERS/xp023799/Downloads/audio/AudioHardware Device Map for Android O(Tama1.0).xlsm',
               'Non Call Input Routing')


























