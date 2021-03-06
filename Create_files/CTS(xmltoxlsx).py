#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import xml.etree.cElementTree as ET
import sys, os

#sys.path.append("/home/CORPUSERS/xp023799/")
import xlsxwriter

tree = ET.ElementTree(file='/home/CORPUSERS/xp023799/test_result1.xml')
workbook = xlsxwriter.Workbook('result.xlsx')
sheet = workbook.add_worksheet('Result')

red_title_format = workbook.add_format({
    'font_name': 'Arial',
    'bold': True,
    'color': 'red'
})

title_format = workbook.add_format({
    'font_name': 'Arial',
    'bold': True,
    'border': 1,
    'border_color': '#6d766b',
    'align': 'center',
    'valign': 'vcenter',
    'bg_color': 'yellow'
})

failured_title_format = workbook.add_format({
    'font_name': 'Arial',
    'bold': True,
    'font_size': 20,
    'align': 'center',
    'valign': 'vcenter'

})

failured_module_format = workbook.add_format({
    'font_name': 'Arial',
    'bold': True,
    'font_size': 12,
    'valign': 'vcenter'

})

failured_result_format = workbook.add_format({
    'font_name': 'Arial',
    'bold': True,
    'font_size': 8,
    'bg_color': '#fa5858',
    'align': 'center',
    'valign': 'vcenter'

})

failured_value_format = workbook.add_format({
    'font_name': 'Arial',
    'border': 1,
    'border_color': '#a5c639'
})


def getSummaryList(tree):
    suite_plan = ''
    suite_build = ''
    host_info = ''
    start_end_time = ''
    test_pass = ''
    test_fail = ''
    test_not_executed = ''
    module_done = ''
    module_total = ''
    fingerprint = ''
    security = ''
    release_sdk = ''
    abis = ''

    # Result attrib
    resultElement = tree.getroot()
    suiteName = resultElement.attrib['suite_name']
    suitePlan = resultElement.attrib['suite_plan']
    suiteVersion = resultElement.attrib['suite_version']
    suiteBuildNumber = resultElement.attrib['suite_build_number']
    host_name = resultElement.attrib['host_name']
    osName = resultElement.attrib['os_name']
    osVersion = resultElement.attrib['os_version']
    startDisplay = resultElement.attrib['start_display']
    endDisplay = resultElement.attrib['end_display']

    suite_plan = suiteName + ' / ' + suitePlan
    suite_build = suiteVersion + ' / ' + suiteBuildNumber
    host_info = 'Result/@start ' + host_name + '(' + osName + ' - ' + osVersion + ')'
    start_end_time = startDisplay + ' / ' + endDisplay

    # Summary attrib
    for summaryElement in tree.iterfind('Summary'):
        testPassed = summaryElement.attrib['pass']
        testFailed = summaryElement.attrib['failed']
        # notExecuted = summaryElement.attrib['not_executed']
        modulesDone = summaryElement.attrib['modules_done']
        modulesTotal = summaryElement.attrib['modules_total']

        test_pass = testPassed
        test_fail = testFailed
        # test_not_executed = notExecuted
        module_done = modulesDone
        module_total = modulesTotal

        # Build attrib
    for buildElement in tree.iterfind('Build'):
        buildFingerprint = buildElement.attrib['build_fingerprint']
        buildVersion_security_patch = buildElement.attrib['build_version_security_patch']
        buildVersion_release = buildElement.attrib['build_version_release']
        buildVersion_sdk = buildElement.attrib['build_version_sdk']
        buildAbis = buildElement.attrib['build_abis']

        fingerprint = buildFingerprint
        security = buildVersion_security_patch
        release_sdk = buildVersion_release + '(' + buildVersion_sdk + ')'
        abis = buildAbis

    summaryList = (
        ['Suite / Plan', suite_plan], ['Suite / Build', suite_build], ['Host Info', host_info],
        ['Start time / End Time', start_end_time], ['Tests Passed', test_pass], ['Tests Failed', test_fail],
        ['Tests Not Executed', test_not_executed], ['Modules Done', module_done], ['Modules Total', module_total],
        ['Fingerprint', fingerprint], ['Security Patch', security], ['Release (SDK)', release_sdk], ['ABIs', abis]
    )

    return summaryList


def getFailuredCount(tree):
    fail_count = 0
    for testElement in tree.iterfind('Module/TestCase/Test'):
        test_result = testElement.attrib['result']
        if test_result != 'pass':
            fail_count += 1
    fail_count = str(fail_count)
    return fail_count


def failuredExcelList(tree):
    fail_count = 0
    failuredRow = 2
    failuredModuleTestRow = 5
    failuredColumn = 5
    failuredModuleTestColumn = 2
    for testElement in tree.iterfind('Module/TestCase/Test'):
        test_result = testElement.attrib['result']
        if test_result != 'pass':
            fail_count += 1
    fail_count = str(fail_count)
    # Failured Tests Title
    sheet.write(failuredRow, failuredColumn, 'Failured Tests ' + '(' + fail_count + ')', failured_title_format)

    for moduleElement in tree.iterfind('Module'):
        moduleElementName = moduleElement.attrib['name']
        moduleElementAbi = moduleElement.attrib['abi']

        for testCaseElement in moduleElement.getchildren():
            testCaseName = testCaseElement.attrib['name']

            for testElement in testCaseElement:
                testName = testElement.attrib['name']
                testResult = testElement.attrib['result']
                #print a = 'run cts -- module/-m '+moduleElementName+' -- test '+testCaseName+' CTS'

                if testResult != 'pass':
                    for failureElement in testElement:
                        #print a = 'run cts -- module/-m ' + moduleElementName + ' -- test ' + testCaseName + ' CTS'
                        failureDetails = failureElement.attrib['message']

                        module_title = moduleElementName + ' - ' + moduleElementAbi
                        failured_test_name = testCaseName + '#' + testName
                        failured_test_result = testResult
                        failure_details = failureDetails

                        sheet.set_row(failuredModuleTestRow, 20)
                        sheet.write(failuredModuleTestRow + 1, failuredModuleTestColumn, 'Test', title_format)
                        sheet.write(failuredModuleTestRow + 1, failuredModuleTestColumn + 1, 'Result', title_format)
                        sheet.write(failuredModuleTestRow + 1, failuredModuleTestColumn + 2, 'Details', title_format)

                        sheet.write(failuredModuleTestRow, failuredModuleTestColumn, module_title,
                                    failured_module_format)
                        sheet.write(failuredModuleTestRow + 2, failuredModuleTestColumn, failured_test_name,
                                    failured_value_format)
                        sheet.write(failuredModuleTestRow + 2, failuredModuleTestColumn + 1, failured_test_result,
                                    failured_result_format)
                        sheet.write(failuredModuleTestRow + 2, failuredModuleTestColumn + 2, failure_details,
                                    failured_value_format)

                        failuredModuleTestRow += 5


def creatExcelList(worksheet):
    # Failured Tests
    worksheet.set_column(2, 10, 35)
    worksheet.write(2, 2, 'Fail Details_This round', red_title_format)


if __name__ == '__main__':
    creatExcelList(sheet)
    failuredExcelList(tree)
    workbook.close()
