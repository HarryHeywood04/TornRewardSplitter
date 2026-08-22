import math
import requests

tornToken = "" # Enter token here
reward_fund = 278000000 # Enter money obtained from the trade here
faction_id = '51122' # Replace with faction ID

def request(section, selection, ID=""):
    if ID == "":
        return requests.get(
            "https://api.torn.com/" + section + "/?selections=" + selection + "&key=" + tornToken + "&comment=RewardSplitter")
    else:
        return requests.get(
            "https://api.torn.com/" + section + "/" + ID + "?selections=" + selection + "&key=" + tornToken + "&comment=RewardSplitter")


def getWarRewards(money):
    money = int(money)
    result = ""
    member_cash = float(money) * 0.9 # Enter ratio of money to go to members
    result += "Total: " + f"${math.floor(money):,d}" + "\n"
    # Get most recent war ID
    response = request("faction", "rankedwars").json()
    war_IDs = list(response['rankedwars'].keys())
    war_IDs.sort()
    latest_war_ID = war_IDs[-1]
    # Get details using ID
    war_report = request("torn", "rankedwarreport", ID=latest_war_ID).json()
    members = war_report['rankedwarreport']['factions']['51122']['members']
    # Extract players and hit numbers
    member_ids = list(members.keys())
    extracted_member_data = []
    total_hits = 0
    total_score = 0
    for id in member_ids:
        if members[id]['attacks'] > 0:
            single_member_data = dict()
            single_member_data['name'] = members[id]['name']
            single_member_data['hits'] = members[id]['attacks']
            single_member_data['score'] = members[id]['score']
            total_hits += single_member_data['hits']
            total_score += single_member_data['score']
            extracted_member_data.append(single_member_data)
    # Divide money by hits and assign to players
    mph = member_cash / total_hits
    for member in extracted_member_data:
        member['money'] = member['hits'] * mph
    extracted_member_data.sort(key= lambda item: item['hits'], reverse=True)
    # Return list of players - hits - reward
    for member in extracted_member_data:
        result += member['name'] + ' - ' + f"{member['hits']:,d}" + ' - ' + f"${math.floor(member['money']):,d}" + '\n'
    return result

print(getWarRewards(278000000))
