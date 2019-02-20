# -*- encoding: utf-8 -*-
"""This module implement the ``Cleaner`` class to clean the text from standard patterns such as SAP tags, date/hours...

It is not intended to remove (business) stopwords or other patterns not to extract entities. It is intended to be used
first on a raw text to remove tags automatically added by the IT systems. It aims to remove a lot of Personal
Identifiable Information and a lot of noise.

Concerning the tags, the following are supported:

    * SAP: ARP, Corp, A-F, A-D
    * P-Aerotech
    * TLB
    * e-QLB
    * IRS5, IRS11
    * FOLIO5

Examples
--------

.. code::

    from nlp4airbus.re.clean import Cleaner

    text='''
        Rampe déterioré
        * 18.06.2016 10:38:21 CET ADEL CHAKIR (NG30537) Phone 33 582055747
        * NonConformity 0001 :
        * Type of nonconformity: Broken
        *
        * LOCALISATION:
        * Soute 1, cadre 42-43, sous le rail Y+1012, côté gauche.
        *
        * NON-CONFORMITE:
        * Suite à une inspection, nous constatons une rampe endommagé et
        * plié.
        *
        * Voir standard doc
        *
        * Demandons refus et remplacement de la rampe
        * --------------------------------------
        * ----------------------------------------
        * 18.06.2016 10:51:04 CET ADEL CHAKIR (NG30537) Phone 33 582055747
        * Text of Task 0001 " ORI0 "
        * 18.06.2016 10:51:00 CET ADEL CHAKIR (NG30537) Phone 33 582055747
        *
        * 18.06.2016 10:51:04 CET ADEL CHAKIR (NG30537) Phone 33 582055747
        * 20.06.2016 11:38:55 CET CHANH LUAN LE (NG51F18) Tél. 33 686706013
        * 20.06.2016 11:39:45 CET CHANH LUAN LE (NG51F18) Tél. 33 686706013
        * ----------------------------------------
        * 20.06.2016 11:41:05 CET CHANH LUAN LE (NG51F18) Tél. 33 686706013
        * *Texte tâche 0200 " DEC0 "
        * 20.06.2016 11:40:38 CET CHANH LUAN LE (NG51F18) Tél. 33 686706013
        * Demande changement la rampe V92422553000 .
        * 20.06.2016 11:41:05 CET CHANH LUAN LE (NG51F18) Tél. 33 686706013
        * 20.06.2016 11:44:45 CET CHANH LUAN LE (NG51F18) Tél. 33 686706013
        * ----------------------------------------
        * 20.06.2016 11:47:01 CET CHANH LUAN LE (NG51F18) Tél. 33 686706013
        * *Texte tâche 0298 " DEC0 "
        * 20.06.2016 11:46:31 CET CHANH LUAN LE (NG51F18) Tél. 33 686706013
        * Remontage via S03 de réappro:1003481050
        * 20.06.2016 11:47:01 CET CHANH LUAN LE (NG51F18) Tél. 33 686706013
        * 24.06.2016 09:50:29 CET CHANH LUAN LE (NG51F18) Tél. 33 686706013
        * Remontage de la nouvelle rampe via S03:1003481050.
        * 24.06.2016 09:51:06 CET CHANH LUAN LE (NG51F18) Tél. 33 686706013
        * ----------------------------------------
        * 27.06.2016 11:51:14 CET YOHANN ROBERT (NG23587) Tél. 33 648642991
        * *Texte tâche 0396 " DO00 "
        * 27.06.2016 11:51:11 CET YOHANN ROBERT (NG23587) Tél. 33 648642991
        *
        * 27.06.2016 11:51:14 CET YOHANN ROBERT (NG23587) Tél. 33 648642991
        * ----------------------------------------
        * 27.06.2016 11:51:24 CET YOHANN ROBERT (NG23587) Tél. 33 648642991
        * *Texte tâche 0445 " DO00 "
        * 27.06.2016 11:51:21 CET YOHANN ROBERT (NG23587) Tél. 33 648642991
        *
        * 27.06.2016 11:51:24 CET YOHANN ROBERT (NG23587) Tél. 33 648642991
        * ----------------------------------------
        * 27.06.2016 13:42:36 CET RIDDA CHOUGRANI (NG3DC29) Tél. 0
        * *Texte tâche 0494 " ATW0 "
        * 27.06.2016 13:42:21 CET RIDDA CHOUGRANI (NG3DC29) Tél. 0
        * travail fait sur avion
        * 27.06.2016 13:42:36 CET RIDDA CHOUGRANI (NG3DC29) Tél. 0
        * ----------------------------------------
        * 30.06.2016 14:23:47 CET RAISSA AUFUN (NG5C4B7) Tél. 0
        * *Texte tâche 0500 " ATQ0 "
        * 30.06.2016 14:23:41 CET RAISSA AUFUN (NG5C4B7) Tél. 0
        *
        * 30.06.2016 14:23:47 CET RAISSA AUFUN (NG5C4B7) Tél. 0
        * 30.06.2016 14:24:19 CET RAISSA AUFUN (NG5C4B7) Tél. 0'''
    c = Cleaner()
    print(c.clean(text))
    '''
    Rampe déterioré
    NonConformity 0001 :
    Type of nonconformity: Broken
    LOCALISATION:
    Soute 1, cadre 42-43, sous le rail Y+1012, côté gauche.
    NON-CONFORMITE:
    Suite à une inspection, nous constatons une rampe endommagé et
    plié.
    Voir standard doc
    Demandons refus et remplacement de la rampe
    Text of Task 0001 " ORI0 "
    Texte tâche 0200 " DEC0 "
    Demande changement la rampe V92422553000 .
    Texte tâche 0298 " DEC0 "
    Remontage via S03 de réappro:1003481050
    Remontage de la nouvelle rampe via S03:1003481050.
    Texte tâche 0396 " DO00 "
    Texte tâche 0445 " DO00 "
    Texte tâche 0494 " ATW0 "
    travail fait sur avion
    Texte tâche 0500 " ATQ0 "'''

    tlb = '''1st time occurence. Please reset indicator.
               To be monitored after next E/R and next flight.
               /* FRICKE Juergen - BLEMY - 08-Feb-2018 11:12 */
               #----------------------------------------------------#

               Clogging indicator reseted before flight n? 2
               /* CHAPUIS Jean-Pierre - QLAM - 26-Feb-2018 17:29 */

               Sub-task stamped
               /* CHAPUIS Jean-Pierre - QLAM - 26-Feb-2018 17:29 */
               #----------------------------------------------------#

               Clogging indicator checked after flight n?3 ( ferry flight from Chatauroux to toulouse)
               Nothing to report
               /* CHAPUIS Jean-Pierre - QLAM - 26-Feb-2018 17:31 */

               Sub-task stamped
               /* CHAPUIS Jean-Pierre - QLAM - 26-Feb-2018 17:31 */
               #----------------------------------------------------#

               Final Stamp
               /* CHAPUIS Jean-Pierre - QLAM - 26-Feb-2018 17:31 */'''
    print(c.clean(tlb))
    '''
    1st time occurence. Please reset indicator.
    To be monitored after next E/R and next flight.
    Clogging indicator reseted before flight n? 2
    Sub-task stamped
    Clogging indicator checked after flight n?3 ( ferry flight from Chatauroux to toulouse)
    Nothing to report
    Sub-task stamped
    Final Stamp'''
"""
import re


class Cleaner:
    """
    remove noise from text (SAP)
    """

    #: dictionnary of entity/regex
    _tags = {
        'SAP ARP': [
            # * 03.02.2017 11:55:08 CET MACHIN BIDULE (NGxyzEb) Tél. 33 xxxxxxxx  -
            re.compile(r'^\* \d{2}\.\d{2}\.\d{4} \d{2}\:\d{2}\:\d{2} CET .*$', re.MULTILINE),
        ],
        'SAP A-F': [
            #  01.06.2016 14:52:00 LESLIE LEPLAY (NG0D388) Tél. 33 228541016
            re.compile(r'^\s*\d{2}\.\d{2}\.\d{4} \d{2}\:\d{2}\:\d{2}.*$', re.MULTILINE),
            # reçu par LY le 20/03/17 ajout op 30
            re.compile(r'^reçu par [A-Z]* le \d{1,2}[\:\.\/]\d{1,2}[\:\.\/]\d{2,4}.*$', re.MULTILINE)
        ],
        'P-AEROTECH': [
            # * << 21.12.2017 13:14 0001 ORI0 GROTH, Marco (GROTH.MA) PQAC2
            re.compile(r'^[*] << \d{2}\.\d{2}\.\d{4} \d{2}\:\d{2}.*$', re.MULTILINE)
        ],
        'TLB': [
            re.compile(r'\/\*.*\*\/'),  # /* MACHIN Bidule - EVRT - 21-dec-2015 16:29 */
            re.compile(r'#\-*#')  # #----------------------------------------------------#
        ],
        'IRS': [],
        'FOLIO': [],
        'dates': [
            re.compile(r'\b\d{1,2}[\:\.\/]\d{1,2}[\:\.\/]\d{2,4}\b'),  # 12.12.2012, 3/4/2013
        ],
        'hours': [
            re.compile(r'\b\d{2}[\:h]\d{2}\b'),  # HH:MM, HHhMM
            re.compile(r'\b\d{2}\:\d{2}\:\d{2}\b'),  # HH:MM:SS
            re.compile(r'\b(utc|gmt)\s+\d{2}[\:h]?\d{2}\b', re.I),  # UTC HH:MM
            re.compile(r'\b\d{2}[\:h]?\d{1,2}\s*(utc|gmt)\b'),  # HH:MM UTC
        ],
        'punctuations': [
            # line only made of punctutation * --------------------------------------
            re.compile(r'^[\s\-\*_\+\#]*$', re.MULTILINE),
            # leading punctuation
            re.compile(r'^[\s\*\/\-]*', re.MULTILINE),
            # trailing punctuation
            re.compile(r'[\s\*\/\:]*$', re.MULTILINE)
        ]
    }

    def __init__(self):
        pass

    def clean(self, text, tag_types='all'):
        """
        Clean text based on regular expressions

        :param text: the text to parse
        :type text: str
        :param tag_types: name of the entity
        :type tag_types: str or list of str
        :return: cleaned text
        :rtype: str
        """

        types2process = tag_types
        if tag_types == 'all':
            types2process = self._tags.keys()

        for tag in types2process:
            tag_regex = self._tags[tag]
            for regex in tag_regex:
                text = re.sub(regex, '', text)

        return text

    def remove_punctuation_lines(self, text):
        """

        :param text:
        :return:
        """
        for regex in self._tags['punctuations']:
            text = re.sub(regex, '', text)
        return text


if __name__ == '__main__':
    c = Cleaner()

    textex = """1st time occurence. Please reset indicator.
               To be monitored after next E/R and next flight.
               /* FRICKE Juergen - BLEMY - 08-Feb-2018 11:12 */
               #----------------------------------------------------#

               Clogging indicator reseted before flight n? 2
               /* CHAPUIS Jean-Pierre - QLAM - 26-Feb-2018 17:29 */

               Sub-task stamped
               /* CHAPUIS Jean-Pierre - QLAM - 26-Feb-2018 17:29 */
               #----------------------------------------------------#

               Clogging indicator checked after flight n?3 ( ferry flight from Chatauroux to toulouse)
               Nothing to report
               /* CHAPUIS Jean-Pierre - QLAM - 26-Feb-2018 17:31 */

               Sub-task stamped
               /* CHAPUIS Jean-Pierre - QLAM - 26-Feb-2018 17:31 */
               #----------------------------------------------------#

               Final Stamp
               /* CHAPUIS Jean-Pierre - QLAM - 26-Feb-2018 17:31 */
"""

    print("\n\n\n")
    print(c.clean(textex))

    textex = '\nOFF\tP/N FE256-001\n S/N FR10388\nON \tP/N FE256-001\nS/N FR10742\nReplacement done iaw AMM  :\n52-12-14\nPlease refill damper IAW   AMM 52-10-00-600-802-A\nDischarging/charging of the door damper and emergency operation cylinder.\nCabin, door 2 RH, the door damper 360RH 4 has been re-filled up to the green zone before installation I.A.W   AMM 52-10-00-600-802A\nAfter the damper replacement, please reinstall the arm door lining of the door 2 RH\nCabin, door 2 LH, the arm door lining has been re-installed after installation of the door damper\nplease perform operational test of CIDS connection IAW AMM Subtask 52-12-14-710-050-B\nOperational test of CIDS connection   IAW AMM Subtask 52-12-14-710-050-B\n=>test ok'
    print(textex)
