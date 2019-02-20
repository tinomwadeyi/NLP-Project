# -*- encoding: utf-8 -*-
"""This module implement the ``Entity`` class to retrieve some defined entities from the text based on regular
expressions. There are mostly Airbus/aeronautics entities.

Current list is:

============ ==================================================== ===================================================
Tag          Description                                          Matching string examples
============ ==================================================== ===================================================
PN           part number                                          ``PN 123543654``, ``V12345..``, ``F36874654``
SP           Standard Parts                                       ``NSA1234``, ``ABS125``, ``NAS156``
SN           serial number                                        ``S/N 2E2002933``
AM           AM                                                   ``AM 8993075``, ``AM 2205.1``
WO           word order                                           ``WO 51749769``
QLB          Quality Log Book                                     ``qlb 008``, ``eqlb 68``
OT           work ORDER                                           ``OT 4231386``
MPD          Maintenance Planning Document                        ``MPD Task 783141-210-042``
AMM_task     Aicraft Maintnenace Manuel                           ``AMM TASK 26-10-00-740-801-A``, ``AMM Task 49.00.00.860.801``
AMM          Aicraft Maintnenace Manuel                           ``AMM 531943-400-801``
TSM_task     Trouble Shooting Manual                              ``TSM TASK 26-23-00-810-833-A-``
TSM          Trouble Shooting Manual                              ``TSM 23-72-00-810-818-A``
PFR          Post Flight Report                                   ``PFR 4Y1792``
QSR          Quality Survey Report                                ``AF V EQ 16-00001, TH/V/EQ/14-00005``
Concession   Concession                                           ``TH-004335149``
NC           Non-Conformity                                       ``NC 000202975354``
related_wo   work order                                           ``1005037156``
GTI_RTI      ground and restest instrugmentation                  ``V0203TOE0040``
AMM_a350     AMM A350                                             ``A350-A-32-XX-XX-00001-240A-A, A350-A-35-11-56-00002-520A-A``
Paras                                                             ``VREL1200ULE0193L86RAT_IndA``
MCA          Major Component Assembly                             ``MCA 34080640900-TR1-000-A5``
FIN          Functional Item Number                               ``FIN 360RH7``
DWG          Drawing                                              ``DWG F521-70216-060-00``, ``Drw F521-70216-069-00``
AIPS         Airbus process specification: for A350
AIMS         AIPI: Airbus process instructions, for A350
Doc80        Doc80 is a family of document in docmaster
============ ==================================================== ===================================================


Example
-------

.. code:: python

    from nlp4airbus.re.entity import Entity

    text = '''Please refill damper360RH7 for RTO and first flight.
        Following TSM : 52-13-00-810-811-A
        Damper 360RH7 must be replaced.
                       /* LAPIERRE Olivier - AAA for QLA3 - 15-jun-2015 12:40 */

        On Door 4 LH, charging of the Door  Damper and Emergency Operation Cylinder performed IAW AMM TASK 52-10-00-600-802-A.
        Work performed with LE ROY A.
                       /* ORIOT Frédéric - AAA for BLLA3 - 15-jun-2015 13:22 */
                       #----------------------------------------------------#

        For spare ordering NC 13198106 created.
        Affected door-damper FIN 360RH7 P/N FE256-001 S/N FR9133 to be replaced i.a.w DWG F521-70216-060-00 sheet 21,15 and 09/ AMM Task 52-13-14-000-801-A removal, 52-13-14-400-801-A installation.

        Pressurisation and Operational Test of the CIDS Connection to be performed by FAL.
                       /* H.-H. Raguse / TP - TBALL1 - 15-jun-2015 16:33 */
                       #----------------------------------------------------#

                       Item status changed to HIL & crew accepted by
                       /* CORTES OCANA José - EVRT - 16-jun-2015 08:22 */'''
    e = Entity()
    print(e.extract(text, ['TSM', 'FIN', 'PN', 'DWG']))
    # {'TSM': [('TSM', '52-13-00-810-811-A')], 'FIN': [('FIN', '360RH7')], 'PN': [('P/N', 'FE256-001')], 'DWG': [('DWG', 'F521-70216-060-00')]}
"""
import re


class Entity:
    """
    class to retrieve diverse Airbus entities in free text
    """

    #: dictionnary of entity/regex
    _entities = {
        'AIPS': r'\b(AIPS)\s*([A-Z0-9\-]*)',  # AIPS: Airbus process specification: for A350
        'AIMS': r'\b(AIMS)\s*([A-Z0-9\-]*)',  # AIPI: Airbus process instructions, for A350
        'Doc80': r'(80)[\s]*([A-Z0-9\-]*)',  # Doc80 is a family of document in docmaster (for A320 i think)
        'PNFV': r'\b((P\/*N)|V|F)\s*([A-Z0-9\-]+)\b',  # PN for part number: PN 123543654 or V12345.. or F36874654
        'PN': r'\b(P\/*N|part number)\s*([\w\-]+)\b',  # PN for part number: PN 123543654 or V12345.. or F36874654
        'SP': r'\b(ASN|NSA|ABS|EN)[\s]*([A-Z0-9\-]*)',  # SP is for standard parts: NSA1234, ABS125, NAS156...
        'SN': r'\b(S\/*N|serial number)[\s:]*(\w+)\b',  # serial number S/N 2E2002933
        'AM': r'\b(AM)[:\s]+([\.\w]+)',  # AM 8993075
        'WO': r'\b(WO)[\:\s]*(\d+)\b',  # word order WO 51749769
        'QLB': r'\b([e]?qlb)[\:\s]*([\w\-]+)\b',  # QLB
        'OT': r'\b(OT)\s*([0-9]*)\b',  # work ORDER OT 4231386
        'MPD': r"\bmpd\s+task\s+([\w\-]{4,})\b",  # MPD Task 783141-210-042
        'AMM_task': r"\b(AMM\s+task)\s+(\d[\w\-\.]{4,})\b",  # AMM TASK 26-10-00-740-801-A, AMM Task 49.00.00.860.801
        'AMM': r"\bamm[\:\s]*(\d[\w\-]{4,})\b",  # AMM 531943-400-801, AMM:79-21-11-210-801
        'TSM_task': r"\btsm\s+task\s+([\w\-]{4,})\b",  # TSM TASK 26-23-00-810-833-A-
        'TSM': r"\b(TSM)[\s:]+([\w\-]{4,})\b",  # TSM 23-72-00-810-818-A
        'PFR': r'\b(PFR)\s*([0-9]\w+)\b',  # PFR 4Y1792
        'QSR': r'(\w{2}|ROH|AIB)\WV\W[a-zA-Z]{2}\W.{8}',  # AF V EQ 16-00001, TH/V/EQ/14-00005
        'Concession':  r'\w{2,3}-\d{9}',  # TH-004335149
        'NC': r'\b(NC|REJ)\s*(\d+)\b',  # NC 000202975354
        'related_wo': r'(100|00100)\d{7}',  # 1005037156
        'GTI_RTI': r'(?i)v[a-z0-9]{11}',  # V0203TOE0040
        'AMM_a350': r'(?i)a350-\w-\S*',  # A350-A-32-XX-XX-00001-240A-A, A350-A-35-11-56-00002-520A-A
        'Paras': r'(?i)(?<=para).\S*',  # VREL1200ULE0193L86RAT_IndA
        'MCA': r'\b(MCA)\s*(\d{11}\-\w{3}-\d{3}[\-\s]A\d)',  # Major Component Assembly MCA 34080640900-TR1-000-A5
        'FIN': r'\b(FIN)\s*(\w+)\b',  # FIN 360RH7
        'DWG': r'\b(DWG|DRW)\s*([\w\-]+)\b',  # DWG F521-70216-060-00, Drw F521-70216-069-00
    }

    def __init__(self):
        pass

    def get_regex(self, entity_type):
        """
        Get the regex pattern corresponding to a given entity

        :param entity_type: name of the entity
        :type entity_type: str
        :return: matching entity string
        :rtype: str
        """
        return self._entities[entity_type]

    def extract(self, text, entity_type, ignore_case=True):
        """
        get all entities from a given text

        :param text: the text to parse
        :type text: str
        :param entity_type: (list of) entity(ies)
        :type entity_type: str or list of str
        :param ignore_case: Ignore case?
        :type ignore_case: bool
        :return: list of entities
        :rtype: list of str
        :raise TypeError: if entity type is neither a string or a list of strings
        :raise KeyError: if entity is not known

        >>> from nlp4airbus.re.entity import Entity
        >>> e = Entity()
        >>> e.extract('manufacturing PN F521-81204 (Door Skins) for the A330 Doors (PN F521-71401 \
                            and F521-71402) and the material call out is AIMS 0304012 which is purchased in the –O- Condition','PN')
        [('PN', 'PN', 'F521-81204'), ('PN', 'PN', 'F521-71401'), ('F', '', '521-71402')]

        >>> e.extract('In Issue 7 of ABS 1707 the blind fasteners and solid rivets were in one column and there was the needed code: 03 defined.','SP')
        [('ABS', '1707')]
        """

        # single request
        if isinstance(entity_type, str):
            if entity_type not in self._entities:
                raise KeyError('Unknwon entity %s. Should be in %s' % (entity_type, str(self._entities.keys())))
            if ignore_case:
                reg_c = re.compile(self._entities[entity_type], re.I)
            else:
                reg_c = re.compile(self._entities[entity_type])
            return reg_c.findall(text)

        # several types
        elif isinstance(entity_type, list):
            entities = {}
            for entity in entity_type:
                if entity not in self._entities:
                    raise KeyError('Unknwon entity %s.  Should be in %s' % (entity, str(self._entities.keys())))

                if ignore_case:
                    reg_c = re.compile(self._entities[entity], re.I)
                else:
                    reg_c = re.compile(self._entities[entity])
                entities[entity] = reg_c.findall(text)
            return entities

        else:
            raise TypeError('Unknwon type for entity_type')


if __name__ == '__main__':
    # import doctest
    # doctest.testmod()

    e = Entity()
    foo = e.extract('manufacturing PN F521-81204 (Door Skins) for the A330 Doors (PN F521-71401 \
                           and F521-71402) and the material call out is AIMS 0304012 which is purchased in the –O- Condition','PN',
                    ignore_case=False)
    print(foo)

    foo = e.extract('In Issue 7 of ABS 1707 the blind fasteners and solid rivets were in one column and there was the needed code: 03 defined.','SP')
    print(foo)

    foo = e.extract("""TSM 24-00-00-810-933-A applied.
No Fault detected.
               /* LAMELA Alain - BLLA321 - 23-jun-2015 13:56 */
               #----------------------------------------------------#

This message has been trigerred due to an electrical transient detected by DMCs during GEN tests. 
Please perform DMC bite test. if the test is ok no further action will be needed on A/C.
               /* PEREZ Edouard - BLENM3 - 23-jun-2015 17:42 */

Bite test of  DMC 1,2 and 3   performed iaw AMM TASK 31-60-00-740-801 --> test OK.
               /* BOUKEFFA Nassim - BLLA321 - 23-jun-2015 23:32 */
               #----------------------------------------------------#

               Final Stamp
               /* BORDOT David - BLLAQ3 - 24-jun-2015 00:23 */

               Crew accept
               /* MACHU Eric - EVRT - 24-jun-2015 07:59 */""", 'TSM')
    print(foo)

    foo = e.extract("""PFR  4Y04KA

FMGEC1(1CA1) AP ENG COW DISCRETE
UTC:09:37 - ATA:228334 - Source:AFS - HARD - Ph:06 - Class:1
FAILURE MESSAGE
               /* BERTRAND Christophe - EVRT - 23-feb-2018 12:24 */""", 'PFR')
    print(foo)

    foo = e.extract("""TSM applied following AMM task 28-46-00-810-822-A
               
               FCMS  Level sense Test applied following AMM task 28-51-00-710-802-A .
               
               TEST ==> OK
               
                   BLANC VALENTIN TO114311 &
               /* LAMELA Alain - BLLA321 - 05-Oct-2016 23:16 */
               #----------------------------------------------------#

               Please attach PFR and FCMC 1&2 TSD.
               /* RIDGE Jerry - BLEMY - 06-Oct-2016 08:38 */
               #----------------------------------------------------#

               See in attached files PFR and TSD message of FCMC 1&2.
               /* RENARD Didier - BLLA3 - 06-Oct-2016 09:30 */
               #----------------------------------------------------#

               As Level Sense Test OK TSD Shows this as a Spurious Indication, associated with power switching, displayed at Engine Start which is a known issue. 
               No further maintenance action required.
               /* RIDGE Jerry - BLEMY - 06-Oct-2016 10:09 */
               #----------------------------------------------------#

               Final Stamp
               /* CRACHET Jérôme - QLAM - 06-Oct-2016 10:20 */

               Crew accept
               /* REN Zidan - EVRT - 06-Oct-2016 10:46 */""", 'AMM_task')
    print(foo)


    foo = e.extract("""INSPECTION BEFORE ENGINE RUN-UP PERFORMED IAW MCA34080645100-TR1-000-A1.
               /* CRACHET J?r?me - QLA - 16-Jun-2017 08:31 */
               #----------------------------------------------------#

               Final Stamp
               /* CRACHET J?r?me - QLA - 16-Jun-2017 08:31 */

               Crew accept
               /* GARCIA Eric - EVRT - 20-Jun-2017 09:23 */""", 'MCA')
    print(foo)

    foo = e.extract("""INSPECTION POST FIRST FLIGHT HAS BEEN CARRIED OUT IAW MCA 34080640900-TR1-000-A5.
               /* BRUNEL Pierre-Marie - QLA - 03-Jul-2017 13:26 */
               #----------------------------------------------------#

               Final Stamp
               /* BRUNEL Pierre-Marie - QLA - 03-Jul-2017 13:26 */

               Crew accept
               /* ALVAREZ-TOLEDO Agustin - EVRA - 03-Jul-2017 13:27 */""", 'MCA')
    print(foo)

    toto = """Please refill damper360RH7 for RTO and first flight.
Following TSM : 52-13-00-810-811-A
Damper 360RH7 must be replaced.
               /* LAPIERRE Olivier - AAA for QLA3 - 15-jun-2015 12:40 */

On Door 4 LH, charging of the Door  Damper and Emergency Operation Cylinder performed IAW AMM TASK 52-10-00-600-802-A.
Work performed with LE ROY A.
               /* ORIOT Frédéric - AAA for BLLA3 - 15-jun-2015 13:22 */
               #----------------------------------------------------#

For spare ordering NC 13198106 created.
Affected door-damper FIN 360RH7 P/N FE256-001 S/N FR9133 to be replaced i.a.w DWG F521-70216-060-00 sheet 21,15 and 09/ AMM Task 52-13-14-000-801-A removal, 52-13-14-400-801-A installation. 

Pressurisation and Operational Test of the CIDS Connection to be performed by FAL.
               /* H.-H. Raguse / TP - TBALL1 - 15-jun-2015 16:33 */
               #----------------------------------------------------#

               Item status changed to HIL & crew accepted by
               /* CORTES OCANA José - EVRT - 16-jun-2015 08:22 */"""
    print(e.extract(toto, ['TSM', 'FIN', 'PN', 'DWG']))

    sn = """JOB CARD EQUIPMENT CHANGED

REPLACEMENT
FIN	1WW1
FWC
ATA	31
OFF	P/N LA2E20202T60000
	S/N 2E2002949
ON	P/N LA2E20202T50000
	S/N 2E2002942
Replacement done iaw AMM Task:
31-53-34 PB 401
               /* ESTARLIE Pierre - BLLA321 - 26-jan-2016 19:07 */
Tests done iaw AMM Task:
31-50-00-740-801test of the FWS==> test OK
22-97-00-740-801the LAND CAT 3 capability test ==> test OK  
               /* ESTARLIE Pierre - BLLA321 - 26-jan-2016 19:10 */

REPLACEMENT
FIN	1WW2
FWC
ATA	31
OFF	P/N LA2E20202T60000
	S/N 2E2002962
ON	P/N LA2E20202T50000
	S/N 2E2002933
Replacement done iaw AMM Task:
31-53-34 PB 401
               /* ESTARLIE Pierre - BLLA321 - 26-jan-2016 19:12 */
Tests done iaw AMM Task:
31-50-00-740-801test of the FWS==> test OK
22-97-00-740-801the LAND CAT 3 capability test ==> test OK  
               /* ESTARLIE Pierre - BLLA321 - 26-jan-2016 19:12 */
               #----------------------------------------------------#

               Final Stamp
               /* KERVADEC Lionel - BLLAQ3 - 26-jan-2016 23:32 */

               Crew accept
               /* GILARD Thierry - EVRT - 28-jan-2016 09:18 */"""
    print(e.extract(sn, ['SN', 'PN', 'FIN']))

    dwg = """For spare parts order NC 13943262 created. ODD probably on the first of February.
The affected cover must be replaced in accordance with DWG F523-70900-006, observing notes <1> and <4>.
               /* H.-H. Raguse / Prod / TL  - BLL4 - 31-Jan-2018 09:09 */

               IC 1852-272
               Acces cover assy (F523-70730-018) replaced iaw F523-70900/1-002
               /* MARTINI S?bastien - BLL421 - 01-Feb-2018 08:58 */

               Sub-task stamped
               /* ROUVRE Marceau - TRIGO QUALITAIRE for BBL4 - 01-Feb-2018 08:58 */
               #----------------------------------------------------#

               Final Stamp
               /* MURRAY Ian - QLAM - 01-Feb-2018 17:18 */

               /* GENSCH Thomas - QLA3 - 01-Feb-2018 18:11 */

               Crew accept
               /* CANALE  Bruno - EVRT - 05-Feb-2018 09:36 */"""
    print(e.extract(dwg, 'DWG'))

    wo = """APU fuel filter and APU oil filter inspected IAW WO 51749769 & 51749769.
               Work done with RUIZ M. (AAA TEAM)
               /* ORIOT Fr?d?ric - AAA for BLLA3 - 26-Jun-2017 15:35 */

               Sub-task stamped
               /* CAROLLO Jean-Marie - AAA for QLA3 - 26-Jun-2017 17:58 */
               #----------------------------------------------------#

Please perform APU run for leak check.
               /* PAUTRIC J?rome - QLA31 - 26-Jun-2017 17:10 */

               APU Start performed following AMM Task 49.00.00.860.801.
               /* FRIEDERICH Luc - QLA - 26-Jun-2017 19:15 */
               #----------------------------------------------------#

Please perform fuel and oil leak check
               /* FRIEDERICH Luc - QLA - 26-Jun-2017 19:16 */

               Fuel and oil  leack check performed and satisfactory .No anomaly found
               /* CAROLLO Jean-Marie - AAA for QLA3 - 26-Jun-2017 19:21 */

               Sub-task stamped
               /* CAROLLO Jean-Marie - AAA for QLA3 - 26-Jun-2017 19:21 */
               #----------------------------------------------------#

               Final Stamp
               /* CAROLLO Jean-Marie - AAA for QLA3 - 26-Jun-2017 19:22 */

               Crew accept
               /* DEBOURBE Jean-Pascal - EVRT - 27-Jun-2017 10:03 */"""
    print(e.extract(wo, ['WO', 'AMM_task']))

    qlb = """Launch an AM
               /* CHAPUIS Jean-Pierre - QLAM - 29-Nov-2017 12:17 */

               See AM 8993075
               /* CHAPUIS Jean-Pierre - QLAM - 29-Nov-2017 12:18 */

               Sub-task stamped
               /* CHAPUIS Jean-Pierre - QLAM - 29-Nov-2017 12:18 */
               #----------------------------------------------------#

Please perform dresse back following MAP answer in the qlb 008
               /* MESLIER S?bastien - QLA31 - 01-Dec-2017 15:08 */

               FI 296 closed 
               Dress back performed by CASTAING TO 96730 AV 96730,
               New value: +0.09 mm
               /* MESLIER S?bastien - QLA31 - 01-Dec-2017 15:11 */

               Sub-task stamped
               /* MESLIER S?bastien - QLA31 - 01-Dec-2017 15:11 */
               #----------------------------------------------------#

Please peform NDT after rework
               /* MESLIER S?bastien - QLA31 - 01-Dec-2017 15:13 */

               NDT performed after rework. ( see result in attached file ).
               No cracks found inside and outside aircraft.
               Following AM 2205.1, it's a dent classified to class 1.
               /* MESLIER S?bastien - QLA31 - 01-Dec-2017 15:33 */

               Sub-task stamped
               /* MESLIER S?bastien - QLA31 - 01-Dec-2017 15:33 */
               #----------------------------------------------------#

Please to install the floor panel
               /* MESLIER S?bastien - QLA31 - 01-Dec-2017 15:34 */

               FLOOR PANEL REINSTALLED
               /* CASSAGNE Jean-Pierre - BLLA3 - 04-Dec-2017 09:17 */

               Sub-task stamped
               /* MESLIER S?bastien - QLA31 - 04-Dec-2017 10:10 */
               #----------------------------------------------------#

               Final Stamp
               /* MESLIER S?bastien - QLA31 - 04-Dec-2017 10:11 */

               Crew accept
               /* ROUZEVAL Mathieu - EVRT - 05-Dec-2017 11:13 */"""
    print(e.extract(qlb, ['AM', 'QLB']))

    amm = """IC:31228
Inspection of the MCD performed on both engines i.a.w. AMM:79-21-11-210-801.
No findings to report.Engines serviceable.
               /* GSELL Guy - CFM - 16-mar-2015 20:38 */
               Sub-task stamped
               /* GSELL Guy - CFM - 16-mar-2015 20:39 */
               #----------------------------------------------------#

Airbus to perform a minimum idle leak check per AMM:71-00-00-720-811
               /* GSELL Guy - CFM - 16-mar-2015 20:39 */

IDLE Run performed iaw GTG procedure
Please perform leak check
               /* KERVADEC Lionel - BLLAQ3 - 19-mar-2015 15:16 */
               #----------------------------------------------------#


after idle, leak check performed on MCD on both engines.
No leaks found
               /* MESLIER Sébastien - QLA31 - 19-mar-2015 15:26 */
               #----------------------------------------------------#

               Final Stamp
               MESLIER Sébastien - QLA31 - 19-mar-2015 15:26
               Crew accept
               /* ALVAREZ-TOLEDO Agustin - EVRA - 19-mar-2015 16:09 */"""
    print(e.extract(amm, 'AMM'))
