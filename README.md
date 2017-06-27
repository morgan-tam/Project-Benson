
## Project Benson
# Problem Statement

**OBJECTIVE**
Women Tech Women Yes (WTWY) is hosting a fundraising Gala on Sep 26, 2017. 
They would like us help them identify optimal times and locations to deploy their subway canvassing team in order to maximize ticket purchases for the gala.

**ASSUMPTIONS and DISCLAIMERS**
WTWY
- Gala is on Sep 26, 2017
- WTWY has a team of 50 volunteers, who each work twice a week, at a max of 4 hours per day

Attendees
- Tech workers, wealthy individuals and philanthropists are more likely to purchase Gala tickets
- Ridership frequency among the above groups is consistent with general population
- Locals are more likely to attend than tourists
- Geographical distribition of women is consistent enought to be negligble in our model

Data
- public datasets (esp MTA data) will contain an inherent amount of incorrectable error
- matches from 
- we will omit significant sources of error from our analays, but minor sources of error will persist

**MODELING CONSIDERATIONS**
We'll consider the following metrics in our final model:
SUBWAY RIDERSHIP
- Number of entries by station by time over a given week
- Number of exists by station by time over a given week
- Number of subway entrances (bottlenecks per station (for final considerations)
CROSS REFERENCES
- Average income in area surrounding station
- Average donor activity in area surrounding station
- Effect of weather on subway ridership
- Prevalence of Toursts (anecdotal)
- Proximity to tech hubs (anecdotal)

**DATASETS**
- MTA weekly turnstile data
- Census Data: income income per census tract
- Census Data: past donations relative to income per census tract
- NOAA NYC Climate Data

- anedotal information regarding tourist hotspots botltlenecks
