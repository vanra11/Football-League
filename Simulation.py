import random

class Player:
    def __init__(self, name, position, team):
        self.name = name
        self.position = position
        self.team = team
        self.points = 0
        self.yellow_cards = 0
        self.red_cards = 0
        self.suspension_games = 0  # Tracks the number of games a player is suspended
    
    def update_points(self, performance):
        if performance.get('minutes_played', 0) >= 60:
            self.points += 2
        else:
            self.points += 1
        
        if self.position == 'Goalkeeper' and performance.get('goals', 0) > 0:
            self.points += 10
        elif self.position == 'Defender' and performance.get('goals', 0) > 0:
            self.points += 6
        elif self.position == 'Midfielder' and performance.get('goals', 0) > 0:
            self.points += 5
        elif self.position == 'Forward' and performance.get('goals', 0) > 0:
            self.points += 4
        
        # Deduct points for cards
        self.points -= self.yellow_cards  # -1 point for each yellow card
        self.points -= (self.red_cards * 2)  # -2 points for each red card

    def receive_card(self, card_type):
        if card_type == 'yellow':
            if self.yellow_cards < 2:  # A player can receive a max of 2 yellow cards in one game
                self.yellow_cards += 1
            if self.yellow_cards == 2:  # 2 yellow cards lead to a suspension
                self.suspension_games += 1
        elif card_type == 'red':
            self.red_cards += 1
            self.suspension_games += 2  # 1 red card leads to suspension for 2 games

class Team:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.total_goals_scored = 0
        self.total_goals_conceded = 0
        self.matches_won = 0
        self.matches_drawn = 0
        self.matches_lost = 0
        self.total_match_points = 0  # Points from match results
        self.monthly_points = [0] * 12  # Points per month
        self.matches_played = 0  # Tracks the number of matches played
        self.total_cards_received = 0  # Track total cards received by the team
    
    def add_player(self, player):
        if len(self.players) < 15:
            self.players.append(player)
    
    def calculate_total_points(self):
        return sum(player.points for player in self.players)
    
    def add_match_result(self, goals_scored, goals_conceded, month):
        self.total_goals_scored += min(goals_scored, 70)
        self.total_goals_conceded += min(goals_conceded, 30)
        self.total_goals_scored = min(self.total_goals_scored, 70)
        self.total_goals_conceded = min(self.total_goals_conceded, 30)

        if goals_scored > goals_conceded:
            self.matches_won += 1
            self.total_match_points += 3
        elif goals_scored == goals_conceded:
            self.matches_drawn += 1
            self.total_match_points += 1
        else:
            self.matches_lost += 1
        
        self.monthly_points[month] += self.total_match_points
        self.matches_played += 1
    
    def calculate_additional_score(self):
        K = 3
        G = 2
        M = 1
        return (K * self.matches_won) + (G * self.total_goals_scored) - (M * self.total_goals_conceded)

    def normalize_points(self):
        return sum(self.monthly_points) / 12

class Match:
    def __init__(self, teams, month):
        self.teams = teams  # List of two teams
        self.month = month
    
    def simulate(self):
        team1, team2 = self.teams
        goals_team1 = random.randint(0, 6)
        goals_team2 = random.randint(0, 6)
        
        team1.add_match_result(goals_team1, goals_team2, self.month)
        team2.add_match_result(goals_team2, goals_team1, self.month)
        
        # Select players for card assignment
        players_for_cards = random.sample(team1.players, k=random.randint(1, 2)) + \
                           random.sample(team2.players, k=random.randint(1, 2))
        
        # Assign cards to selected players at a frequency of 1 card per 4 games
        if random.random() < (1 / 4):
            for player in players_for_cards:
                card_type = random.choice(['yellow', 'red'])
                player.receive_card(card_type)
                team1.total_cards_received += 1 if card_type == 'yellow' else 2
                team2.total_cards_received += 1 if card_type == 'yellow' else 2
        
        # Simulate performance for all players
        for player in team1.players + team2.players:
            if player.suspension_games > 0:
                player.suspension_games -= 1  # Reduce suspension games
                continue  # Skip point update if suspended
            
            # Simulate performance
            performance = {
                'minutes_played': random.randint(30, 90),
                'goals': random.randint(0, 2),
                'assists': random.randint(0, 1)
            }
            player.update_points(performance)

class League:
    def __init__(self, teams):
        self.teams = teams
    
    def simulate_season(self):
        num_matches_per_team = 14
        all_matches = []
        for i in range(len(self.teams)):
            for j in range(i + 1, len(self.teams)):
                team1 = self.teams[i]
                team2 = self.teams[j]
                # Schedule matches to ensure each team plays 14 matches
                while team1.matches_played < num_matches_per_team and team2.matches_played < num_matches_per_team:
                    all_matches.append((team1, team2))
                    team1.matches_played += 1
                    team2.matches_played += 1
        
        random.shuffle(all_matches)  # Randomize match order
        month = 0
        for match in all_matches:
            if month >= 12:
                month = 0
            Match(match, month).simulate()
            month += 1

    def get_winner(self):
        return max(self.teams, key=lambda team: team.calculate_additional_score() + team.total_match_points)

    def get_most_least_cards(self):
        most_cards_team = max(self.teams, key=lambda team: team.total_cards_received)
        least_cards_team = min(self.teams, key=lambda team: team.total_cards_received)
        return most_cards_team, least_cards_team

# Main function to simulate the program
def main():
    # Create players and teams
    teams = []
    team_names = [
        "Manchester United", "Liverpool", "Manchester City", "Arsenal",
        "Chelsea", "Tottenham Hotspur", "FC Barcelona", "Real Madrid",
        "Atlético Madrid", "Inter Milan", "AC Milan", "Juventus"
    ]
    
    for team_name in team_names:
        team = Team(team_name)
        for i in range(15):
            position = random.choice(["Forward", "Midfielder", "Defender", "Goalkeeper"])
            player = Player(f"Player {i+1} of {team_name}", position, team_name)
            team.add_player(player)
        teams.append(team)
    
    # Create a league
    league = League(teams)
    
    # Simulate the season
    league.simulate_season()
    
    # Get the winner
    winner = league.get_winner()
    if winner:
        print(f"The winner is: {winner.name} with {winner.calculate_additional_score()} ovr")
        print(f"Total points scored: {winner.total_match_points} match points.")
        print(f"Goals Scored: {winner.total_goals_scored}, Goals Conceded: {winner.total_goals_conceded}")
        print(f"Matches Won: {winner.matches_won}, Matches Drawn: {winner.matches_drawn}, Matches Lost: {winner.matches_lost}")
    
    # Get teams with most and least cards
    most_cards_team, least_cards_team = league.get_most_least_cards()
    #print(f"Team with the most cards: {most_cards_team.name} with {most_cards_team.total_cards_received} cards.")
    print(f"Fairplay Award: {least_cards_team.name} with {least_cards_team.total_cards_received} cards.")

# Run the simulation
main()


#Hypothetical situation
#Compiled by Arnav Chourey
