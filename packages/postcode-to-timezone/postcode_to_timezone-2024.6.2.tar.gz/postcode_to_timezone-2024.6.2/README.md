# Postcode to Timezone

Example:

```python
from postcode_to_timezone import postcode_to_timezone

postcode_to_timezone('NL', '1234 AB')
```

return `'Europe/Amsterdam'`

## Sources

### `location_postcode.csv.xz`

A dump of the location_postcode table in a Nominatim database. Nominatim creates this database from OpenStreetMap data using the following query:

```sql
SELECT
    COALESCE(plx.country_code, get_country_code(ST_Centroid(pl.geometry))) as country_code,
    pl.address->'postcode' as postcode,
    COALESCE(plx.centroid, ST_Centroid(pl.geometry)) as geometry
  FROM place AS pl
  LEFT OUTER JOIN placex AS plx
         ON pl.osm_id = plx.osm_id AND pl.osm_type = plx.osm_type
WHERE 
	pl.address ? 'postcode'
	AND pl.geometry IS NOT null
```

### postcode_regex.json

Obtained from [GitHub Gist](https://gist.githubusercontent.com/lkopocinski/bd4494588458f5a8cc8ffbd12a4deefd/raw/6bc84f50091852ecfa0ee6ea4b506cabcea1cc52/postal_codes_regex.json). Actual source not known.

