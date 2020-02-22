import json

with open("DailyChallengePools/challenge_results.json", 'r') as infile:
    jason = json.load(infile)
    # print(jason)
    infile.close()


snipers = {}
for day in jason:
    for level in jason[day]:
        for result in jason[day][level]:
            sniper = result["sniper"]
            if sniper not in snipers:
                snipers[sniper] = [result["score"]]
            else:
                snipers[sniper].append(result["score"])

unordered = []
for sniper in snipers:
    pkg = sum(snipers[sniper]), 8*len(snipers[sniper]), sniper
    unordered.append(pkg)
unordered.sort(reverse=True)

for x in unordered:
    print("{}'s winrate: {}% ({} wins/{} games)".format(x[2], round(100*x[0]/x[1], 2), x[0], x[1]))
