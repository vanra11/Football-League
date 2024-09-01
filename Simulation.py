import random

class Player:
    def __init__(self, name, position, team):
        self.name = name
        self.position = position
        self.team = team
        self.points = 0
        self.yellow_cards = 0
        self.red_cards = 0
        self.suspended_games = 0
    
    def update_points(self, performance):
        if self.suspended_games > 0:
            self.suspended_games -= 1
            return  # Skip updating points if player is suspended
        
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

    def receive_yellow_card(self):
        self.yellow_cards += 1
        self.points -= 1
        if self.yellow_cards == 3:
            self.suspended_games = 1
            self.yellow_cards = 0  # Reset yellow cards after suspension

    def receive_red_card(self):
        self.red_cards += 1
        self.points -= 2
        self.suspended_games = 2  # 2-game suspension for a red card

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
        self.total_yellow_cards = 0
        self.total_red_cards = 0
    
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
        K = 1.5
        G = 1.5
        M = 0.5
        return (K * self.matches_won) + (G * self.total_goals_scored) - (M * self.total_goals_conceded)

    def normalize_points(self):
        return sum(self.monthly_points) / 12
    
    def receive_card(self, card_type):
        if card_type == "yellow":
            self.total_yellow_cards += 1
        elif card_type == "red":
            self.total_red_cards += 1

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
        
        # Handle pre-defined card recipients
        self.assign_predefined_cards(team1, team2)
        
        # Random card assignments to other players
        self.assign_random_cards(team1, team2)
        
        # Simulate performance and update points for all players
        for player in team1.players + team2.players:
            performance = {
                'minutes_played': random.randint(30, 90),
                'goals': random.randint(0, 2),
                'assists': random.randint(0, 1)
            }
            player.update_points(performance)

    def assign_predefined_cards(self, team1, team2):
        for team in [team1, team2]:
            predefined_players = random.sample(team.players, random.randint(1, 2))
            for player in predefined_players:
                self.assign_card_to_player(player, team)

    def assign_random_cards(self, team1, team2):
        for team in [team1, team2]:
            if random.random() < 0.25:  # 25% chance of giving a card to any random player
                player = random.choice(team.players)
                self.assign_card_to_player(player, team)

    def assign_card_to_player(self, player, team):
        card_type = random.choice(["yellow", "red"])
        if card_type == "yellow":
            if player.yellow_cards < 2:  # Ensure a player can't get more than 2 yellow cards in a game
                player.receive_yellow_card()
                team.receive_card("yellow")
        elif card_type == "red":
            if player.red_cards == 0:  # Ensure a player can't get both yellow and red in the same game
                player.receive_red_card()
                team.receive_card("red")

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
    
    def get_most_least_carded_teams(self):
        most_yellow_cards_team = max(self.teams, key=lambda team: team.total_yellow_cards)
        least_yellow_cards_team = min(self.teams, key=lambda team: team.total_yellow_cards)
        most_red_cards_team = max(self.teams, key=lambda team: team.total_red_cards)
        least_red_cards_team = min(self.teams, key=lambda team: team.total_red_cards)
        
        return most_yellow_cards_team, least_yellow_cards_team, most_red_cards_team, least_red_cards_team

    def display_standings(self):
        print(f"{'Team Name':<20}{'Games Played':<15}{'Won':<6}{'Drawn':<6}{'Lost':<6}{'Goals Scored':<15}{'Goals Conceded':<17}{'Total Points':<13}")
        print("-" * 105)
        for team in sorted(self.teams, key=lambda x: (x.total_match_points, x.total_goals_scored), reverse=True):
            print(f"{team.name:<20}{team.matches_played:<15}{team.matches_won:<6}{team.matches_drawn:<6}{team.matches_lost:<6}{team.total_goals_scored:<15}{team.total_goals_conceded:<17}{team.total_match_points:<13}")

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
    
    # Create a league and simulate the season
    league = League(teams)
    league.simulate_season()
    
    # Display the league standings
    league.display_standings()

if __name__ == "__main__":
    main()



#Compiled by Arnav Chourey
