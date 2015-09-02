# PokeCompanion
#### A theory-crafting site for the Pokemon video games

## Interface
The interface consists of two Pokémon stat cards. To begin, enter a name in the 'Select Pokémon' field and hit 'FIND'.
    * NOTE: If the Pokémon does not exist in the database, it will take some time to load the data in.
     
Once the Pokémon is found, the stats will autopopulate. All stat fields have input disabled, only the fields under the 'EDIT' buttons, the Pokémon Level field, and the select boxes can be changed. These changes will then be calculated into the displayed stats.

If a move has been selected, an 'ATTACK' button and select box will appear so you can select a target and test the attack against it.
     * Note only standard damaging attacks are functional, attacks with specially calculated power values are not supported
     
## Server commands
In addition to standard Flask commands, there is a `populate.py` script to add Pokémon data into the database. Three options are avaliable:
* `populate.py name1 name2 ... nameN` will add the listed Pokémon
* `populate.py -a` or `populate --all` will add all possible Pokémon (as per the Bulbapedia listing)
     * WARNING: This is untested and will take a very long time
* `populate.py -u` or `populate.py --update` will update all Pokémon in the database
     * NOTE: Currently only moves are updated