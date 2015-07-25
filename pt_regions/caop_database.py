"""
 This module converts 3 TSV files of districts, municipalities and counties into
 a dictionaries. Use `get_districts`, `get_municipalities`, `get_counties`.

 This module uses the database from
 http://www.dgterritorio.pt/cartografia_e_geodesia/cartografia/carta_administrativa_oficial_de_portugal__caop_/caop_em_vigor/
 specifically from the excel file
 http://www.dgterritorio.pt/ficheiros/cadastro/caop/caop_download/caop_2014_0/areasfregmundistcaop2014_3

 which:
 1. each sheet was exported to TSV via "save as..." "UTF-16 Unicode Text" in excel.
 2. each sheet was converted to utf-8 via a text program.
 3. each sheet was saved in
 * `Areas_distritos_CAOP2014_utf8.txt`
 * `Areas_municipios_CAOP2014_utf8.txt`
 * `Areas_freguesias_CAOP2014_utf8.txt`
"""
import csv

from .auxiliar import cache, DATA_PATH, NUMBER_OF_DISTRICTS, \
    NUMBER_OF_MUNICIPALITIES, NUMBER_OF_COUNTIES


def _get_districts():
    with open(DATA_PATH + 'Areas_distritos_CAOP2014_utf8.txt', 'r') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        tsvin = list(tsvin)[1:]  # ignore first line

        count = 0
        for line in tsvin:
            if line[0] == line[1] == '':
                break
            count += 1
        assert(count == NUMBER_OF_DISTRICTS)
        tsvin = tsvin[:count]

        results = []
        for line in tsvin:
            results.append({
                'COD': line[0],
                'name': line[2],
                'area': int(line[3].replace(',', ''))}
            )

    assert(len(results) == NUMBER_OF_DISTRICTS)
    return results


@cache('caop_districts_normalized.json')
def get_districts():
    districts = _get_districts()
    assert(len(districts) == NUMBER_OF_DISTRICTS)
    return districts


def _get_municipalities():
    districts = get_districts()

    with open(DATA_PATH + 'Areas_municipios_CAOP2014_utf8.txt', 'r') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        tsvin = list(tsvin)[1:]  # ignore first line

        count = 0
        for line in tsvin:
            if line[0] == line[1] == '':
                break
            count += 1
        assert(count == NUMBER_OF_MUNICIPALITIES)
        tsvin = tsvin[:count]

        results = []
        for line in tsvin:
            result = {
                'COD': line[0],
                'name': line[5],
                'area': int(line[6].replace(',', ''))}

            # create relation with district
            try:
                district = next(district for district in districts
                                if district['name'] == line[4])
            except StopIteration:
                raise IndexError("District not found")

            result['district_COD'] = district['COD']
            result['district_name'] = district['name']

            results.append(result)

    assert(len(results) == NUMBER_OF_MUNICIPALITIES)
    return results


@cache('caop_municipalities_normalized.json')
def get_municipalities():
    municipalities = _get_municipalities()
    assert(len(municipalities) == NUMBER_OF_MUNICIPALITIES)
    return municipalities


def _get_counties():
    municipalities = get_municipalities()
    districts = get_districts()

    # create an inverted index NAME->district
    districts_index = dict()
    for d in districts:
        assert(d['name'] not in districts_index)
        districts_index[d['name']] = d

    with open(DATA_PATH + 'Areas_freguesias_CAOP2014_utf8.txt', 'r') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        tsvin = list(tsvin)[1:]  # ignore first line

        count = 0
        for line in tsvin:
            if line[0] == line[1] == '':
                break
            count += 1
        assert(count == NUMBER_OF_COUNTIES)
        tsvin = tsvin[:count]

        results = []
        for line in tsvin:
            assert(len(line) == 10)
            result = {
                'COD': line[0],
                'name': " ".join(line[6].split()),
                'area': int(line[7].replace(',', ''))}

            # build relation
            district = districts_index[line[4]]
            try:
                municipality = next(municipality for municipality in municipalities
                                    if municipality['name'] == line[5] and
                                    municipality['district_COD'] == district['COD'])
            except StopIteration:
                raise IndexError("Municipality not found")

            result['municipality_COD'] = municipality['COD']
            result['municipality_name'] = municipality['name']
            result['district_name'] = district['name']

            results.append(result)

    assert(len(results) == NUMBER_OF_COUNTIES)
    return results


@cache('caop_counties_normalized.json')
def get_counties():
    counties = _get_counties()
    assert(len(counties) == NUMBER_OF_COUNTIES)
    return counties


if __name__ == '__main__':
    get_districts(flush=True)
    get_municipalities(flush=True)
    get_counties(flush=True)
