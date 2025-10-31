# Advanced-Topics-in-CS 
This is the code for my Advanced Topics in CS project

The code can be run in k shortest path mode using:

python3 driver_competent.py --budget 1 --start 20 --fn adsim05 --algo ksp --k 2

or it can be run in its other modes using:

python3 honeypot/driver_competent.py --budget 10 --start 20 --fn adsim05 --algo mixed_attack

--algo:

mixed_attack: mip for the joint problem of competent and simple attacker
greedy_flat: greedy algorithm for simple attacker
greedy_competent: greedy algorithm for competent attacker

Note these modes and a large majority of the code was not developed by me. The k shortest path algorithm is an extension of the existing honeypot placement algorithm which can be found at:

https://github.com/huyqngo/honeypot_proj 
