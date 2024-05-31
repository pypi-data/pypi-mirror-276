# Country Mapper

The country mapper is a Python package to map and match
country names between different classifications and between different
naming versions. Internally it uses regular expressions to match country
names.


## Motivation

It's very difficult to standardise country names when inputs differ at every turn for every 
country, for instance some may write US/ USA/ America, there has to be a way to map all
these variations (including common spelling mistakes) to one naion, thus standarising the 
country names.

Addressing this challenge, the Country Mapper streamlines the process of 
converting between different naming conventions and versions of country names. Country Mapper
operates on a database that maps various ISO and UN standards to each country, alongside 
its official name and a regular expression designed to capture all English versions 
of the country name.


## Installation

countrymapper is registered at PyPI. From the command line:

    pip install countrymapper --upgrade


Alternatively, the source code is available on
[GitHub](https://github.com/shaikharfat/countrymapper).

The package depends on [Pandas](http://pandas.pydata.org/); for testing
[pytest](http://pytest.org/) is required.

## Usage

### Basic usage

#### Use within Python

Convert various country names to some standard names:

``` python
import countrymapper as coco
some_names = ["(1) Lebanon (2) Syria", "COLOMBIA; MEXICO", "Czech", "Philippine", "UK"]
standard_names = coco.convert(names=some_names, to='name_short')
print(standard_names)
```

Which results in \[['Lebanon', 'Syria'], ['Colombia', 'Mexico'], 'Czechia', 'Philippines',
'United Kingdom'].The input format is determined automatically, based on ISO two letter, ISO
three letter, ISO numeric or regular expression matching. In case of any
ambiguity, the source format can be specified with the parameter 'src'.



In order to more efficiently convert Pandas Series, the `pandas_convert()` method can be used. The
performance gain is especially significant for large Series. For a series containing 1 million rows
a 4000x speedup can be achieved, compared to `convert()`.

``` python
import countrymapper as coco
import pandas as pd
cc = coco.countrymapper()

some_countries = pd.Series(['Australia', 'Belgium', 'Brazil', 'Bulgaria', 'Cyprus', 'Czech Republic',
                  'Guatemala', 'Mexico', 'Honduras', 'Costa Rica', 'Colombia', 'Greece', 'Hungary',
                  'India', 'Indonesia', 'Ireland', 'Italy', 'Japan', 'Latvia', 'Lithuania',
                  'Luxembourg', 'Malta', 'Jamaica', 'Ireland', 'Turkey', 'United Kingdom',
                  'United States'], name='country')
 
iso3_codes = cc.pandas_convert(series=some_countries, to='ISO3')                  
```

Convert between classification schemes:

``` python
iso3_codes = ['USA', 'VUT', 'TKL', 'AUT', 'XXX' ]
iso2_codes = coco.convert(names=iso3_codes, to='ISO2')
print(iso2_codes)
```

Which results in \['US', 'VU', 'TK', 'AT', 'not found'\]

The not found indication can be specified (e.g. not_found = 'not
there'), if None is passed for 'not_found', the original entry gets
passed through:

``` python
iso2_codes = coco.convert(names=iso3_codes, to='ISO2', not_found=None)
print(iso2_codes)
```

results in \['US', 'VU', 'TK', 'AT', 'XXX'\]

Internally the data is stored in a Pandas DataFrame, which can be
accessed directly. For example, this can be used to filter countries for
membership organisations (per year). Note: for this, an instance of
countrymapper is required.

``` python
import countrymapper as coco
cc = coco.countrymapper()

some_countries = ['Australia', 'Belgium', 'Brazil', 'Bulgaria', 'Cyprus', 'Czech Republic',
                  'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary',
                  'India', 'Indonesia', 'Ireland', 'Italy', 'Japan', 'Latvia', 'Lithuania',
                  'Luxembourg', 'Malta', 'Romania', 'Russia', 'Turkey', 'United Kingdom',
                  'United States']

oecd_since_1995 = cc.data[(cc.data.OECD >= 1995) & cc.data.name_short.isin(some_countries)].name_short
eu_until_1980 = cc.data[(cc.data.EU <= 1980) & cc.data.name_short.isin(some_countries)].name_short
print(oecd_since_1995)
print(eu_until_1980)
```

All classifications can be directly accessed by:

``` python
cc.EU28
cc.OECD

cc.EU27as('ISO3')
```

and the classification schemes available:

``` python
cc.valid_class
```

There is also a method for only getting country classifications (thus
omitting any grouping of countries):

``` python
cc.valid_country_classifications
```

If you rather need a dictionary describing the classification/membership
use:

``` python
import countrymapper as coco
cc = coco.countrymapper()
cc.get_correspondence_dict('EXIO3', 'ISO3')
```

to also include countries not assigned within a specific classification
use:

``` python
cc.get_correspondence_dict('EU27', 'ISO2', replace_nan='NonEU')
```

The regular expressions can also be used to match any list of countries
to any other. For example:

``` python
match_these = ['norway', 'united_states', 'china', 'taiwan']
master_list = ['USA', 'The Swedish Kingdom', 'Norway is a Kingdom too',
               'Peoples Republic of China', 'Republic of China' ]

matching_dict = coco.match(match_these, master_list)
```

Country mapper by default provides a warning to the python <span
class="title-ref">logging</span> logger if no match is found. The
following example demonstrates how to configure the <span
class="title-ref">coco</span> logging behaviour.

``` python
import logging
import countrymapper as coco
logging.basicConfig(level=logging.INFO)
coco.convert("asdf")
# WARNING:countrymapper.countrymapper:asdf not found in regex
# Out: 'not found'

coco_logger = coco.logging.getLogger()
coco_logger.setLevel(logging.CRITICAL)
coco.convert("asdf")
# Out: 'not found'
```


#### Command line usage

The country mapper package also provides a command line interface
called coco.

Minimal example:

    coco Cyprus DE Denmark Estonia 4 'United Kingdom' AUT

Converts the given names to ISO3 codes based on matching the input to
ISO2, ISO3, ISOnumeric or regular expression matching. The list of names
must be separated by spaces, country names consisting of multiple words
must be put in quotes ('').

The input classification can be specified with '--src' or '-s' (or will
be determined automatically), the target classification with '--to' or
'-t'.

The default output is a space separated list, this can be changed by
passing a separator by '--output_sep' or '-o' (e.g -o '\|').

Thus, to convert from ISO3 to UN number codes and receive the output as
comma separated list use:

    coco AUT DEU VAT AUS -s ISO3 -t UNcode -o ', '

The command line tool also allows to specify the output for none found
entries, including passing them through to the output by passing None:

    coco CAN Peru US Mexico Venezuela UK Arendelle --not_found=None

and to specify an additional data file which will overwrite existing
country matching

    coco Congo --additional_data path/to/datafile.csv




#### Use in Matlab

Newer (tested in 2016a) versions of Matlab allow to directly call Python
functions and libraries. This requires a Python version \>= 3.4
installed in the system path (e.g. through Anaconda).

To test, try this in Matlab:

``` matlab
py.print(py.sys.version)
```

If this works, you can also use coco after installing it through pip (at
the windows commandline - see the installing instruction above):

``` matlab
pip install countrymapper --upgrade
```

And in matlab:

``` matlab
coco = py.countrymapper.countrymapper()
countries = {'The Swedish Kingdom', 'Norway is a Kingdom too', 'Peoples Republic of China', 'Republic of China'};
ISO2_pythontype = coco.convert(countries, pyargs('to', 'ISO2'));
ISO2_cellarray = cellfun(@char,cell(ISO2_pythontype),'UniformOutput',false);
```

Alternatively, as a long oneliner:

``` matlab
short_names = cellfun(@char, cell(py.countrymapper.convert({56, 276}, pyargs('src', 'UNcode', 'to', 'name_short'))), 'UniformOutput',false);
```

All properties of coco as explained above are also available in Matlab:

``` matlab
coco = py.countrymapper.countrymapper();
coco.EU27
EU27ISO3 = coco.EU27as('ISO3');
```

These functions return a Pandas DataFrame. The underlying values can be
access with .values (e.g.

``` matlab
EU27ISO3.values
```

I leave it to professional Matlab users to figure out how to further
process them.


### Building concordances for country aggregation

Coco provides a function for building concordance vectors, matrices and
dictionaries between different classifications. This can be used in
python as well as in matlab. 

## Classification schemes

Currently the following classification schemes are available (see also
Data sources below for further information):

1.  ISO2 (ISO 3166-1 alpha-2) - including UK/EL for Britain/Greece (but always convert to GB/GR)
2.  ISO3 (ISO 3166-1 alpha-3)




## Acknowledgements

This package was inspired by Konstantin Stadler's (https://github.com/IndEcol/country_converter).
