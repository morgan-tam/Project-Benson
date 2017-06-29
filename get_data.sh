#!/bin/bash
#
# A shell script to download and save the MTA data and metadata to files.
#
set -e
set -u
set -o pipefail

mkdir -p Metadata
cd Metadata
curl -O http://web.mta.info/developers/resources/nyct/subway/StationEntranceDefinitions.csv 
curl -O http://web.mta.info/developers/data/nyct/subway/StationEntrances.csv
curl -O http://web.mta.info/developers/resources/nyct/turnstile/ts_Field_Description.txt
curl -O http://web.mta.info/developers/data/nyct/subway/Stations.csv
cd ../

mkdir -p data_mta
cd data_mta
# See http://web.mta.info/developers/turnstile.html
# generally of the form
# http://web.mta.info/developers/data/nyct/turnstile/turnstile_170624.txt
week_number_list="160604 160611 160618 160625 160702 160709 160716 160723 160730 160806 160813 160820 160827 160903 160910 160917 160924"

base_url="http://web.mta.info/developers/data/nyct/turnstile/turnstile_"
for n in ${week_number_list}; do
    url="${base_url}${n}.txt"
    [[ -e ${url##*/} ]] || curl -O $url
done

