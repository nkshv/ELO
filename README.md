https://nkshv.github.io/ELO/web/

# Overview

In [this project](https://nkshv.github.io/ELO/web/), the Elo rating algorithm is employed to determine the relative skill levels between fighters and rank
them accordingly and objectively. Proposed as an alternative to the pound-for-pound ranking, the Elo ranking is in no way an attempt
to replace the former, as numbers don't tell the whole story: while insightful, the algorithm does not fully capture the intricacies of any fight as
the only factors considered are the strength of each competitor and the end result. Another factor that contributes to its lack of accuracy is the fact
that MMA is a sport that generally favors youth. A lot of fighters benefit by stacking up wins against aging fighters, whose Elo doesn't reflect their
current skills anymore. Conversely, because it only takes into account fights that took place in the UFC, some elite fighters coming from another promotions
are underrated giving their lack of experience inside the UFC octagon.

# Intricacies
All the data was obtained via web scraping from [UFC's website](http://ufcstats.com/statistics/events/).
The starting value used in this project is 100 and the K-factor (factor of change) is equal to 32.
Although convoluted to read and make changes, the single python source file makes it simple for use in such a simple project. Upon execution, all functionalities become accessible. 
*ufc_ranking_elo.py* does all the data gathering, processing, web page creation and persistence of information as a csv file.
