print("Elemental Shaman simulator v0.1 beta")

import json
import random
import statistics as stats

#ToDo:
#Each cast type needs cleaning up to prevent duplication


#define functions
def stringtobool(string):
	if string.lower()=='true':
		return True
	elif string.lower()!='false':
		raise Exception('Boolean values in JSON must be "True" or "False"')
	else:
		return False

def verbose_print(text,verbose=False):
	if verbose:
		print(text)

def cast_spell(dmgmin, dmgmax, spellpower, hit, crit, critmultiplier, guaranteedcrit=False):
	damage=0;
	missroll=random.randint(1,100)
	#assume miss and change if otherwise
	hittype='MISS'
	if missroll<hit:
		#calculate damage
		damage=spellpower+random.randint(dmgmin,dmgmax)
		#print(str(spellpower) +'+(' +str(dmgmin) +'-' +str(dmgmax) +')')
		#check for crit
		critroll=random.randint(1,100)
		if critroll<=crit:
			damage=damage*critmultiplier
			hittype='CRIT'
		else:
			hittype='Hit'
	return hittype,damage;
	

###BEGIN MAIN###

#Load configs
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
print("Clearcasting: " +config['spec']['clearcasting'])
print("Arcane Brilliance Buff used: " +config['buffs']['arcanebrilliance'])
print("Gift Of The Wild Buff used: " +config['buffs']['giftofthewild'])
print("Brilliant Wizard Oil used: " +config['buffs']['brilliantwizardoil'])
print("Greater Arcane Elixir used: " +config['buffs']['greaterarcaneelixir'])
print("Flask of Supreme Power used: " +config['buffs']['flask'])
print("Troll Berserking: " +config['spec']['troll berserking'])




#Calculated char stats:
#intellect=baseintellect+arcanebrillianceint+giftofthewildint
intellect=int(config['gear']['baseintellect'])
if stringtobool(config['buffs']['arcanebrilliance']):
    intellect+=int(constants['arcanebrillianceint'])
    
if stringtobool(config['buffs']['giftofthewild']):
    intellect+=int(constants['giftofthewildint'])
    

critfromint=intellect/float(constants['intpercrit'])
crit=critfromint +float(config['spec']['critfromtalents']) +float(config['gear']['critfromitems'])
hit=int(constants['basehitpercent']) +int(config['spec']['hitfromtalents']) +int(config['gear']['hitfromitems'])

#hit cap innit
if hit > 99:
    hit=99

spellpower=int(config['gear']['basespellpower']) 
if stringtobool(config['buffs']['brilliantwizardoil']):
    spellpower+=int(constants['brilliantwizardoilpower'])
    crit+=float(constants['brilliantwizardoilcrit'])

if stringtobool(config['buffs']['greaterarcaneelixir']):
    spellpower+=int(constants['GAEPower'])
    
if stringtobool(config['buffs']['flask']):
    spellpower+=int(constants['flaskofsupremepower'])
	
chainlightning=stringtobool(config['config']['chain lightning'])
clearcasting=stringtobool(config['spec']['clearcasting'])
verbose= stringtobool(config['config']['verbose'])



#Calculated dps:
manapool=1240+(intellect*15)

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
print("Spell power adjusted, hit adjusted lightning boltdps: " +str(haspadps))

print("Bonus dps from crits: " +str(dpsfromcrits))
print("Estimated DPS: " +str(estimateddps))

print("\nBeginning Simulation with the following parameters:")

#init run:

r10lbcost=int(int(constants['r10lbcost']) - (int(constants['r10lbcost'])*int(constants['convectionpercent'])/100))
r10lbmin=int(constants['r10lbmindmg'])
r10lbmax=int(constants['r10lbmaxdmg'])
r4lbcost=int(int(constants['r4lbcost']) - (int(constants['r4lbcost'])*int(constants['convectionpercent'])/100))
r4lbmin=int(constants['r4lbmindmg'])
r4lbmax=int(constants['r4lbmaxdmg'])
clcost=int(int(constants['r4clcost']) - (int(constants['r4clcost'])*int(constants['convectionpercent'])/100))
clmin=int(constants['r4clmindmg'])
clmax=int(constants['r4clmaxdmg'])
critmultiplier=float(constants['critmultiplier'])
fightlength=int(config['config']['fight length'])
numberofruns=int(config['config']['number of runs'])
mp5=int(config['gear']['mp5'])
spiritpertick=15+(int(int(config['gear']['spirit'])/5))
downrank=int(config['config']['downrank percent'])
lbpower=int(spellpower*float(constants['lbcoefficient']))
clpower=int(spellpower*float(constants['clcoefficient']))


print("Fight Length: " +str(fightlength))
print("Number of Runs(not implemented): " +str(numberofruns))
print("Verbose: " +str(verbose))

DPSes =[]
for run in range(1,numberofruns+1):
	mana=manapool
	time=0
	totaldamage=0
	casts=0
	hits=0
	crits=0
	misses=0
	manapotcooldown=0
	runecooldown=0
	mp5tick=0
	timespentoom=0
	fivesecondrule=True
	spirittick=0
	clearcastingproc=False
	ccprocs=0
	clcooldown=0
	while(time<fightlength):
		#Action decision tree:
		#1. Pop cooldowns if they are available
		#2a. Cast R4 lightning bolt if we are in downranking state
		#2.b. Cast chain lightning if it's available
		#2.c. Cast R10 lightning bolt if it's available
		#2.d. Wait 5 seconds if we are oom
		#3. Pop mana pot or rune if we are low on mana
		#4. Tick mp5 if appropriate
		
		#Pop cooldowns if they are available:
		
		
		#Downrank if mana is below threshold and we have enough mana
		if mana/manapool*100<=downrank and mana>=r4lbcost:
			verbose_print("\nLightning Bolt R4", verbose)
			casts+=1
			if clearcastingproc:
				verbose_print('Clearcasting proc', verbose)
				clearcastingproc=False
			else:
				mana-=r4lbcost
			time+=2
			manapotcooldown-=2
			runecooldown-=2
			clcooldown-=2
			mp5tick+=2
			fivesecondrule=True
			hittype,damage= cast_spell(r4lbmin, r4lbmax, lbpower, hit, crit, critmultiplier)
			verbose_print(hittype, verbose)
			verbose_print('Damage ' + str(damage), verbose)
			totaldamage+=damage
			if hittype=='Hit':
				hits+=1
			elif hittype=='CRIT':
				crits+=1
			elif hittype=='MISS':
				misses+=1
			#generate clearcasting procs
			if clearcasting:
				proc=random.randint(1,10)
				if proc==1:
					clearcastingproc=True
					ccprocs+=1
		#Cast chain lightning if it's being used and off cooldown and enough mana and we're not downranking:
		elif chainlightning and clcooldown<=0 and mana>=clcost:
			verbose_print("\nChain Lightning", verbose)
			casts+=1
			if clearcastingproc:
				verbose_print('Clearcasting proc', verbose)
				clearcastingproc=False
			else:
				mana-=clcost
			time+=1.5
			manapotcooldown-=1.5
			runecooldown-=1.5
			mp5tick+=1.5
			fivesecondrule=True
			clcooldown=6
			
			hittype,damage= cast_spell(clmin, clmax, clpower, hit, crit, critmultiplier)
			verbose_print(hittype, verbose)
			verbose_print('Damage ' + str(damage), verbose)
			totaldamage+=damage
			if hittype=='Hit':
				hits+=1
			elif hittype=='CRIT':
				crits+=1
			elif hittype=='MISS':
				misses+=1
			#generate clearcasting procs
			if clearcasting:
				proc=random.randint(1,10)
				if proc==1:
					clearcastingproc=True
					ccprocs+=1
		#Normal lightning bolt:
		elif mana>=r10lbcost:
			verbose_print("\nLightning Bolt R10", verbose)
			casts+=1
			if clearcastingproc:
				verbose_print('Clearcasting proc', verbose)
				clearcastingproc=False
			else:
				mana-=r10lbcost
			time+=2
			manapotcooldown-=2
			runecooldown-=2
			clcooldown-=2
			mp5tick+=2
			fivesecondrule=True
			#check for miss:
			hittype,damage= cast_spell(r10lbmin, r10lbmax, lbpower, hit, crit, critmultiplier)
			verbose_print(hittype, verbose)
			verbose_print('Damage ' + str(damage), verbose)
			totaldamage+=damage
			if hittype=='Hit':
				hits+=1
			elif hittype=='CRIT':
				crits+=1
			elif hittype=='MISS':
				misses+=1
			#check for clearcasting procs	
			if clearcasting:
				proc=random.randint(1,10)
				if proc==1:
					clearcastingproc=True
					ccprocs+=1
		else:
		#If not enough mana, progress time by 5 seconds then try again
		#ToDo: include spirit mana restore here
			verbose_print('\nOOM', verbose)
			time+=5
			manapotcooldown-=5
			runecooldown-=5
			clcooldown-=5
			mp5tick+=5
			timespentoom+=5
			#if we're not casting then we can have a spirit tick(unless this is the first 5 seconds since we last cast a spell)
			if fivesecondrule is True:
				fivesecondrule=False
			else:
				#Spirit ticks every 2 seconds
				spirittick+=5
				while spirittick>=2:
					verbose_print('spirittick+=' +str(spiritpertick), verbose)
					mana+=spirittick
					spirittick-=2
			
		#Use mana pot and/or demonic rune if it's off cooldown and enough mana is spent
		if manapotcooldown<=0 and manapool-mana>2250:
			pot=random.randint(1350,2250)
			verbose_print('Major Mana Potion used, restored ' +str(pot) +' mana', verbose)
			mana+=pot
			manapotcooldown=120
			
		if runecooldown<=0 and manapool-mana>1500:
			rune=random.randint(900,1500)
			verbose_print('Rune used, restored ' +str(rune) +' mana', verbose)
			mana+=rune
			runecooldown=120
			
		#add mp5 mana if ticked
		if mp5tick>=5:
			verbose_print('mp5tick', verbose)
			mana+=mp5
			mp5tick-=5
			
	print('\n***Report for run ' +str(run) + '***')
	print("Fight Length: " +str(fightlength))
	print('Casts: ' +str(casts))
	print('Hits: ' +str(hits))
	print('Crits: ' +str(crits))
	print('Misses: ' +str(misses))
	print('Clearcasting procs: ' +str(ccprocs))
	print('Total damage: ' +str(totaldamage))
	print('DPS: ' +str(int(totaldamage/time)))
	DPSes.append(int(totaldamage/time))
	print('Time spent OOM: ' +str(timespentoom) +'s')
    

print('*****FINAL REPORT*****')
print(DPSes)
averagedps=int(sum(DPSes)/len(DPSes))
mediandps=int(stats.median(DPSes))
variance=int(stats.variance(DPSes))
mindps=min(DPSes)
maxdps=max(DPSes)
print('Min DPS: ' +str(mindps))
print('Max DPS: ' +str(maxdps))
print('Average DPS: ' +str(averagedps))
print('Median DPS: ' +str(mediandps))
print('Variance: ' +str(variance))