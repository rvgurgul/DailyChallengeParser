import json

with open("DailyChallengePools/challenge_results.json", 'r') as infile:
    jason = json.load(infile)
    # print(jason)
    infile.close()

spies = {}
for day in jason:
    for level in jason[day]:
        for result in jason[day][level]:
            for spy in result["wins"]:
                if spy not in spies:
                    spies[spy] = [False]
                else:
                    spies[spy].append(False)
            for spy in result["losses"]:
                if spy not in spies:
                    spies[spy] = [True]
                else:
                    spies[spy].append(True)

appearances = {}
for day in jason:
    for level in jason[day]:
        for result in jason[day][level]:
            for spy in result["wins"]+result["losses"]:
                if spy not in appearances:
                    appearances[spy] = {(day, level)}
                else:
                    appearances[spy] |= {(day, level)}
print(appearances)

unordered = []
for spy in spies:
    pkg = len(appearances[spy]), len(spies[spy]), spies[spy].count(True), spy
    unordered.append(pkg)
unordered.sort(reverse=True)

for x in unordered:
    print("{}'s winrate: {}% ({} wins/{} games, {} appearances)".format(x[3], round(100*x[2]/x[1], 2), x[2], x[1], x[0]))
print()
for x in unordered:
    print("{}'s winrate: {}x ({} wins/{} appearances)".format(x[3], round(x[2]/x[0], 2), x[2], x[0]))



