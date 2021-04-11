# Nim game
## Team name : Quantronauts
### Team members
<table>
	<thead>
		<tr>
			<th align="center">Members</th>
			<th align="center">email@</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td align="center">Michael Rollin</td>
			<td align="center">mika89700@[...]</td>
		</tr>
		<tr>
			<td align="center">Sahar Ben Rached</td>
			<td align="center">sahar.benrached1@[...]</td>
		</tr>
		<tr>
			<td align="center">Alain Chancé</td>
			<td align="center">alain.chance@[...]</td>
		</tr>
		<tr>
			<td align="center">Tamas Varga</td>
			<td align="center">varga78t@[...]</td>
		</tr>
    <tr>
			<td align="center">Laurent Querella</td>
			<td align="center">lquerella@[...]</td>
		</tr>
	</tbody>
</table>

## Game
### Running the game
To run the program just launch : `python3 nim_game.py`

### Rules
This game is inspiring from the [Nim game](https://en.wikipedia.org/wiki/Nim). You are 2 players face to face, you have 11 sticks in front of you :
<pre>
          \o/
           |
          / \
#######################
 | | | | | | | | | | | 
#######################
          \ /
           |
          /o\
</pre>
The goal is **NOT** take the last stick !!
Originally, this game can be automatize by classical computer to always loose again a computer or against someone knowing [the strategy](https://en.wikipedia.org/wiki/Modular_arithmetic#Congruence).
But what happens if we implement quantum rules ?

Like the original game each player can take 1 to 3 sticks each turn but this time, they can say if they want to take the stick normally, put it in superposition or creating an entanglement between this stick and the sticks previously on the board (played before) :
<table>
	<thead>
		<tr>
			<th align="center">Symbols table</th>
			<th align="center">name</th>
			<th align="center">means</th>
			<th align="center">action possible ?</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td align="center">|</td>
			<td align="center">stick left</td>
			<td align="center">a simple sticks</td>
			<td align="center">any action</td>
		</tr>
		<tr>
			<td align="center">/</td>
			<td align="center">superposition stick</td>
			<td align="center">sticks in states : |0> + |1></td>
			<td align="center">no action (only here for info)</td>
		</tr>
		<tr>
			<td align="center">¬</td>
			<td align="center">entangle stick</td>
			<td align="center">the faith of this stick depends of the previous one</td>
			<td align="center">no action (only here for info)</td>
		</tr>
		<tr>
			<td align="center">[ ]</td>
			<td align="center">blank space</td>
			<td align="center">the previous stick has been fully taken</td>
			<td align="center">an cx action can be done with if it's not the first turn of the circuit generation</td>
		</tr>
	</tbody>
</table>

Here each stick correspond to a qubit at the `|0>` state.

Example of a game :
11 sticks in board : `| | | | | | | | | | |`  
1st turn :  
Robin choose 2 sticks
  - Robin apply an x gate the 11th stick
  - Robin apply an h gate to the 10th stick

9 sticks in board : `| | | | | | | | | /`  
Batman choose 3 sticks  
  - Batman apply a cx to the 9th stick (now the 9th stick is automatically link with the 10th)
  - Batman apply a x gate to the 8th stick
  - Batman apply a x gate to the 7th stick

6 sticks in board : `| | | | | |`

etc ...

2 sticks left : `| | ¬`  
Robin choose 1 sticks
  - Robin apply an x gate to the 2nd stick

1 sticks left : `|`  
Batman choose 1 sticks
  - Batman apply an x gate to the last stick

When it doesn't have a stick anymore we run the circuit we create with the gates and get the result, for each qubit still at the state `|0>` we had 1 stick left.
Then we continue wit the sticks remaning until we don't have stick at all after running the circuit.

### Modes
#### 2 players
A 2 players mode is available is you want to play with a friend or with your cat
#### 1 player
A 1 player is available and you'll fight against a quantum ia made with Grover with inside the modulo 4 classical algorythm.

--> **Explanation coming soon !***

<pre>
q0|0>  ---------------------------------

q1|0>  ---------------------------------

q2|0>  ---------------------------------

q3|0>  ---------------------------------

psi|+> ---------------------------------
</pre>

