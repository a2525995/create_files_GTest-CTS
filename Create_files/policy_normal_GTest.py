#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import os, requests
import getpass

name = input("input:your account")
pwd = input("input:your password")

# url
# xml

URL_HEAD = '???????'
POLICY_XML_URL = URL_HEAD + '?????'

DOWNLOAD_DIR = os.path.abspath('.') + '/download_file'

OUT_DIR = os.path.abspath('.') + '/output'
file_name_normal_list = [OUT_DIR + '/PolicyTestCases_NormalTests_Pcm_16bit.h',
                  OUT_DIR + '/PolicyTestCases_NormalTests_Pcm_8_24bit.h',
                  OUT_DIR + '/PolicyTestCases_NormalTests_Pcm_24bit_packed.h',
                  OUT_DIR + '/PolicyTestCases_NormalTests_Pcm_32bit.h',
                  ]
file_name_BT_list = [
                  OUT_DIR + '/PolicyTestCases_BtTests_Pcm_16bit.h',
                  OUT_DIR + '/PolicyTestCases_BtTests_Pcm_8_24bit.h',
                  OUT_DIR + '/PolicyTestCases_BtTests_Pcm_24bit_packed.h',
                  OUT_DIR + '/PolicyTestCases_BtTests_Pcm_32bit.h',

]
file_name_USB_list = [
                  OUT_DIR + '/PolicyTestCases_UsbTests_Pcm_16bit.h',
                  OUT_DIR + '/PolicyTestCases_UsbTests_Pcm_8_24bit.h',
                  OUT_DIR + '/PolicyTestCases_UsbTests_Pcm_24bit_packed.h',
                  OUT_DIR + '/PolicyTestCases_UsbTests_Pcm_32bit.h',
]
POLICY_XML = DOWNLOAD_DIR + '/audio_policy_configuration.xml'

TAB3 = '\t\t\t'
TAB4 = '\t\t\t\t'
LINE = '///////////////////////////////////////////////////////////////'
TEST_NUM_DETAILS = '/// \\brief   PolicyTest      : '
USECASE_DETAILS = '/// \\details Usecase         : compress-offload-playback'
FRONT_END_DETAILS = '/// \\details DSP front end   : MultiMedia4'
BACK_END_DETAILS = '/// \\details DSP back end    : '
APP_TYPE_DETAILS = '/// \\details ACDB app type   : '
FORMAT_DETAILS = '/// \\details AFE format      : '
CHANNEL_DETAILS = '/// \\details AFE channel     : '
SAMPLE_RATE_DETAILS = '/// \\details AFE sample rate : '

# Android output device
OUTPUT_DEVICE = 'NORMAL_OUT( // Android output device'
OUTPUT_DEVICE_VALUE = 'AUDIO_DEVICE_OUT_'
OUTPUT_DEVICE_NORMAL_VALUE = "WIRED_HEADSET,"
OUTPUT_DEVICE_USB_VALUE    = "USB_DEVICE,"
OUTPUT_DEVICE_BT_VALUE     = "BLUETOOTH_A2DP,"
# Stream configuration
STREAM_CONFIGURATION = '// Stream configuration'
audio_format_value = ''
channel_masks_value_list = []
sampling_rate_value_list = []
AUDIO_OUTPUT_FLAG_VALUE = '(AUDIO_OUTPUT_FLAG_DIRECT|AUDIO_OUTPUT_FLAG_COMPRESS_OFFLOAD|AUDIO_OUTPUT_FLAG_NON_BLOCKING),'

# Parameters
PARAMS = '// Parameters'
PARAMS_VALUE = 'PARAM::NONE,'
#COMMA
COMMA =","

# ------------------------------------

# Expected usecase
USECASE = '// Expected usecase'
USECASE_VALUE = 'USECASE_AUDIO_PLAYBACK_OFFLOAD,'
# Expected dsp front end
FRONT_END = '// Expected dsp front end'
FRONT_END_VALUE = 'DSPFE::FRONTEND_MULTIMEDIA4,'
# Expected dsp back end
BACK_END = '// Expected dsp back end'
BACK_END_VALUE = 'DSPBE::BACKEND_'
# Expected back end details
BACK_END_DETAILS_NORMAL_VALUE = "SLIMBUS_0_RX"
BACK_END_DETAILS_USB_VALUE    = "USB_AUDIO_RX"
BACK_END_DETAILS_BT_VALUE     = "SLIMBUS_7_RX"
# Expected acdb app type
APP_TYPE = '// Expected acdb app type'
app_type_normal_list = ['69936,', '69940,', '69940,', '69942,']
app_type_usb_list    = ['69936,', '69940,', '69940,', '69942,']
app_type_bt_list     = ['69936,', '69940,', '69940,', '69942,']
# Expected afe format
AFE_FORMAT = '// Expected afe format'
afe_format_normal_list = ['AFEFMT::FORMAT_S16_LE,', 'AFEFMT::FORMAT_S24_3LE,', 'AFEFMT::FORMAT_S24_3LE,',
                   'AFEFMT::FORMAT_S24_LE,','AFEFMT::FORMAT_S32_LE']
afe_format_usb_list = ['AFEFMT::FORMAT_S16_LE,', 'AFEFMT::FORMAT_S32_LE,', 'AFEFMT::FORMAT_S24_3LE,',
                   'AFEFMT::FORMAT_S32_LE,','AFEFMT::FORMAT_S32_LE,']
afe_format_bt_list = ['AFEFMT::FORMAT_S24_LE,','AFEFMT::FORMAT_S24_3LE,', 'AFEFMT::FORMAT_S24_3LE,',
                   'AFEFMT::FORMAT_S24_LE,','AFEFMT::FORMAT_S32_LE,']
# Expected afe channel
AFE_CHANNEL = '// Expected afe channel'
AFE_CHANNEL_NORMAL_VALUE = 'AFECH::CHANNEL_TWO,'
AFE_CHANNEL_USB_VALUE    = 'AFECH::CHANNEL_ONE,'
# Expected channel details value
CHANNEL_DETAILS_NORMAL_VALUE = "2"
CHANNEL_DETAILS_USB_VALUE = "1"

# Expected afe sample rate
AFE_SAMPLE_RATE = '// Expected afe sample rate'
afe_sample_rate_list = ['AFERATE::SAMPLE_RATE_KHZ_48),', 'AFERATE::SAMPLE_RATE_KHZ_96),',
                        'AFERATE::SAMPLE_RATE_KHZ_192),','AFERATE::SAMPLE_RATE_KHZ_8),',
                        'AFERATE::SAMPLE_RATE_KHZ_32),','AFERATE::SAMPLE_RATE_KHZ_16),',
                        'AFERATE::SAMPLE_RATE_KHZ_11p025),','AFERATE::SAMPLE_RATE_KHZ_22p05),',
                        'AFERATE::SAMPLE_RATE_KHZ_44p1),','AFERATE::SAMPLE_RATE_KHZ_88p2),',
                        'AFERATE::SAMPLE_RATE_KHZ_176p4),','AFERATE::SAMPLE_RATE_KHZ_352p8),',
                        'AFERATE::SAMPLE_RATE_KHZ_384),',]


def get_html_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'}
    re = requests.get(url, headers=headers)
    re.encoding = re.apparent_encoding
    return re.text


# download file
def download_file():
    file_name = POLICY_XML_URL[POLICY_XML_URL.rfind('/') + 1:]
    file_text = get_html_content(POLICY_XML_URL)

    file = open(DOWNLOAD_DIR + '/' + file_name, 'w')
    file.write(file_text)
    file.close()


def create_folder():
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)


def write_file_head(num,file_name_list):
    file_name_path = file_name_list[num]
    file_name = file_name_path[file_name_path.rfind('/') + 1:]
    pcm_level = file_name[file_name.find('Pcm_') + 4:file_name.find('bit')].replace('_', '.')
    if 'packed' in file_name:
        pcm_level = pcm_level + ' packed'

    with open(file_name_path, 'w') as f:
        f.write('////////////////////////////////////////////////////////////////////////////////\n')
        f.write('/// \\file ' + file_name + '\n')
        f.write('/// \\brief Defines policy normal test cases for direct pcm' + pcm_level + '\n')
        f.write('///\n')
        f.write('/// All policy normal test cases are specified in\n')
        f.write('/// http://XXXX (T.B.D)\n')
        f.write('/// \\remark This file is only intended to be included from PolicyTest.cpp. Thus\n')
        f.write('///         it intentionally contains no inclusion guards\n')
        f.write('///\n')
        f.write('/// Test configurations should be set up as follows:\n')
        f.write('/// \\code\n')
        f.write('/// <INITIAL_STATE>( <Android output device>,\n')
        f.write('///                  <Stream configuration>\n')
        f.write('///                      - format\n')
        f.write('///                      - channel mask\n')
        f.write('///                      - sampling rate\n')
        f.write('///                      - flags\n')
        f.write('///                  <Input source> *** for input case only ***\n')
        f.write('///                  <Parameters>\n')
        f.write('///                  <Expected usecase>\n')
        f.write('///                  <Expected dsp front end>\n')
        f.write('///                  <Expected dsp back end>\n')
        f.write('///                  <Expected acdb app type>\n')
        f.write('///                  <Expected afe format>\n')
        f.write('///                  <Expected afe channel>\n')
        f.write('///                  <Expected afe sample rate> )\n')
        f.write('/// \\endcode\n')
        f.write('///\n')
        f.write('/// \\addtogroup AudioPolicyTests\n')
        f.write('////////////////////////////////////////////////////////////////////////////////\n\n\n')


def add_method_normal_file(file_name_list):
    policy_tree = ET.ElementTree(file=POLICY_XML)

    for elem in policy_tree.iterfind('modules/module/mixPorts/mixPort/[@name="direct_pcm"]'):

        file_num = 0
        for child_of_elem in elem:
            test_num = 0
            method_head_notes = ''
            audio_format_value = child_of_elem.attrib['format']
            channel_masks_value_list = child_of_elem.attrib['channelMasks'].split(',')
            sampling_rate_value_list = child_of_elem.attrib['samplingRates'].split(',')

            for channel in channel_masks_value_list:

                method_head_notes = '// ' + audio_format_value + ', ' + channel
                with open(file_name_list[file_num], 'a') as f:
                    f.write(method_head_notes + '\n')

                for rate in sampling_rate_value_list:
                    rate_int = int(rate)
                    if rate_int == 128000 or rate_int <= 48000:
                        khz_index = 0
                    elif rate_int >= 176400:
                        khz_index = 2
                    else:
                        khz_index = 1

                    app_type_note_value = app_type_normal_list[file_num][:app_type_normal_list[file_num].find(',')]
                    afe_format_note_value = afe_format_normal_list[file_num][
                                            afe_format_normal_list[file_num].find('_') + 1:afe_format_normal_list[file_num].find(',')]
                    afe_sample_rate_note_value = afe_sample_rate_list[khz_index][
                                                 afe_sample_rate_list[khz_index].find('KHZ'):afe_sample_rate_list[
                                                     khz_index].find(')')]

                    method_notes = LINE + '\n' + TEST_NUM_DETAILS + '%02d' % (test_num) + '\n' \
                                   + USECASE_DETAILS + '\n' + FRONT_END_DETAILS + '\n' + BACK_END_DETAILS+BACK_END_DETAILS_NORMAL_VALUE + '\n' \
                                   + APP_TYPE_DETAILS + app_type_note_value + '\n' \
                                   + FORMAT_DETAILS + afe_format_note_value + '\n' \
                                   + CHANNEL_DETAILS +CHANNEL_DETAILS_NORMAL_VALUE+ '\n' \
                                   + SAMPLE_RATE_DETAILS + afe_sample_rate_note_value + '\n' + LINE

                    method_body = OUTPUT_DEVICE + '\n' + TAB4 + OUTPUT_DEVICE_VALUE + OUTPUT_DEVICE_NORMAL_VALUE + '\n' \
                                  + TAB3 + STREAM_CONFIGURATION + '\n' + TAB4 + audio_format_value + ',\n' + TAB4 + channel + ',\n' + TAB4 + rate + ',\n' + TAB4 + AUDIO_OUTPUT_FLAG_VALUE + '\n' \
                                  + TAB3 + PARAMS + '\n' + TAB4 + PARAMS_VALUE + '\n' + TAB3 + '//------------------------------------' + '\n' \
                                  + TAB3 + USECASE + '\n' + TAB4 + USECASE_VALUE + '\n' + TAB3 + FRONT_END + '\n' + TAB4 + FRONT_END_VALUE + '\n' \
                                  + TAB3 + BACK_END + '\n' + TAB4 + BACK_END_VALUE + BACK_END_DETAILS_NORMAL_VALUE + COMMA + '\n' + TAB3 + APP_TYPE + '\n' + TAB4 + \
                                  app_type_normal_list[file_num] + '\n' \
                                  + TAB3 + AFE_FORMAT + '\n' + TAB4 + afe_format_normal_list[
                                      file_num] + '\n' + TAB3 + AFE_CHANNEL + '\n' + TAB4 + AFE_CHANNEL_NORMAL_VALUE + '\n' \
                                  + TAB3 + AFE_SAMPLE_RATE + '\n' + TAB4 + afe_sample_rate_list[khz_index] + '\n'

                    with open(file_name_list[file_num], 'a') as f:
                        f.write(method_notes + '\n')
                        f.write(method_body + '\n')
                    test_num += 1
            file_num += 1

def add_method_usb_file(file_name_list):
    policy_tree = ET.ElementTree(file=POLICY_XML)

    for elem in policy_tree.iterfind('modules/module/mixPorts/mixPort/[@name="direct_pcm"]'):

        file_num = 0
        for child_of_elem in elem:
            test_num = 0
            method_head_notes = ''
            audio_format_value = child_of_elem.attrib['format']
            channel_masks_value_list = child_of_elem.attrib['channelMasks'].split(',')
            sampling_rate_value_list = child_of_elem.attrib['samplingRates'].split(',')

            for channel in channel_masks_value_list:

                method_head_notes = '// ' + audio_format_value + ', ' + channel
                with open(file_name_list[file_num], 'a') as f:
                    f.write(method_head_notes + '\n')

                for rate in sampling_rate_value_list:
                    rate_int = int(rate)
                    if   rate_int == 8000:
                        khz_index = 3
                    elif rate_int == 11025:
                        khz_index = 6
                    elif rate_int == 12000 or rate_int == 24000 or rate_int == 48000 or rate_int == 128000:
                        khz_index = 0
                    elif rate_int == 16000:
                        khz_index = 5
                    elif rate_int == 22050:
                        khz_index = 7
                    elif rate_int == 32000:
                        khz_index = 4
                    elif rate_int == 44100:
                        khz_index = 8
                    elif rate_int == 64000 or rate_int == 96000:
                        khz_index = 1
                    elif rate_int == 88200:
                        khz_index = 9
                    elif rate_int == 176400:
                        khz_index = 10
                    elif rate_int == 352800:
                        khz_index = 11
                    elif rate_int == 384000:
                        khz_index = 12
                    app_type_note_value = app_type_usb_list[file_num][:app_type_usb_list[file_num].find(',')]
                    afe_format_note_value = afe_format_usb_list[file_num][
                                            afe_format_usb_list[file_num].find('_') + 1:afe_format_usb_list[file_num].find(',')]
                    afe_sample_rate_note_value = afe_sample_rate_list[khz_index][
                                                 afe_sample_rate_list[khz_index].find('KHZ'):afe_sample_rate_list[
                                                     khz_index].find(')')]

                    method_notes = LINE + '\n' + TEST_NUM_DETAILS + '%02d' % (test_num) + '\n' \
                                   + USECASE_DETAILS + '\n' + FRONT_END_DETAILS + '\n' + BACK_END_DETAILS+ BACK_END_DETAILS_USB_VALUE+ '\n' \
                                   + APP_TYPE_DETAILS + app_type_note_value + '\n' \
                                   + FORMAT_DETAILS + afe_format_note_value + '\n' \
                                   + CHANNEL_DETAILS +CHANNEL_DETAILS_USB_VALUE+ '\n' \
                                   + SAMPLE_RATE_DETAILS + afe_sample_rate_note_value + '\n' + LINE

                    method_body = OUTPUT_DEVICE + '\n' + TAB4 + OUTPUT_DEVICE_VALUE + OUTPUT_DEVICE_USB_VALUE + '\n' \
                                  + TAB3 + STREAM_CONFIGURATION + '\n' + TAB4 + audio_format_value + ',\n' + TAB4 + channel + ',\n' + TAB4 + rate + ',\n' + TAB4 + AUDIO_OUTPUT_FLAG_VALUE + '\n' \
                                  + TAB3 + PARAMS + '\n' + TAB4 + PARAMS_VALUE + '\n' + TAB3 + '//------------------------------------' + '\n' \
                                  + TAB3 + USECASE + '\n' + TAB4 + USECASE_VALUE + '\n' + TAB3 + FRONT_END + '\n' + TAB4 + FRONT_END_VALUE + '\n' \
                                  + TAB3 + BACK_END + '\n' + TAB4 + BACK_END_VALUE + BACK_END_DETAILS_USB_VALUE + COMMA + '\n' + TAB3 + APP_TYPE + '\n' + TAB4 + \
                                  app_type_usb_list[file_num] + '\n' \
                                  + TAB3 + AFE_FORMAT + '\n' + TAB4 + afe_format_usb_list[
                                      file_num] + '\n' + TAB3 + AFE_CHANNEL + '\n' + TAB4 + AFE_CHANNEL_USB_VALUE + '\n' \
                                  + TAB3 + AFE_SAMPLE_RATE + '\n' + TAB4 + afe_sample_rate_list[khz_index] + '\n'

                    with open(file_name_list[file_num], 'a') as f:
                        f.write(method_notes + '\n')
                        f.write(method_body + '\n')
                    test_num += 1
            file_num += 1

def add_method_bt_file(file_name_list):
    policy_tree = ET.ElementTree(file=POLICY_XML)

    for elem in policy_tree.iterfind('modules/module/mixPorts/mixPort/[@name="direct_pcm"]'):

        file_num = 0
        for child_of_elem in elem:
            test_num = 0
            method_head_notes = ''
            audio_format_value = child_of_elem.attrib['format']
            channel_masks_value_list = child_of_elem.attrib['channelMasks'].split(',')
            sampling_rate_value_list = child_of_elem.attrib['samplingRates'].split(',')

            for channel in channel_masks_value_list:

                method_head_notes = '// ' + audio_format_value + ', ' + channel
                with open(file_name_list[file_num], 'a') as f:
                    f.write(method_head_notes + '\n')

                for rate in sampling_rate_value_list:
                    rate_int = int(rate)
                    khz_index = 0
                    app_type_note_value = app_type_usb_list[file_num][:app_type_usb_list[file_num].find(',')]
                    afe_format_note_value = afe_format_bt_list[file_num][
                                            afe_format_bt_list[file_num].find('_') + 1:afe_format_bt_list[file_num].find(',')]
                    afe_sample_rate_note_value = afe_sample_rate_list[khz_index][
                                                 afe_sample_rate_list[khz_index].find('KHZ'):afe_sample_rate_list[
                                                     khz_index].find(')')]

                    method_notes = LINE + '\n' + TEST_NUM_DETAILS + '%02d' % (test_num) + '\n' \
                                   + USECASE_DETAILS + '\n' + FRONT_END_DETAILS + '\n' + BACK_END_DETAILS+ BACK_END_DETAILS_NORMAL_VALUE+ '\n' \
                                   + APP_TYPE_DETAILS + app_type_note_value + '\n' \
                                   + FORMAT_DETAILS + afe_format_note_value + '\n' \
                                   + CHANNEL_DETAILS + CHANNEL_DETAILS_NORMAL_VALUE + '\n' \
                                   + SAMPLE_RATE_DETAILS + afe_sample_rate_note_value + '\n' + LINE

                    method_body = OUTPUT_DEVICE + '\n' + TAB4 + OUTPUT_DEVICE_VALUE + OUTPUT_DEVICE_BT_VALUE + '\n' \
                                  + TAB3 + STREAM_CONFIGURATION + '\n' + TAB4 + audio_format_value + ',\n' + TAB4 + channel + ',\n' + TAB4 + rate + ',\n' + TAB4 + AUDIO_OUTPUT_FLAG_VALUE + '\n' \
                                  + TAB3 + PARAMS + '\n' + TAB4 + PARAMS_VALUE + '\n' + TAB3 + '//------------------------------------' + '\n' \
                                  + TAB3 + USECASE + '\n' + TAB4 + USECASE_VALUE + '\n' + TAB3 + FRONT_END + '\n' + TAB4 + FRONT_END_VALUE + '\n' \
                                  + TAB3 + BACK_END + '\n' + TAB4 + BACK_END_VALUE + BACK_END_DETAILS_BT_VALUE + COMMA + '\n' + TAB3 + APP_TYPE + '\n' + TAB4 + \
                                  app_type_usb_list[file_num] + '\n' \
                                  + TAB3 + AFE_FORMAT + '\n' + TAB4 + afe_format_bt_list[
                                      file_num] + '\n' + TAB3 + AFE_CHANNEL + '\n' + TAB4 + AFE_CHANNEL_NORMAL_VALUE + '\n' \
                                  + TAB3 + AFE_SAMPLE_RATE + '\n' + TAB4 + afe_sample_rate_list[khz_index] + '\n'

                    with open(file_name_list[file_num], 'a') as f:
                        f.write(method_notes + '\n')
                        f.write(method_body + '\n')
                    test_num += 1
            file_num += 1
def main():
    create_folder()

    download_file()

    for num in range(len(file_name_normal_list)):
        write_file_head(num,file_name_normal_list)

    add_method_normal_file(file_name_normal_list)

    for num in range(len(file_name_BT_list)):
        write_file_head(num,file_name_BT_list)

    add_method_bt_file(file_name_BT_list)

    for num in range(len(file_name_USB_list)):
        write_file_head(num,file_name_USB_list)

    add_method_usb_file(file_name_USB_list)

if __name__ == '__main__':
    main()
