https://nkshv.github.io/

# Overview

In this project, the Elo rating algorithm is employed to determine the relative skill levels between fighters and rank
them accordingly and objectively. Proposed as an alternative to the pound-for-pound ranking, the Elo ranking is in no way an attempt
to replace the former, as numbers don't tell the whole story: while insightful, the algorithm does not fully capture the intricacies of any fight as
the only factors considered are the strength of each competitor and the end result. Another factor that contributes to its lack of accuracy is the fact
that MMA is a sport that generally favors youth. A lot of fighters benefit by stacking up wins against aging fighters, whose Elo doesn't reflect their
current skills anymore. Conversely, because it only takes into account fights that took place in the UFC, some elite fighters coming from another promotions
are underrated giving their lack of experience inside the UFC octagon.

# How it works

The program was made using Python, and the data was web scrapped from the ufcstats website using BeautifulSoup. It generates a simple html file containg
a table with every fighter that has ever fought in the UFC and their ratings. The website is updated weekly, on Sundays.
The starting value is 100 and K-factor (factor of change) is equal to 32.