import json

jason = {}
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

unordered =[]
for spy in spies:
    pkg = len(spies[spy]), spies[spy].count(True), spy
    unordered.append(pkg)
unordered.sort(reverse=True)

for x in unordered:
    print("{}'s winrate: {}% ({} wins/{} appearances)".format(x[2], round(100*x[1]/x[0], 2), x[1], x[0]))
