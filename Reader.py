import os
import json
import re
from Result import Result

root = "./Datafiles"
results = {}
res_re = re.compile(r'''\*\*(?P<sniper>[^*]+)\*\*\s+Day #(?P<day>[\d]+)\s+_Level:_ \*\*(?P<level>[\d])(\s\()?(?P<delta>[+\-\d]+)?(?P<bonus>(bonus))?\)?[\s\S]*\*\* _Score:_ \*\*(?P<score>[\d])/8\*\* _Time:_ \*\*((?P<m>[\d]+)m)?\s?(?P<s>[\d]+)s\*\*\n\|\|(\*\*Won against:\*\*\s(?P<wins>(.*?)))?(\s\s)?(\*\*Lost to:\*\*\s(?P<losses>(.*?)))?\|\|''')

# One of Opi's lvl 7 8/8 scores is invalid/illegitimate


def coherency_check(mtchs):
    if mtchs["day"] < "61":
        print(mtchs["day"], "< 61")
        return False
    tot = len(mtchs["losses"]) + len(mtchs["wins"])
    if tot != 8:
        print(tot, "games found!")
        return False
    if mtchs["s"] not in range(0, 61):
        print(mtchs["s"], "is invalid!")
        return False
    return True


for filename in os.listdir(root):
    file = open(root+"/"+filename, "r", encoding='utf-8')
    jason = json.load(file)
    file.close()

    for channel in jason["data"]:
        for message in jason["data"][channel]:
            # the sender must be SniperDailyChallenge, since checker has also sent messages
            if jason["data"][channel][message]['u'] == 0:
                msg = jason["data"][channel][message]["m"]
                # print(msg)

                match = res_re.match(msg)
                if match is None:
                    print("failed:", msg)
                    continue
                matches = match.groupdict()
                matches["level"] = int(matches["level"])
                matches["delta"] = int(matches["delta"]) if matches["delta"] is not None else 0
                # matches["sniper_level"] = matches["level"] - (int(matches["delta"]) if matches["delta"] is not None else 0)
                # del matches["delta"]
                matches["bonus"] = matches["bonus"] is not None
                matches["score"] = int(matches["score"])
                matches["m"] = int(matches["m"]) if matches["m"] is not None else 0
                matches["s"] = int(matches["s"])
                matches["wins"] = matches["wins"].split(", ") if matches["wins"] is not None else []
                matches["losses"] = matches["losses"].split(", ") if matches["losses"] is not None else []
                # print(matches)

                if coherency_check(matches):
                    day = matches["day"]
                    lvl = matches["level"]
                    del matches["day"], matches["level"]
                    if day in results:
                        if lvl in results[day]:
                            results[day][lvl].append(matches)
                        else:
                            results[day][lvl] = [matches]
                    else:
                        results[day] = {}
                else:
                    print("incoherent:", msg)

    with open("DailyChallengePools/challenge_results.json", 'w') as outfile:
        json.dump(results, outfile)
        outfile.close()

