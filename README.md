nkshv.github.io/ELO/
# Overview

The [Elo rating algorithm](https://en.wikipedia.org/wiki/Elo_rating_system) was employed to determine the relative skill levels between every fighter that has ever fought under the UFC banner and rank them accordingly and objectively. Proposed as an alternative to the pound-for-pound ranking, the Elo ranking is in no way an attempt to replace the former, as numbers don't tell the whole story: while insightful, the algorithm does not fully capture the intricacies of any fight as the only data gathered are the strength of each competitor and the fight result.

# Intricacies
All the data was obtained via web scraping from [UFC's website](http://ufcstats.com/statistics/events/).
The starting value used in this project is 100 and the K-factor (factor of change) is equal to 32.
Although convoluted to read and make changes, the single python source file simplifies the use in such a basic project. Upon execution, all functionalities become accessible.
*ufc_ranking_elo.py* does all the data gathering, processing, web page creation, local file organization and persistence of information as a csv file.

# Accuracy
Given the very limited number of fights an athlete typically has throughout their career, such ranking is far from perfect.
The possible lack of accuracy can also be explained by the fact that MMA, by its own nature, is a sport that favors youth. A lot of fighters benefit by stacking up wins against aging fighters, whose Elo doesn't reflect their current skills anymore. Conversely, because it only takes into account fights that took place in the UFC, some elite fighters coming from another promotions are underrated giving their lack of experience inside the UFC octagon.
