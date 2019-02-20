"""
This module allows to access `Lexinet <http://airbushosting3.eu.airbus.corp:1080/Lexinet/eu/do_welcome>`_ abbreviations.


.. note:: This module requires Pandas.
"""
import os.path as pa

import pandas as pd


class Lexinet:

    def __init__(self):
        self.abbrvs = pd.read_csv(pa.join(pa.dirname(pa.abspath(__file__)),
                                          '..', 'data', 'lexinet_acronyms.csv.gz')).dropna()

    def get_full_form(self, acronym):
        """
        Get the meaning of an acronym

        :param acronym: acronym
        :type acronym: str
        :return: full form of the acronym
        :type: str or list of str
        :raise KeyError: if acronym not in Lexinet

        >>> from nlp4airbus.utils.lexinet import Lexinet
        >>> l = Lexinet()
        >>> l.get_full_form('ACMS')
        'Aircraft Condition Monitoring System'
        >>> l.get_full_form('CSC')
        ['Configured Spare Component', 'Cabin Safety Crew']
        """
        matching_rows = self.abbrvs.loc[self.abbrvs['Abbr'] == acronym, 'Full Form']
        if matching_rows.shape[0] == 0:
            raise KeyError
        elif matching_rows.shape[0] == 1:
            return matching_rows.iloc[0]
        else:
            return matching_rows.tolist()

    def get_all_acronyms(self):
        """
        Get the list of all acronyms. It is used in the :py:mod:`nlp4airbus.utils.stem`
        as a stemming black list.

        :return: All acronyms
        :rtype: list of str
        """
        return self.abbrvs['Abbr'].str.lower().unique().tolist()


if __name__ == '__main__':
    a = Lexinet()
    print(a.get_full_form('ACMS'))
    print(a.get_full_form('CSC'))
    print(a.get_full_form('IAW'))
    print(a.get_full_form('CDSS'))
    try:
        print(a.get_full_form('toto'))
    except KeyError:
        print('there is no toto in the acrnym list')
