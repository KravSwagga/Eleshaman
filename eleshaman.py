print("Elemental Shaman simulator v0.1 beta")

import json
import random

#Load constants
with open('constants.json') as json_file:
    constants = json.load(json_file)
    
with open('config.json') as json_file:
    config = json.load(json_file)

print(config)

print("\nConfig:")
print("Base Spell Power: " +config['gear']['basespellpower'])
print("Spell Crit From Talents: " +config['spec']['critfromtalents'])
print("Spell Crit From Items: " +config['gear']['critfromitems'])
print("Base Intellect: " +config['gear']['baseintellect'])
print("Spell Hit From Talents: " +config['spec']['hitfromtalents'])
print("Spell Hit From Items: " +config['gear']['hitfromitems'])
print("Mana per 5 seconds: " +config['gear']['mp5'])
print("Spirit: " +config['gear']['spirit'])
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

print("\nBeginning Simulation with the following parameters:")

mana=manapool
time=0
totaldamage=0
casts=0
hits=0
crits=0
misses=0
lbcost=int(int(constants['r10lbcost']) - (int(constants['r10lbcost'])*int(constants['convectionpercent'])/100))
lbmin=int(constants['r10lbmindmg'])
lbmax=int(constants['r10lbmaxdmg'])
critmultiplier=float(constants['critmultiplier'])
fightlength=int(config['config']['fight length'])
numberofruns=int(config['config']['number of runs'])
manapotcooldown=0
runecooldown=0
mp5=int(config['gear']['mp5'])
mp5tick=0
timespentoom=0
fivesecondrule=True
spirittick=0
spiritpertick=15+(int(int(config['gear']['spirit'])/5))

print("Fight Length: " +str(fightlength))

while(time<fightlength):
	#Cast lightning bolt if enough mana:
	if mana>=lbcost:
		print("\nLightning Bolt")
		casts+=1
		damage=0
		mana-=lbcost
		time+=2
		manapotcooldown-=2
		runecooldown-=2
		mp5tick+=2
		#check for miss:
		missroll=random.randint(1,100)
		fivesecondrule=True
		if missroll>hit:
			print('RESIST\nDamage 0')
			misses+=1
		else:
			#calculate damage
			damage=spellpower+random.randint(lbmin,lbmax)
			#check for crit
			critroll=random.randint(1,100)
			if critroll<=crit:
				print('CRIT')
				damage=damage*critmultiplier
				crits+=1
			else:
				print('Hit')
				hits+=1
			print('Damage ' +str(damage))
			totaldamage+=damage
	else:
	#If not enough mana, progress time by 5 seconds then try again
	#ToDo: include spirit mana restore here
		print('\nOOM')
		time+=5
		manapotcooldown-=5
		runecooldown-=5
		mp5tick+=5
		timespentoom+=5
		#if we're not casting then we can have a spirit tick(unless this is the first 5 seconds since we last cast a spell)
		if fivesecondrule is True:
			fivesecondrule=False
		else:
			#Spirit ticks every 2 seconds
			spirittick+=5
			while spirittick>=2:
				print('spirittick+=' +str(spiritpertick))
				mana+=spirittick
				spirittick-=2
		
	#Use mana pot and/or demonic rune if it's off cooldown and enough mana is spent
	if manapotcooldown<=0 and manapool-mana>2250:
		pot=random.randint(1350,2250)
		print('Major Mana Potion used, restored ' +str(pot) +' mana')
		mana+=pot
		manapotcooldown=120
		
	if runecooldown<=0 and manapool-mana>1500:
		rune=random.randint(900,1500)
		print('Rune used, restored ' +str(rune) +' mana')
		mana+=rune
		runecooldown=120
		
	#add mp5 mana if ticked
	if mp5tick>=5:
		print('mp5tick')
		mana+=mp5
		mp5tick-=5
		
print('\n***Final report***')
print('Casts: ' +str(casts))
print('Hits: ' +str(hits))
print('Crits: ' +str(crits))
print('Misses: ' +str(misses))
print('Total damage: ' +str(totaldamage))
print('DPS: ' +str(totaldamage/time))
print('Time spent OOM: ' +str(timespentoom))
    
