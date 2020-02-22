
from math import log10, e, log, log2
import json


def point_calc(sco, lvl):
    # apply the 0.5*level buffer
    return (sco)*(1+lvl)**2
    # return log10((sco+2)**(lvl+3))
    # return log10((sco+1)**(lvl+1))


with open("DailyChallengePools/challenge_results.json", 'r') as infile:
    jason = json.load(infile)
    # print(jason)
    infile.close()

print("Points earned: log10((2+score)^(3+level))")
print(" Bonus points:  score^2")
print("V level // score >")

for level in range(0, 8):
    for score in range(0, 9):
        print(point_calc(score, level), end="\t")
    print()

print()

scores = {}
points = {}
for day in jason:
    for level in jason[day]:
        for result in jason[day][level]:
            earned = point_calc(result["score"], int(level))
            sniper = result["sniper"]
            if sniper not in scores:
                scores[sniper] = [result["score"]]
                points[sniper] = earned
            else:
                scores[sniper].append(result["score"])
                points[sniper] += earned

unordered = []
for sniper in scores:
    pkg = points[sniper], sum(scores[sniper]), 8*len(scores[sniper]), sniper
    unordered.append(pkg)
unordered.sort(reverse=True)

for x in unordered:
    print("{}'s challenge points: {}\t({} wins/{} games, winrate: {}%)".format(x[3], x[0], x[1], x[2], round(100*x[1]/x[2])))

print()
most_points = max([x[0] for x in unordered])
point_reward = sum([point_calc(8, i) for i in range(0, 8)]) + 64
print("Highest points:", most_points)
print("Max. point reward:", point_reward)
print("Perfect days to catch up:", most_points/point_reward)
