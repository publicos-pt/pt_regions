This package contains a complete list of Local Administrative Units (LAUs) of Portugal:
municipalities (municípios, LAU 1) and counties (freguesias, LAU 2), along 
with their fiscal number (NIF).

It also contains the scripts used to build this list from the official sources: 

1. The official database of regions (districts, municipalities, counties)
2. The database of counties administrations (portal autárquico)
3. The official database of public institutions (Banco de Portugal)

The main problem this package solves is the mismatch between the names on the above databases.
We kept the names from the official database of regions, since it uses the names set by law.

This package has 2 functions: 

* `municipalities()` returns the list of dictionaries with the municipalities.
* `counties()` returns a list of dictionaries with the counties.

Both lists are available in json in this package.
