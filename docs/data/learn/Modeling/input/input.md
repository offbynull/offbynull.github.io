`{title} Modeling`

```{toc}
```

# Probability

One way to think about probability is as a fraction of a finite set, where a ...

* finite set means a collection of items of the same class (e.g. people)
* fraction means some portion of a finite set (e.g. 50 out of 1000 people).

The idea is that the fraction is representative of the likelihood of some statement, called a proposition, being true. For example, imagine attempting to determine the probability of a person being a child. One possibility is to randomly find 1000 people and determine how many of them are children. For example, if 250 out of the 1000 people are children, it's reasonable to assume that the likelihood of any random person being a child is 250/1000 = 0.25. In other words, there's a 0.25 probability that a person selected at random is a child.

```{svgbob}
+------+------+
| "<18"|      |
|      |      |
+------+      |
|             |
|             |
+-------------+
```

```{run}
#>>>people.csv
import pandas
pandas.set_option('display.max_rows', 4)
print('\n```')
# MARKDOWN
df = pandas.read_csv('people.csv', index_col=0, skipinitialspace=True)
print(df, end='\n\n')
child = df['age'] < 18
print(f'{sum(child == True)=}', end='\n\n')
# MARKDOWN
print('```\n')
```

The notation for probability is P(A), where A is proposition.

## Complement (NOT)

Where as probability is the likelihood of some proposition being true, complement probability is the likelihood of that same proposition being false. If you already know what the probability of some proposition being true is, denoted as P(A), its complement probability is simply 1 - P(A).

For example, if you know that the probability of a person being a child is 0.25, then the probability of a person not being a child is 1 - 0.25 = 0.75.

```{svgbob}
+------+------+
| "<18"|      |
|      |      |
+------+      |
|             |
|   ">=18"    |
+-------------+
```

If you were to think of probabilities as fractions of a finite set, the fraction of people that are children is 250/1000 (0.25). That leaves 750/1000 that aren't children (0.75). 1 - 0.25 = 0.75.

```{run}
#>>>people.csv
import pandas
pandas.set_option('display.max_rows', 4)
print('\n```')
# MARKDOWN
df = pandas.read_csv('people.csv', index_col=0, skipinitialspace=True)
print(df, end='\n\n')
child = df['age'] < 18
print(f'{sum(child == True)=}', end='\n\n')
print(f'{sum(child == False)=}', end='\n\n')
# MARKDOWN
print('```\n')
```

Where as the notation for probability is P(A), the notation for complement probability is P(A').

## Conjunction

Consider two probabilities, both for the same population: P(A) and P(B). The probability that propositions A and B are both true is P(A) * P(B). For example, the probability that a person is a ...

 * child is 0.25.
 * overweight is 0.5.

The probability that a person is both a child and overweight should come out to 0.125.

```{run}
#>>>people.csv
import pandas
pandas.set_option('display.max_rows', 4)
print('\n```')
# MARKDOWN
df = pandas.read_csv('people.csv', index_col=0, skipinitialspace=True)
child = df['age'] < 18
overweight = df['overweight']
df = pandas.DataFrame(data={
  'child': child,
  'overweight': overweight,
  'both': child & overweight
})
print(df, end='\n\n')
print(f'{df["child"].mean()=}', end='\n\n')
print(f'{df["overweight"].mean()=}', end='\n\n')
print(f'{df["both"].mean()=}', end='\n\n')
# MARKDOWN
print('```\n')
```

In the Python example above, the fraction of the population that's both a child and overweight comes out to roughly 0.125. One way to think about this is as an intersection: Think of the 1000 people above as randomly standing around. If you were to select ...

 * 90 people at random, roughly half of them would be overweight.
 * all children, roughly half of them would be overweight.
 * all adults, roughly half of them would be overweight.

If you're selecting based on some criteria that doesn't factor in overweight-ness, then chances are that roughly half of the people you select will end up being overweight. In this case, 25% of the people above are children. As such, half of those 25% should be overweight: 0.25 * 0.5 = 0.125.

The reasoning works the other way as well. If you were to select ...

 * 90 people at random, roughly a quarter of them would be children.
 * all overweight, roughly a quarter of them would be children.
 * all non-overweight, roughly a quarter of them would be children.

If you're selecting based on some criteria that doesn't factors in age, then chances are that roughly a quarter of the people you select will end up being children. In this case, 50% of the people above are overweight. As such, a quarter of those 50% should be children: 0.5 * 0.25 = 0.125.
 
Swapping the probabilities around produces some the same result: The probability that propositions B and A are both true is P(B) * P(A). The probability that a 0.5 people are overweight. Of those 0.5, a quarter of them are children. So, you're essentially isolating to the population that are overweight, of which a quarter are children: 0.125 percent of the population.

There is one caveat. If the propositions A and B aren't for the same population, the probability that P(A) and P(B) are both true will be 0.0. For example, the probability that ...

 * a person is a child is 0.25.
 * a rabbit is cream colored is 0.1.

The conjunction probability of the two probabilities above is 0.0 because the probabilities are for different populations. A person can't be a rabbit and a rabbit can't be a person. The populations don't overlap.

## Disjunction

## Conditional

## Bayes Theorem

Probability rules:

 P(A) - Probability of some proposition A.
 P(A and B) - Probability of A and B both being true.
 P(A|B) - Probability of A given that B is true.

 

`{ref} tb:p9`

# Terminology

 * `{bm} statistics` - The collection, analysis, interpretation, and presentation of data. `{ref}osis:1.1`

 * `{bm} descriptive statistics` - The organizing and summarizing of data. `{ref}osis:1.1`

 * `{bm} inferential statistics` - Formal methods for drawing conclusions from good data, where probabilities are used as a measure of confidence for those conclusions. `{ref}osis:1.1`

 * `{bm} population` - A set under study. `{ref}osis:1.1`

 * `{bm} sample/(sample|sampling)/i` - A subset of a population, selected to represent the population in studies that produce information about the population. For example, instead of studying all people on Earth, a sample of 1000 people might be chosen as a representation of all people on Earth. `{ref}osis:1.1`

   Sampling is used because it's a more practical alternative to studying an entire population, which often times isn't feasible (e.g. studying 1000 people is more feasible than studying every single person on Earth). `{ref}osis:1.1` However, the sample should retain the characteristics of the population that it's from, meaning that results of studies done on the sample translate to the population. In that sense, samples are typically random samples. `{ref}osis:1.2`

 * `{bm} random sample/(random sample|random sampling)/i` - A sample where members of the population are randomly selected for the sample, intended to reduce / eliminate bias. `{ref}osis:1.2`

   True random sampling is performed with replacement. `{ref}osis:1.2`

 * `{bm} simple random sample/(simple random sample|simple random sampling)/i` - A form of sampling where where each member of a population had an equal chance of being selected for the sample. `{ref}osis:1.2`

 * `{bm} stratified sample/(stratified sample|stratified sampling)/i` - A form of random sampling where the population is first placed into groups (strata), then a proportionate number of members from each group are randomly selected to be part of the sample. `{ref}osis:1.2`

 * `{bm} cluster sample/(cluster sample|cluster sampling)/i` - A form of random sampling where the population is first placed into groups (clusters), then a set of the groups are randomly selected, where the members of those selected groups make up the sample. `{ref}osis:1.2`

 * `{bm} systematic sample/(systematic sample|systematic sampling)/i` - A form of random sampling where the population is lined up, a random starting point in the line is selected, and every nth member after the start of the line is selected to be part of the sample. For example, imagine being given a list of stores in the city you live in. Picking a random starting point in that list and selecting every 5th store after that starting point is systematic sampling. `{ref}osis:1.2`

 * `{bm} convenience sample/(convenience sample|convenience sampling)/i` - A form of sampling where, rather than randomly selecting members of the population somehow, members of the population are selected in some other non-random fashion. For example, selecting a sample of restaurant goers by choosing those who are already currently eating at the local Burger King restaurant. `{ref}osis:1.2`

 * `{bm} with replacement/(with replacement|without replacement)/i` - A form of random sampling where a member of the population can get placed in the sample more than once. That is, once a member is selected for a sample, that member is re-inserted back into the population and may get selected again. `{ref}osis:1.2`

   While true random sampling is performed with replacement, it's sometimes more practical to sample without replacement. For example, having members of a population fill out a survey is an example of sampling without replacement (once a member fills out a survey, that member won't be selected to fill out the survey again). For large populations where a small number of members are being sampled, it typically won't matter if the sample is with replacement or without replacement. It becomes an issue when the population size is small. `{ref}osis:1.2`

 * `{bm} sampling error` - An error in analysis due to the sample not being representative of the population it represents. For example, the sample might have been too small or biased in some way. `{ref}osis:1.2`

   In most cases, a sample will never be truly representative of it the population it was chosen from. There will always be some level of sampling error. `{ref}osis:1.2`

 * `{bm} non-sampling error/(non[-\s]?sampling error)/i` - An error in analysis unrelated to sampling error (all errors other than those caused by poorly choosing a sample). These are typically errors caused by faulty data collection. For example, incorrectly counting up the answers in a set of surveys is a non-sampling error. `{ref}osis:1.2`

 * `{bm} sampling bias/(sampling bias|bias)/i` - When a sample isn't representative as of its population because some members of the population were more likely to be selected than others for the sample. `{ref}osis:1.2`

 * `{bm} variation` - How spread out data is around the center of data. For example, the manufacturer that makes Snickers chocolate bar may intend for each bar to be 1.86 ounces, but realistically the weight of each Snickers will fluctuate one way or the other by some marginal amount. `{ref}osis:1.2`

 * `{bm} measurement levels/(measurement levels|levels of measurement|measurement scales|scales of measurement|nominal scale|ordinal scale|interval scale|ratio scale)/i` - There are four different classes in which data is measured, depending on the data's properties. `{ref}osis:1.3`

   * nominal scale - A form of measuring categorical data that is unordered. For example, smartphone models are categories and there is no inherit order to them, so they would be measured on a nominal scale. `{ref}osis:1.3`

   * ordinal scale - A form of measuring categorical data that is ordered / ranked (unlike nominal scale), but the degree of difference between the measured items isn't captured. For example, the top 5 smartphone models is ordinal scale data. A smartphone model that comes before another one is ranked higher, but the difference in how much better it is isn't captured by the ordinal scale. `{ref}osis:1.3`

   * interval scale - A form of measuring quantitative data that is ordered / ranked, where the distance between the measured items is captured (unlike ordinal scale). However, there is no base value / fixed beginning with interval scale data. For example, 2:15pm is one hour ahead of 1:15pm (distance is captured), but you can't say that 2:15pm is n times more than 1:15pm (not representable as a ratio) because there is no definitive starting point in which time starts. `{ref}osis:1.3`

   * ratio scale - A form of measuring quantitative data that is ordered / ranked, where the distance between the measured items is captured and there is a fixed beginning (unlike interval scale). When there is a fixed beginning, it's possible to compute ratios. For example, 30 feet below sea-level is twice as deep as 15 feet below sea-level. `{ref}osis:1.3`

   |                      | Nominal scale | Ordinal scale | Interval scale | Ratio scale |
   |----------------------|---------------|---------------|----------------|-------------|
   | Labelled (has names) |        x      |       x       |         x      |      x      |
   | Ordered (has ranks)  |               |       x       |         x      |      x      |
   | Distance             |               |               |         x      |      x      |
   | Fixed beginning      |               |               |                |      x      |

   ```{note}
   For interval scale, can't you just make a arbitrary starting point? For example, treat midnight as the starting point. Then you would be able to take a ratio.

   I suppose if you gave it a starting point, it wouldn't be interval scale anymore. It would be ratio scale.
   ```

 * `{bm} frequency` - The number of times some value occurs in data. For example, in the list [9, 8, 1, 1, 5, 7, 9, 7, 6], 7 has a frequency of two. `{ref}osis:1.3`

 * `{bm} relative frequency` - A ratio representing the number of times some value occurs in the data vs the total number of items in that data. In other words, the relative frequency is the frequency as a ratio. For example, in the list [9, 8, 1, 1, 5, 7, 9, 7, 6], 7 has a relative frequency of `{kt} \frac{2}{9}`. `{ref}osis:1.3`

 * `{bm} cumulative frequency/(cumulative frequency|cumulative relative frequency)/i` - The accumulation of frequencies down a list, where that list has a meaningful incrementing order. This is useful when the data is interval scale / ratio scale because it gives an "up-until" view. For example, consider data that tracks the month in which a fridge was sold: [Jan, Jan, Feb, Feb, Mar, Mar, Mar, ...]. The cumulative frequency will let you know how many fridges were sold in total by each month. `{ref}osis:1.3`

   | Month | Fridges Sold (Frequency) | Total Fridges Sold (Cumulative Frequency) |
   |-------|--------------------------|-------------------------------------------|
   | Jan   |         3                |   3                                       |
   | Feb   |         2                |   3+2=5                                   |
   | Mar   |         2                |   3+2+2=7                                 |
   | ...   |        ...               |   ...                                     |

   ```{note}
   For cumulative relative frequency, the ending frequency in the list should sum to 1.

   Beware floating point rounding errors. It may not sum to exactly 1.
   ```

 * `{bm} explanatory / response variable/(explanatory variable|response variable)/i` - Two variables that have a relationship with each other, where changes in the explanatory variable causes changes in the response variable. Researchers manipulate an explanatory variable and measure the resulting changes in the response variable. For example, imagine a clinical trial that's testing the effectiveness of a flu drug. The amount of the drug administered is the explanatory variable while the degree to which flu symptoms are expressed is the response variable. `{ref}osis:1.4`

   ```{note}
   See treatment experimental unit, and lurking variable.
   ```

 * `{bm} treatment` - One specific value within an exploratory variable. Treatments are applied to experimental units. For example, if the exploratory variable is the amount of some drug that gets administered, the treatments may be 50mg, 70mg, 200mg, etc.. `{ref}osis:1.4`

 * `{bm} experimental unit` - A single entity that can have a treatment applied to it. Once treatment is applied, the experimental unit is measured. For example, if treatment is the administrating of a drug, the experimental unit may be a person. That is, each treatment of the drug (exploratory variable) is given to a single person, where that person's symptoms are measured (response variable). `{ref}osis:1.4`

 * `{bm} lurking variable` - A variable that is neither an explanatory variable nor a response variable, but still could influence the relationship between the two variables. For example, imagine a clinical trial that's testing the effectiveness of a flu drug. Age can be a lurking variable in that older people typically have less active immune systems, and as such may not show as much improvement in symptoms unless given higher dosages (treatments). `{ref}osis:1.4`

   Studies typically limit the influence of lurking variables by randomly assigning experimental units to treatment groups. The random assignment should make it so that lurking variables are equally spread out between those groups, and as such their impact won't be an outsized influence on the relationship between explanatory variable and response variable. `{ref}osis:1.4`

   ```{note}
   Does "random assignment" in this case just mean random sampling? Random assignment is what the book uses.
   ```

 CONTINUE FROM: When participation in a study prompts a physical response from a participant, it is ...

 CONTINUE FROM: When participation in a study prompts a physical response from a participant, it is ...

 CONTINUE FROM: When participation in a study prompts a physical response from a participant, it is ...

 CONTINUE FROM: When participation in a study prompts a physical response from a participant, it is ...
 
 * `{bm} statistic` - A number that represents a property of a sample. For example, imagine that a sample of 1000 people have their heights measured. The average height across that sample is a statistic. `{ref}osis:1.1`

   Each statistic is an estimate of a population parameter. `{ref}osis:1.1`

 * `{bm} parameter/(parameter|population parameter)/i` - A number that represents the characteristic of the whole population, estimated using a statistic. For example, the average height across all people on Earth is a population parameter, while the average height across a sample of 1000 people is a statistic. The statistic is an estimation of the population parameter. `{ref}osis:1.1`

 * `{bm} representative sample` - A sample that captures the various characteristics of the population it comes from, meaning that it's a good representation of the population. A statistic on a representative sample should roughly align with the corresponding population parameter that it's for. `{ref}osis:1.1`

 * `{bm} variable/(variable|numerical variable|categorical variable)/i` - A characteristic or measurement that can be determined for every member of a population. Variables come in two forms:

   * numerical variable - A variable that measures something (e.g. a person's weight).
   * categorical variable - A variable that places into a category (e.g. a person being obese vs non-obese).

 * `{bm} data` - Values for a variable. For example, given a sample of 5 people from a population, the following data represents their weights (numerical variable): [180, 200, 144, 127, 194].  `{ref}osis:1.1`

 * `{bm} datum` - A single value in data. `{ref}osis:1.1`

 * `{bm} quantitative data` - Data that measures or counts the attributes of a population. Household income, number of family members, and distance to the nearest Burger King are all examples of quantitative data. `{ref}osis:1.2`

 * `{bm} qualitative data/(qualitative data|categorical data)/i` - Data that falls into a category but typically can't be measured or expressed using numbers. Hair color, car model, and brand of shoes are all examples of qualitative data. `{ref}osis:1.2`

 * `{bm} discrete quantitative data/(discrete|discrete data|discrete quantitative data)/i` - Quantitative data that can only be counted (no fractions / ratios). For example, imagine measuring the number of emails you send throughout the day. The value would end up being a whole number. There's no such thing as a sending a fractional number of e-mails (e.g. half e-mail or a quarter e-mail). `{ref}osis:1.2`

 * `{bm} continuous quantitative data/(discrete|discrete data|discrete quantitative data)/i` - Quantitative data that can be fractional. For example, imagine measuring how many hours it took someone to drive to work. The value may end up being a fractional number (e.g. 2.15 hours). `{ref}osis:1.2`

TODO: start from 1.2

TODO: start from 1.2

TODO: start from 1.2

BUT JUMP FORWARD TO SECTION 3.1 FIRST AND CLEAN UP BELOW

BUT JUMP FORWARD TO SECTION 3.1 FIRST AND CLEAN UP BELOW

BUT JUMP FORWARD TO SECTION 3.1 FIRST AND CLEAN UP BELOW












 * `{bm} proposition` - A declaration that either evaluated to true or false. For example, ...
 
   * "7 is prime" is true
   * "3 is greater than 4" is false.

 * `{bm} independent event/(independent event|independent probability|independent probabilities)/i` - Two events are independent if one's occurrence doesn't effect the probability of the other occurring. You can think of this in terms of sets. If the first event doesn't modify the set for the second event, it's an independent event. For example, ...
 
   * flipping a coin twice - the prior flip doesn't effect the following flip.
   * winning a lawsuit followed by a sale on Bananas - those two have nothing to do with each other.
   * a person being overweight and flipping a coin - those two have nothing to do with each other.

 * `{bm} dependent event/((?:dependent|non-independent) (?:event|probability|probabilities))/i`- Two event are dependent if one's occurrence *does* effect the probability of the other occurring. You can think of this in terms of sets. If the first event modifies the set for the second event, it's a dependent event. For example, ...

   * draw a card twice from the same deck - the removal of the first card will modify the set of available options for the second removal (51 vs 52).
   * a person being overweight and a person being a child - children are being limited to overweight people only (all people vs only overweight people).

 * `{bm} Bayes theorem/(Bayes theorem|Bayes's theorem)/i` -

 * `{bm} Bayesian statistics` - 

 * `{bm} conditional probability` - 

 * `{bm} probability` - A fraction of a finite set. `{ref}tb:p2`

   ```{note}
   The book mentions that the term probability is iffy to define, but this is the definition to use for now.
   ```

   P(A) means the probability of A. `{ref} tb:p8`

 * `{bm} conjunction` - Another name for the logical AND operator. `{ref}tb:p5`

 * `{bm} conjunction probability` - Probability of both A and B being true. `{ref} tb:p9`

 * `{bm} conditional probability` - A probability that depends on a condition (some other probability being true). `{ref} tb:p6` P(A|B) means that the probability of A given that B is true. `{ref} tb:p9`

 * `{bm-error} Did you mean cumulative relative frequency?/(relative cumulative frequency)/i` 

`{bm-ignore} !!([\w\-]+?)!!/i`
