import pandas as pd
import pickle
import matplotlib.pyplot as plt
from column_headings import *

with open('CB5VoterData.pkl', 'rb') as f:
    df = pickle.load(f)

#print(df.iat[10000,SCORE])

"""Plans:
    * I'd like to make a histogram using pandas
    * Scatter plot where the diameter of the dots is in proportion to the size of the precinct
"""
make_window_graphs = False
if make_window_graphs:
    window = 0.1
    max_percent = 1.0
    min_percent = 0.0
    floor = 0.0

    percent_voted = []
    buckets = []

    while floor + window <= max_percent:
        num_voters = 0
        tot_voted = 0
        for index, row in df.iterrows():
            if float(row.iloc[SCORE]) >= floor and float(row.iloc[SCORE]) < floor + window:
                num_voters = num_voters + 1
                if float(row.iloc[VOTED]) == 1:
                    tot_voted = tot_voted + 1
        #print("In the range " + str(floor) + " to " + str(floor+window) + " the percent that voted was " + str(tot_voted / num_voters))
        if num_voters != 0:
            percent_voted.append(tot_voted / num_voters)
            buckets.append(floor)
        floor = floor + window


compare_texts = True
if compare_texts:
    window = 0.1
    max_percent = 1.0
    min_percent = 0.0
    floor = 0.0

    pct_voted_text = []
    pct_voted_no_text = []
    buckets = []

    while floor + window <= max_percent:
        num_voted_text = 0
        num_voted_no_text = 0
        tot_voters_text = 0
        tot_voters_no_text = 0
        for index, row in df.iterrows():
            if float(row.iloc[SCORE]) >= floor and float(row.iloc[SCORE]) < floor + window:
                #anycontact = max(float(row.iloc[TEXT]), float(row.iloc[LITBAG]), float(row.iloc[ENVELOPE]), float(row.iloc[POSTCARD]))
                if float(row.iloc[TEXT]) > 0:
                    tot_voters_text = tot_voters_text + 1
                    if float(row.iloc[DVOTE]) == 1:
                        num_voted_text = num_voted_text + 1
                else:
                    tot_voters_no_text = tot_voters_no_text + 1
                    if float(row.iloc[DVOTE]) == 1:
                        num_voted_no_text = num_voted_no_text + 1

        #print("In the range " + str(floor) + " to " + str(floor+window) + " the percent that voted was " + str(tot_voted / num_voters))
        if tot_voters_text != 0:
            pct_voted_contact = num_voted_text / tot_voters_text
            pct_voted_text.append(pct_voted_contact)
        if tot_voters_text == 0:
            pct_voted_text.append(0)
        if tot_voters_no_text != 0:
            pct_voted_no_contact = num_voted_no_text / tot_voters_no_text
            pct_voted_no_text.append(pct_voted_no_contact)
        if tot_voters_no_text == 0:
            pct_voted_no_text.append(0)
        buckets.append(floor)
        floor = floor + window

        print(floor)
        print("Percent Voted w Contact:", pct_voted_contact)
        print("Percent Voted w/o Contact:", pct_voted_no_contact)
        print("Boost Percent:", pct_voted_contact-pct_voted_no_contact)
        print("Total Voters Contacted:",tot_voters_text)
        print("Total Voters Not Contacted:",tot_voters_no_text)
        print("Voters Boosted:", (pct_voted_contact-pct_voted_no_contact)*tot_voters_text)
        print("")

#find diff
differences = []
new_buckets = []
for i in range(len(buckets)):
    if pct_voted_no_text[i] != 0 and pct_voted_text[i] != 0:
        differences.append(pct_voted_text[i] - pct_voted_no_text[i])
        new_buckets.append(i)

print(df.iloc[:,TEXT].sum())

plt.plot(buckets, pct_voted_text, label = 'Contact')
plt.plot(buckets, pct_voted_no_text, label = 'No Contact')



#plt.plot(new_buckets, differences)

plt.xlabel("Score")
plt.ylabel("Voted Pct")
plt.legend()

plt.show()
