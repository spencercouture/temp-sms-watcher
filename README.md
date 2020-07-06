This repository was forked in order to make changes so it better fits our internal program architecture. Particularly, we needed to get a list of all available numbers rather than grabbing a random one.

# temp-sms-watcher

It's just a wrapper for smsreceivefree.com that provide online phone number to receive sms.

https://smsreceivefree.com

## Usage

### Fetch a temporary number
```
python tempsms.py --country=canada|united-kingdom|usa
```

### Watch that number for new sms
```
python tempsms.py --check=yournumber(without +)
```

### Change pattern and timeRange
Open tempsms.py and change
```
global pattern, timeRange
pattern = ''
timeRange = 120
```
