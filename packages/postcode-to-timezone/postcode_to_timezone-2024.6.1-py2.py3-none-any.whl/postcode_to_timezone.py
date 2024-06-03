import bisect
import functools
import json
import re


@functools.cache
def _country_regexes():
    with open('postcode_regex.json') as f:
        postcode_spec = json.load(f)
    return {
        spec['abbrev'].lower(): re.compile(f'^{spec["postal"]}$')
        for spec in postcode_spec
        if "postal" in spec  # Exclude countries without postal code
    }


def normalize_postcode(country_code: str, postcode: str, *, validate=False):
    if validate and len(country_code) != 2 or not country_code.isalpha():
        return None

    country_code = country_code.lower()
    postcode = postcode.lower()

    # Remove the leading country code if it's ther
    # Special case for the UK, which has postcodes that start with two letters.
    if postcode.startswith(country_code) and (country_code != 'gb'
                                              or len(postcode) > 8):
        postcode = postcode[2:]

    # Remove any leading/trailing whitespace or punctuation
    postcode = postcode.strip('-/ \t\n\r_')

    if validate:
        re_postcode = _country_regexes().get(country_code)
        if re_postcode is not None:
            # print(re_postcode)
            match = re_postcode.match(postcode)
            if match:
                postcode = match.group(0).lower()
            else:
                return None

    return "".join(filter(str.isalnum, postcode))


@functools.cache
def _postcodes_lookup():
    with open('postcodes-lookup.csv', 'rt') as f:
        return [tuple(line.split(',')) for line in f]


def get_tz(country_code: str, postcode: str) -> str | None:
    country_code = country_code.lower()
    postcode = normalize_postcode(country_code, postcode)

    lut = _postcodes_lookup()
    i = bisect.bisect_left(lut, (country_code, postcode, ''))
    if i != len(lut) and lut[i][0] == country_code:
        return lut[i][2]
    return None
