print("Elemental Shaman simulator v0.1 beta")

import json
import random

#Load constants
with open('constants.json') as json_file:
    constants = json.load(json_file)[0]
    
with open('config.json') as json_file:
    config = json.load(json_file)[0]

print(config)

print("\nConfig:")
print("Base Spell Power: " +config['gear']['basespellpower'])
print("Spell Crit From Talents: " +config['spec']['critfromtalents'])
print("Spell Crit From Items: " +config['gear']['critfromitems'])
print("Base Intellect: " +config['gear']['baseintellect'])
print("Spell Hit From Talents: " +config['spec']['hitfromtalents'])
print("Spell Hit From Items: " +config['gear']['hitfromitems'])
print("Arcane Brilliance Buff used: " +config['buffs']['arcanebrilliance'])
print("Gift Of The Wild Buff used: " +config['buffs']['giftofthewild'])
print("Brilliant Wizard Oil used: " +config['buffs']['brilliantwizardoil'])
print("Greater Arcane Elixir used: " +config['buffs']['greaterarcaneelixir'])
print("Flask of Supreme Power used: " +config['buffs']['flask'])

#Assume config.json values are valid and update if not
errors=False

#Calculated char stats:
#intellect=baseintellect+arcanebrillianceint+giftofthewildint
intellect=int(config['gear']['baseintellect'])
if config['buffs']['arcanebrilliance'].lower()=='true':
    intellect+=int(constants['arcanebrillianceint'])
elif config['buffs']['arcanebrilliance'].lower()!='false':
    errors=True
    
if config['buffs']['giftofthewild'].lower()=='true':
    intellect+=int(constants['giftofthewildint'])
elif config['buffs']['giftofthewild'].lower()!='false':
    errors=True
    

critfromint=intellect/float(constants['intpercrit'])
crit=critfromint +float(config['spec']['critfromtalents']) +float(config['gear']['critfromitems'])
hit=int(constants['basehitpercent']) +int(config['spec']['hitfromtalents']) +int(config['gear']['hitfromitems'])

#hit cap innit
if hit > 99:
    hit=99

spellpower=int(config['gear']['basespellpower']) 
if config['buffs']['brilliantwizardoil'].lower()=='true':
    spellpower+=int(constants['brilliantwizardoilpower'])
    crit+=float(constants['brilliantwizardoilcrit'])
elif config['buffs']['brilliantwizardoil'].lower()!='false':
    errors=True

if config['buffs']['greaterarcaneelixir'].lower()=='true':
    spellpower+=int(constants['GAEPower'])
elif config['buffs']['greaterarcaneelixir'].lower()!='false':
    errors=True
    
if config['buffs']['flask'].lower()=='true':
    spellpower+=int(constants['flaskofsupremepower'])
elif config['buffs']['flask'].lower()!='false':
    errors=True

manapool=1240+(intellect*15)


if errors:
    raise Exception('\nBinary values in config.json must be "true" or "false"')

#Calculated dps:
nakedlb= ((int(constants['r10lbmindmg']) +int(constants['r10lbmaxdmg']))/2) * (1 +(int(constants['concussionpercent'])/100))
nakeddps=nakedlb/int(constants['lbcasttime'])
hadps=nakeddps*hit/100

spalb=nakedlb + (spellpower *float(constants['lbcoefficient']))
haspadps=(spalb/int(constants['lbcasttime'])) *hit/100

dpsfromcrits=haspadps*(int(constants['critmultiplier'])-1)*crit/100
estimateddps=haspadps + (dpsfromcrits)


print("\nCalculated character stats:")
print("Intellect: " +str(intellect))
print("Crit chance from intellect: " +str(critfromint))
print("Total crit chance: " +str(crit))
print("Hit chance: " +str(hit))
print("Spell power with flask/oil/pot: " +str(spellpower))
print("Average naked R10 Lightning Bolt hit: " +str(nakedlb))
print("Mana pool: " +str(manapool))

print("\nDPS Stats:")
print("Naked dps without hit or crit: " +str(nakeddps))
print("Hit adjusted dps: " +str(hadps))
print("Spell power adjusted average lightning bolt damage: " +str(spalb))
print("Spell power adjusted, hit adjusted dps: " +str(haspadps))

print("Bonus dps from crits: " +str(dpsfromcrits))
print("Estimated DPS: " +str(estimateddps))

print("\nBeginning Simulation")

mana=manapool
time=0
totaldamage=0
hits=0
crits=0
misses=0
lbcost=int(int(constants['r10lbcost']) - (int(constants['r10lbcost'])*int(constants['convectionpercent'])/100))
lbmin=int(constants['r10lbmindmg'])
lbmax=int(constants['r10lbmaxdmg'])
critmultiplier=float(constants['critmultiplier'])

while(mana>=lbcost):
    print("Lightning Bolt")
    damage=0
    mana-=lbcost
    time+=2
    #check for miss:
    missroll=random.randint(1,100)
    if missroll>hit:
        print('RESIST\nDamage 0')
        misses+=1
    else:
        #calculate damage
        damage=spellpower+random.randint(lbmin,lbmax)
        #check for crit
        critroll=random.randint(1,100)
        print(critroll)
        if critroll<=crit:
            print('CRIT')
            damage=damage*critmultiplier
            crits+=1
        else:
            print('Hit')
            hits+=1
        print('Damage ' +str(damage))
        totaldamage+=damage

print('OOM!')
print('\nTime to OOM: ' +str(time))
print('Hits: ' +str(hits))
print('Crits: ' +str(crits))
print('Misses: ' +str(misses))
print('Total damage: ' +str(totaldamage))
print('DPS: ' +str(totaldamage/time))
    