# -*- coding: utf-8 -*-

from datetime import date
import pytest
import numpy as np
import pandas as pd
import pycocap as pyc


CASES_REF_DE = {
    date(2020, 1, 27): 1,
    date(2020, 1, 29): 0,
    date(2020, 3, 28): 6294,
}
DEATH_REF_DE = {
    date(2020, 1, 27): 0,
    date(2020, 3, 9): 2,
    date(2020, 3, 10): 0,
    date(2020, 4, 16): 315,
}
CASES_REF_UK = {
    date(2020, 1, 30): 0,
    date(2020, 1, 31): 2,
    date(2020, 2, 22): 0,
    date(2020, 4, 22): 5490,
}
DEATH_REF_UK = {
    date(2020, 1, 30): 1,
    date(2020, 3, 6): 1,
    date(2020, 3, 8): 0,
    date(2020, 4, 21): 1224,
}

def test_reports():
    df = pyc.reports('Germany', 'cases', params={'source_name': 'JHU'})
    print(df)
    for k in CASES_REF_DE:
        print(k)
        print(CASES_REF_DE[k])
        print(df[df['date'] == pd.to_datetime(k)]['cases'])
        assert(
            int(df[df['date'] == pd.to_datetime(k)]['cases']) == CASES_REF_DE[k]
        )

    df = pyc.reports('United Kingdom', 'cases')
    print(df[:10])
    print(df)
    for k in CASES_REF_UK:
        print(k)
        print(CASES_REF_UK[k])
        print(df[df['date'] == pd.to_datetime(k)]['cases'])
        assert(
            int(df[df['date'] == pd.to_datetime(k)]['cases']) == CASES_REF_UK[k]
        )

    # df = pyc.reports('Germany', 'death', params={'source_name': 'JHU'})
    # print(df)
    # for k in DEATH_REF_DE:
        # assert(
            # int(df[df['date'] == pd.to_datetime(k)]['death']) == DEATH_REF_DE[k]
        # )

    # df = pyc.reports('United Kingdom', 'death')
    # for k in DEATH_REF_UK:
        # assert(
            # int(df[df['date'] == pd.to_datetime(k)]['death']) == DEATH_REF_UK[k]
        # )

def test_date_cutting():
    start_date = date(2020, 8, 1)

    # start_date == end_date => excption
    with pytest.raises(Exception) as e_info:
        df = pyc.reports(
            'Sweden', 'cases', start_date=start_date, end_date=start_date
        )

    # 1 day corner case
    end_date = date(2020, 8, 2)
    df = pyc.reports(
        'Sweden', 'cases', start_date=start_date, end_date=end_date
    )
    assert(len(df) == 1)
    assert(df['date'][0] == pd.to_datetime(start_date))

    # expand timeseries to start_date & end_date
    start_date = date(2019, 1, 1)
    end_date = date(2024, 12, 31)
    df = pyc.cases(
        'Sweden', start_date=start_date, end_date=end_date, fill_value=0
    )
    assert(len(df) == (end_date - start_date).days)
    assert(df[df['date'] == pd.to_datetime(start_date)]['cases'][0] == 0)

def test_npi():
    SI_ref_de = {
        date(2020, 1, 21): np.nan,
        date(2020, 1, 22): 0.0,
        date(2020, 1, 24): 5.56,
        date(2020, 3, 22): 76.85,
    }
    df = pyc.npi('Germany', 'stringency')
    for k in SI_ref_de:
        si = df[df['date'] == pd.to_datetime(k)]['stringency'].iloc[0]
        if np.isnan(SI_ref_de[k]):
            assert(np.isnan(si))
        else:
            assert(
                si == SI_ref_de[k]
            )

def test_npis():
    df = pyc.npis(
        'Germany', ['school closing', 'dept relief', 'facial coverings']
    )
    assert(len(df.columns) == 4)
    # for k in si_ref_de:
        # si = df[df['date'] == pd.to_datetime(k)]['stringency'].iloc[0]
        # if np.isnan(si_ref_de[k]):
            # assert(np.isnan(si))
        # else:
            # assert(
                # si == si_ref_de[k]
            # )


if __name__ == '__main__':
    # test_reports()
    # test_date_cutting()
    test_npi()
    # test_npis()
