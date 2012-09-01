
usernames = [
    "thenorthfacethe",
    "uggstore",
    "petitepetite",
    "fitnessdvds",
    "goosedown",
    "nikefitsole",
    "belstaffoutlet",
    "clubsgolf",
    "bestoutlet",
    "belstaffonline",
    "christianmary",
    "mprompink",
    "zntezsari",
    "nlitanoheat",
    "racmurraylize",
    "porgphil",
    "lwiefelhoaudr",
    "lnchmelaweldo",
    "tfolettovern",
    "lodwelleste",
    "ianicoliaterin",
    "eimeedmo",
    "iogauvinsergi",
]

for un in usernames:
    try:
        u = User.objects.get(username=un)
        u.delete()
    except User.DoesNotExist:
        pass

