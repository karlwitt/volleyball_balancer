#!/usr/bin/env python3

"""team_balance.py: Python script to take some inputs such as 
number of players, number of games desired to play, and game 
format such as 3v3, 4v4, etc. and optimizes team compensation"""

__author__      = "Karl Witthuhn"
__copyright__   = "Copyright 2023"

import os, sys
import getopt
import re
import itertools
import collections
import copy
import random
from itertools import combinations
from itertools import permutations
from collections import Counter
from typing import List, Tuple
import math

class teamSetup():
    """class001
    class to setup team composition based on inputs/args
    from the main() function
    """
    def __init__(self):
        pass

    def generate_unique_teams(self, players, total_players_per_game):
        """class001-func001
        Generate a list of unique combinations of players, given a number of
        players per game
        """
        fname = str(sys._getframe().f_code.co_name)
        try:
            unique_list = list(combinations(players, total_players_per_game))
        except Exception as err:
            print("Unknown error in function {}, details: {}".format(fname, err))
            sys.exit(1)
        finally:
            return unique_list

    def generate_final_combinations(self, players, players_per_team):
        """class001-func002
        Return a list of tuples of all combinations of players, given a 
        number of players per team, instead of per game.
        """
        fname = str(sys._getframe().f_code.co_name)
        try:
            all_combinations = list()
            team_comp_list = list()
            unique_teams_list = list()
            # Generate all unique teams
            unique_teams = self.generate_unique_teams(players, players_per_team)
            # We need to add a list of all unique teams to a list
            for t in unique_teams:
                # convert to a list
                t_list = list(t)
                unique_teams_list.append(t_list)
            # Now cycle through and make sure no 2 team compositions are unique
            for team1 in unique_teams_list:
                for team2 in unique_teams_list:
                    full_team = (team1 + list(set(team2) - set(team1)))
                    if len(full_team) == len(players):
                        team1_set = set(team1)
                        team2_set = set(team2)
                        if team1_set not in team_comp_list and team2_set not in team_comp_list:
                            team_comp_list.append(team1_set)
                            team_comp_list.append(team2_set)
                            all_combinations.append((team1, team2))
        except Exception as err:
            print("Unknown error in function {}, details: {}".format(fname, err))
            sys.exit(1)
        finally:
            return all_combinations
    def generate_team_pairings(self, player_count_dict, team_list):
        """class001-func003
        """
        fname = str(sys._getframe().f_code.co_name)
        try:
            team_pairings = [(a, b) for idx, a in enumerate(team_list) for b in team_list[idx + 1:]]
            ###################
            # Team Pairings
            ###################
            for team_pair in team_pairings:
                team_member_1 = team_pair[0]
                team_member_2 = team_pair[1]
                ###################
                # Team Member 1
                ###################
                if team_member_1 not in player_count_dict.keys():
                    player_dict = dict()
                    # add team_member_2 to the player_dict here
                    player_dict[team_member_2] = 1
                    player_count_dict[team_member_1] = player_dict
                else:
                    player_dict = player_count_dict[team_member_1]
                    # now check if team_member_2 is already in their dict or not
                    if team_member_2 in player_dict.keys():
                        player_dict[team_member_2] =  player_dict.get(team_member_2) + 1
                    else:
                        player_dict[team_member_2] = 1
                    player_count_dict[team_member_1] = player_dict
                ###################
                # Team Member 2
                ###################
                if team_member_2 not in player_count_dict.keys():
                    player_dict = dict()
                    # add team_member_1 to the player_dict here
                    player_dict[team_member_1] = 1
                    player_count_dict[team_member_2] = player_dict
                else:
                    player_dict = player_count_dict[team_member_2]
                    # now check if team_member_2 is already in their dict or not
                    if team_member_1 in player_dict.keys():
                        player_dict[team_member_1] =  player_dict.get(team_member_1) + 1
                    else:
                        player_dict[team_member_1] = 1
                    player_count_dict[team_member_2] = player_dict

        except Exception as err:
            print("Unknown error in function {}, details: {}".format(fname, err))
            sys.exit(1)
        finally:
            return player_count_dict

    def subtract_dicts(self, dict1, dict2):
        """class001-func004
        subtract the values of 1 dictionary from another dictionary
        """
        fname = str(sys._getframe().f_code.co_name)
        try:
            result = dict()
            for key1, inner_dict1 in dict1.items():
                result[key1] = {}
                for key2, value2 in inner_dict1.items():
                    result[key1][key2] = dict2[key1][key2] - value2
        except Exception as err:
            print("Unknown error in function {}, details: {}".format(fname, err))
            sys.exit(1)
        finally:
            return result

    def generate_min_max_dicts(self, dictionary):
        """class001-func005
        """
        fname = str(sys._getframe().f_code.co_name)
        try:
            max_value = max(dictionary.values())
            min_value = min(dictionary.values())
            max_dict = dict()
            min_dict = dict()

            for key, value in dictionary.items():
                if value == max_value:
                    max_dict[key] = value
                elif value == min_value:
                    min_dict[key] = value

        except Exception as err:
            print("Unknown error in function {}, details: {}".format(fname, err))
            sys.exit(1)
        finally:
            return (min_dict, max_dict)

def main():
    """main code block
    """
    fname = str(sys._getframe().f_code.co_name)
    try:
        # setup default opts
        opt_games, total_players_per_game = int(), int()
        opt_players = list()
        opt_team_size = str()
        # default to 2 teams
        opt_number_of_teams = int(2)

        (opts, args) = getopt.getopt(sys.argv[1:], "t:p:g:n:",
                ["team-size=", "players=", "games=", "number-of-teams="])
        for (o, a) in opts:
            if o in ["-t", "--team-size"]:
                opt_team_size = int(a)
            # we need to split players up by comma
            if o in ["-p", "--players"]:
                opt_arg_players = a
                opt_players = opt_arg_players.split(",")
            if o in ["-g", "--games"]:
                opt_games = a
            if o in ["-n", "--number-of-teams"]:
                opt_number_of_teams = int(a)

        current_dir = str(os.getcwdb().decode())
        
        ###############################
        # Sanity Check Section    
        ###############################
        # Let's create a list of valid team sizes
        supported_team_sizes = [2, 3, 4, 5, 6] 
        if opt_team_size not in supported_team_sizes:
            raise Exception("Error: -t/--team-size must be one of the following: {}, exiting...".format(",".join(supported_team_sizes)))

        # Gather total players that are playing in a game, as well as how many are available
        total_players_per_game = opt_number_of_teams * opt_team_size 
        number_of_players = len(opt_players)

        # We need to make sure that the number of players given can break into two even teams
        if len(opt_players) < total_players_per_game:
            raise Exception("\n-p/--players must be equal to or greater than the -t/--team-size players required. IE: `--team-size {}` needs {} players defined.\n".format(opt_team_size, total_players_per_game))

        ###############################
        # Team Setup Section
        ###############################
        ts = teamSetup()
        # Create a list that holds a count of all players that appear, we'll use this as a sanity check temporarily hopefully
        massive_list = list()
        final_team_tuple_list = list()
        # First, we need all combinations of unique teams, before we split them even further
        unique_teams = ts.generate_unique_teams(opt_players, total_players_per_game)
        # Create a team combination and match number counter
        team_comb, match_num = 1, 1
        # Create a dictionary to separate each team combination into sub-team combinations, to easily pick the correct ones later
        match_dict = dict()
        # NOTE: this here is the case where EVERY team combination is created
        # There's a good chance we don't want to print this out, but we use it for calculations in the 
        # "Team Balance" section
        #print("=== Full Match List ===\n")
        for u in unique_teams:
            # convert each unique combination (tuple) into a list
            u_list = list(u)
            # generate all combinations of this list of tuples
            final_team = ts.generate_final_combinations(u_list, opt_team_size)
            # create a dictionary for every set of teams
            final_team_dict = dict()
            single_team_count = 0
            for f in final_team:
                # we need to caclulate how many unique combos there are, within a single team, N
                final_team_tuple_list.append(f)
                final_team_dict["{}".format(match_num)] = f
                # create a list of team members for each tuple - team_1 is the 0 entry for tuple[f] and team_2 is the 1 entry for tuple[f]
                team_1 = list(f[0])
                team_2 = list(f[1])
                massive_list.extend(team_1)
                massive_list.extend(team_2)
                #print("\tMatch #{:3s} = ({}) VS. ({})".format(str(match_num), ' | '.join(team_1), ' | '.join(team_2)))
                # Add 1 to the match number and single team counters
                match_num += 1
                single_team_count += 1
            match_dict[team_comb] = final_team_dict
            # Add 1 to the team combination counter
            team_comb += 1
        
        ###############################
        # Team Balance Section
        ###############################
        # Now we have all of our team combinations, but how do we make it fair?
        # This will be a big challenge
        # First, we need to determine how many games we need overall 
        # If -n/--number-of-games is not specified, we'll go with the maximum possible
        if not opt_games:
            opt_games = (match_num - 1)
        # Calculate total number of matches that are possible and unqiue
        total_matches_possible = (match_num - 1)
        # Calculate how many different combinations of player sets there are
        total_player_combos_possible = (team_comb - 1)

        # Error out if someone specifies a higher number of games than what is possible
        if int(opt_games) > total_matches_possible:
            raise Exception("-g/--games must not exceed the maximum possible unique combinations of teams of: {}".format(total_matches_possible))
        if int(opt_games) % int(total_player_combos_possible) != 0:
            error_message = str("-g/--games must be a multiple of {}\n".format(total_player_combos_possible))
            error_message += str("For example:\n")
            x = 0
            while x < int(total_matches_possible):
                x += int(total_player_combos_possible)
                error_message += str("--games {}\n".format(x))
            raise Exception(error_message)
        
        # Calculate the multiple that we will use to ensure a balanced bracket
        max_team_count = int(total_matches_possible) / int(total_player_combos_possible)
        current_team_count = int(opt_games) / int(total_player_combos_possible) 
        # Finally, subtract current_team_count from max_team_count
        team_multiple = int(max_team_count - current_team_count)
        # We need a variable to track how many teams per sub-match we should select (potentially unused)
        picks_per_team = int(max_team_count - team_multiple)

        ############################
        # Variable Printout Section
        ############################
        #print("max_team_count = {}".format(max_team_count))
        #print("current_team_count = {}".format(current_team_count))
        #print("opt_games = {}".format(opt_games))
        #print("total_matches_possible = {}".format(total_matches_possible))
        #print("total_player_combos_possible = {}".format(total_player_combos_possible))
        #print("single_team_count = {}".format(single_team_count))
        #print("team_multiple = {}".format(team_multiple))
        #print("picks_per_team = {}".format(picks_per_team))
        # Calculate the total number of player occurances
        for player in opt_players:
            count_of_player = massive_list.count(player)
            #print("Player: ({}) appears in massive_list: {} times".format(player, count_of_player))
        teams = [team for tup in final_team_tuple_list for team in tup]
        team_counts = Counter(map(tuple, teams))
        # Create a list that tracks what teams have been present so far
        #print("=== Team Count Sanity Check ===\n")
        for team, count in team_counts.items():
            pass
            #print("Team = {} ; Count = {}".format(team, count))
        
        # let's set all others who we play with at 0 - so we can use min()/max()/>/< calls if needed
        player_count_dict = dict()
        final_team_list = list()
        for p in opt_players:
            player_count_dict_2 = dict()
            for p2 in opt_players:
                # skip ourselves 
                if p == p2:
                    continue
                player_count_dict_2[p2] = 0
            player_count_dict[p] = player_count_dict_2
        # now let's comb through each team combination and pick the most "fair" teams 
        # where possible
        for team_comb, team_comb_dict in sorted(match_dict.items()):
            # copy the player_count_dict so we can modify/compare it
            copy_player_count_dict = copy.deepcopy(player_count_dict)
            matchup_comps_added = 0
            test = list(team_comb_dict.items())
            random.shuffle(test)
            for matchup, matchup_comp in test:
                if matchup_comps_added >= picks_per_team:
                    continue
                team_1 = matchup_comp[0]
                team_2 = matchup_comp[1]
                team_added = False
                for t in team_1:
                    if team_added == True:
                        continue
                    t_dict = copy_player_count_dict[t]
                    (min_dict, max_dict) = ts.generate_min_max_dicts(t_dict) 
                    for t2 in team_1:
                        # skip ourselves
                        if t == t2 or team_added == True:
                            continue
                        # otherwise, check if the other teammates are part of the min dict, which we can safely add the entire set
                        if t2 in min_dict.keys() or len(min_dict) == 0:
                            final_team_list.append(matchup_comp)
                            matchup_comps_added += 1
                            team_added = True
                for t3 in team_2:
                    if team_added == True:
                        continue
                    t_dict = copy_player_count_dict[t3]
                    (min_dict, max_dict) = ts.generate_min_max_dicts(t_dict) 
                    for t4 in team_2:
                        # skip ourselves
                        if t3 == t4 or team_added == True:
                            continue
                        # otherwise, check if the other teammates are part of the min dict, which we can safely add the entire set
                        if t4 in min_dict.keys() or len(min_dict) == 0:
                            final_team_list.append(matchup_comp)
                            matchup_comps_added += 1
                            team_added = True
                # finish with updating the player_count_dicts for both teams
                player_count_dict = ts.generate_team_pairings(player_count_dict, team_1)
                player_count_dict = ts.generate_team_pairings(player_count_dict, team_2)

        ################################
        # Trimmed Team Calculations
        ################################
        massive_list_2 = list()
        match_num = 1
        print("=== Trimmed Match List ===\n")
        # Let's create a dictionary to see how many times a player is with another player
        player_count_dict = dict()
        for f in final_team_list:
            # create a list of team members for each tuple - team_1 is the 0 entry for tuple[f] and team_2 is the 1 entry for tuple[f]
            team_1 = list(f[0])
            team_2 = list(f[1])
            
            # let's get our player counts (AKA who plays with who) for each team
            player_count_dict = ts.generate_team_pairings(player_count_dict, team_1)
            player_count_dict = ts.generate_team_pairings(player_count_dict, team_2)

            # add both teams to our massive list (2nd version) for trimmed calculations later
            massive_list_2.extend(team_1)
            massive_list_2.extend(team_2)
            print("\tMatch #{:3s} = ({}) VS. ({})".format(str(match_num), ' | '.join(team_1), ' | '.join(team_2)))
            # add 1 to our match counter
            match_num += 1
        print("")
        ######################################
        # Sanity Check for who plays with who
        ######################################
        print("=== Player-to-Player Count Sanity Check ===\n")
        for player, player_dict in sorted(player_count_dict.items()):
            for partner, num_of_appearances in sorted(player_dict.items()):
                print("\tPlayer: ({}) --> Player ({}) {} Times".format(player, partner, num_of_appearances))
        print("")
        ######################################
        # Sanity Check for how many times each person plays
        ######################################
        print("=== Player Count Sanity Check ===\n")
        for player in opt_players:
            count_of_player = massive_list_2.count(player)
            print("\tPlayer: ({}) appears {} times".format(player, count_of_player))
        print("")
        ######################################
        # Sanity Check for how many times each team plays together
        ######################################
        teams = [team for tup in final_team_list for team in tup]
        team_counts = Counter(map(tuple, teams))
        print("=== Team Count Sanity Check ===\n")
        for team, count in team_counts.items():
            print("\tTeam = {} ; Count = {}".format(team, count))
        print("")

    except Exception as err:
        print("Error in function {}, details:\n{}".format(fname, err))
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print("Unknown error {}, exiting".format(err))
        sys.exit(1)

# vim: sw=4 sts=4 et ts=4
