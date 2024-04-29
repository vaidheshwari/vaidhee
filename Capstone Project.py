#!/usr/bin/env python
# coding: utf-8

#### Python Project 13 - Investigating Fandango Movie Ratings

# Reading in and explore briefly the two data sets:
# - fandango_score_comparison.csv :data he analyzed publicly available- (https://github.com/fivethirtyeight/data/tree/master/fandango).
# - movie_ratings_16_17.csv: data is publicly available- https://github.com/mircealex/Movie_ratings_2016_17) 
# Documentation of both datasets are available in related github repositories

import pandas as pd
pd.options.display.max_columns = 100  # Avoid having displayed truncated output

# Reading and assigning variables 
previous = pd.read_csv('fandango_score_comparison.csv')
after = pd.read_csv('movie_ratings_16_17.csv')

#Exploring
previous.head(3)

#Exploring
after.head(3)


# Below we isolate only the columns that provide information about 
# Fandango so we make the relevant data more readily available for later use.
# We'll make copies to avoid any(https://www.dataquest.io/blog/settingwithcopywarning/) *SettingWithCopyWarning* later on.

fandango_previous = previous[['FILM', 'Fandango_Stars', 'Fandango_Ratingvalue', 'Fandango_votes',
                             'Fandango_Difference']].copy()
fandango_after = after[['movie', 'year', 'fandango']].copy()

fandango_previous.head(3)

fandango_after.head(3)

#### Isolating the Samples We Need
# With this new research goal, we have two populations of interest:

# - All Fandango's ratings for popular movies released in 2015.
# - All Fandango's ratings for popular movies released in 2016.

fandango_after.sample(10, random_state = 1)


# Above we used a value of 1 as the random seed.
# This is good practice because it suggests that we weren't trying out various random seeds just to get a favorable sample.

# 90% of the movies in our sample are popular. This is enough and we move forward with a bit more confidence.

# Let's also double-check the other data set for popular movies. 
# The documentation states clearly that there're only movies with at least 30 fan ratings, 
# but it should take only a couple of seconds to double-check here.

sum(fandango_previous['Fandango_votes'] < 30)


# If you explore the two data sets, you'll notice that there are movies with a releasing year different than 2015 or 2016. 
# For our purposes, we'll need to isolate only the movies released in 2015 and 2016.
# Let's start with Hickey's data set and isolate only the movies released in 2015. 
# There's no special column for the releasing year, but we should be able to extract it from the strings in the FILM column.

fandango_previous.head(2)

fandango_previous['Year'] = fandango_previous['FILM'].str[-5:-1]
fandango_previous.head(2)


# Let's examine the frequency distribution for the Year column and then isolate the movies released in 2015.

fandango_previous['Year'].value_counts()

fandango_2015 = fandango_previous[fandango_previous['Year'] == '2015'].copy()
fandango_2015['Year'].value_counts()

# Great, now let's isolate the movies in the other data set.

fandango_after.head(2)

fandango_after['year'].value_counts()

fandango_2016 = fandango_after[fandango_after['year'] == 2016].copy()
fandango_2016['year'].value_counts()


##### Comparing Distribution Shapes for 2015 and 2016
# The aim is to figure out whether there's any difference between Fandango's ratings for popular movies in 2015 and Fandango's ratings 
# for popular movies in 2016. One way to go about is to analyze and compare the distributions of movie ratings for the two samples.
 
# We'll start with comparing the shape of the two distributions using kernel density plots. 
# We'll use the [FiveThirtyEight](https://www.dataquest.io/blog/making-538-plots/) style for the plots.

import matplotlib.pyplot as plt
from numpy import arange
get_ipython().magic('matplotlib inline')
plt.style.use('fivethirtyeight')

fandango_2015['Fandango_Stars'].plot.kde(label = '2015', legend = True, figsize = (8,5.5))
fandango_2016['fandango'].plot.kde(label = '2016', legend = True)

plt.title("Comparing distribution shapes for Fandango's ratings\n(2015 vs 2016)",
          y = 1.07) # the `y` parameter pads the title upward
plt.xlabel('Stars')
plt.xlim(0,5) # because ratings start at 0 and end at 5
plt.xticks(arange(0,5.1,.5))
plt.show()


# Two aspects are striking on the figure above:
# - Both distributions are strongly left skewed.
# - The 2016 distribution is slightly shifted to the left relative to the 2015 distribution.

# The left skew suggests that movies on Fandango are given mostly high and very high fan ratings. 
# Coupled with the fact that Fandango sells tickets, the high ratings are a bit dubious. 
# It'd be really interesting to investigate this further — ideally in a separate project, since this is quite irrelevant for the current goal of our analysis.
The slight left shift of the 2016 distribution is very interesting for our analysis. 
# It shows that ratings were slightly lower in 2016 compared to 2015. This suggests that there was a difference indeed between 
# Fandango's ratings for popular movies in 2015 and Fandango's ratings for popular movies in 2016. We can also see the direction of the difference: the ratings in 2016 were slightly lower compared to 2015.

##### Comparing Relative Frequencies
# It seems we're following a good thread so far, but we need to analyze more granular information. 
# Let's examine the frequency tables of the two distributions to analyze some numbers. 
# Because the data sets have different numbers of movies, we normalize the tables and show percentages instead.

print('2015' + '\n' + '-' * 16) # To help us distinguish between the two tables immediately and
                                # avoid silly mistakes as we read to and fro
fandango_2015['Fandango_Stars'].value_counts(normalize = True).sort_index() * 100

print('2016' + '\n' + '-' * 16)
fandango_2016['fandango'].value_counts(normalize = True).sort_index() * 1

# In 2016, very high ratings (4.5 and 5 stars) had significantly lower percentages compared to 2015. 

##### Determining the Direction of the Change
# Let's take a couple of summary metrics to get a more precise picture about the direction of the change. 
# In what follows, we'll compute the mean, the median, and the mode for both distributions and then use a bar graph to plot the values.

mean_2015 = fandango_2015['Fandango_Stars'].mean()
mean_2016 = fandango_2016['fandango'].mean()

median_2015 = fandango_2015['Fandango_Stars'].median()
median_2016 = fandango_2016['fandango'].median()

mode_2015 = fandango_2015['Fandango_Stars'].mode()[0] # the output of Series.mode() is a bit uncommon
mode_2016 = fandango_2016['fandango'].mode()[0]

summary = pd.DataFrame()
summary['2015'] = [mean_2015, median_2015, mode_2015]
summary['2016'] = [mean_2016, median_2016, mode_2016]
summary.index = ['mean', 'median', 'mode']
summary


plt.style.use('fivethirtyeight')
summary['2015'].plot.bar(color = '#0066FF', align = 'center', label = '2015', width = .25)
summary['2016'].plot.bar(color = '#CC0000', align = 'edge', label = '2016', width = .25,
                         rot = 0, figsize = (8,5))

plt.title('Comparing summary statistics: 2015 vs 2016', y = 1.07)
plt.ylim(0,5.5)
plt.yticks(arange(0,5.1,.5))
plt.ylabel('Stars')
plt.legend(framealpha = 0, loc = 'upper center')
plt.show()


# The mean rating was lower in 2016 with approximately 0.2. This means a drop of almost 5% relative to the mean rating in 2015.

(summary.loc['mean'][0] - summary.loc['mean'][1]) / summary.loc['mean'][0]


# While the median is the same for both distributions, the mode is lower in 2016 by 0.5. Coupled with what we saw for the mean, 
# the direction of the change we saw on the kernel density plot is confirmed: on average, popular movies released in 2016 
# were rated slightly lower than popular movies released in 2015.
 
##### Conclusion
# Our analysis showed that there's indeed a slight difference between Fandango's ratings for popular movies in 2015 
# and Fandango's ratings for popular movies in 2016. We also determined that, on average, popular movies released 
# in 2016 were rated lower on Fandango than popular movies released in 2015.
# We cannot be completely sure what caused the change, but the chances are very high that it was caused 
# by Fandango fixing the biased rating system after Hickey's analysis.



