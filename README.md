# AWAR
WAR refers to the commonly used baseball statistic, wins above replacement which attempts to measure the number of wins contributed by a given player relative to a hypothetical minor league replacement.
For the uninitiated, this article is a good introduction: https://library.fangraphs.com/misc/war/, as is this video: https://www.youtube.com/watch?v=ipD053CE3PI&t=567s.
The purpose of this project is twofold. First I want to develop my comfort working with numpy to (hopefully) efficiently manipulate large datasets.
Second, I hope to adress issues I have with the methods sites like baseball reference and fangraphs use to calculate war, particularly as it pertains to 
assessing the values of stolen bases. Most of the data I take issue with can be found on this page at fangraphs: https://www.fangraphs.com/guts.aspx?type=cn 

Currently Finished: 

1: I have finished the functions that use retrosheet's bevent program to quickly compile data downloaded for a given year into the appropriate format for this project. 

2: I have finished writing the functions that build the run expectancy matrix for a given year. My run expectancy matrix differs slightly from those I've found online. The typical approach seems to be to exclude half-innings in which a walk-off occurs as these innings are technically incomplete; a third out is never recorded and thus potential runs are left on the board. I take issue with this method as I believe it skews the data towards low scoring half-innings in which a walk-off might have occurred but didn't, my solution has been to exclude all half-innings in which there could have been a walk-off. Any discrepencies between my later calculated run values and those found online should be at least partly attributable to this fact. Commented out of my code are the methods to compute the run expectancy matrix dropping only walk-off half innings in case I'm later convinced that my approach is worse.

3: I have finished writing the functions that compute the weighted values of various batting and baserunning events for a given year that will later enable the calculation of a player's total run contribution.

4: I implemented a very basic method to park adjust run contribution. Down the line I will calculate expectancy matrix and weights separately for each league in years predating the balanced schedule. I would also consider park adjusting for each batted ball event and for batter handedness. 

In progress:

5: Developing my own version of UBR for baserunning. 
6: Writing a method to exclude pitcher hitting from RE24 and linear weight calculations. This shouldn't require any existing code to be rewritten, I should be able to filter it out ahead of time but it might require me to
get a little creative with handling skipped plate appearences and accounting for any runs they score. We'll see when we get there. 
