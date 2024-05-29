#!/usr/bin/env python

"""
 * CVE-2020-3452
 * CVE-2020-3452 Bug scanner for WebPentesters and Bugbounty Hunters
 *
 * @Developed By Cappricio Securities <https://cappriciosec.com>
 */


"""


def writedata(output, data):
    with open(output, 'a') as file:
        file.write(data)
