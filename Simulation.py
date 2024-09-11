import random
import matplotlib.pyplot as plt
import numpy as np

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

    def display_standings(self):
        print(f"{'Team Name':<20}{'Games Played':<15}{'Won':<6}{'Drawn':<6}{'Lost':<6}{'Goals Scored':<15}{'Goals Conceded':<17}{'Total Points':<13}")
        print("-" * 105)
        for team in sorted(self.teams, key=lambda x: (x.total_match_points, x.total_goals_scored), reverse=True):
            print(f"{team.name:<20}{team.matches_played:<15}{team.matches_won:<6}{team.matches_drawn:<6}{team.matches_lost:<6}{team.total_goals_scored:<15}{team.total_goals_conceded:<17}{team.total_match_points:<13}")

        # Create a histogram of points scored by each team
        team_points = [team.total_match_points for team in self.teams]
        team_names = [team.name for team in self.teams]
        plt.hist(team_points, bins=10, edgecolor='black')
        plt.xlabel('Points')
        plt.ylabel('Frequency')
        plt.title('Distribution of Points Scored by Each Team')
        plt.xticks(range(min(team_points), max(team_points) + 1))
        plt.yticks(range(max(team_points) + 1))
        plt.show()

    def __init__(self, teams):
        self.teams = teams
    
    def __init__(self, teams):
        self.teams = teams
    
    def simulate_season(self):
        num_matches_per_team = 28  # Updated to 28 matches per team
        all_matches = []
        for i in range(len(self.teams)):
            for j in range(len(self.teams)):
                if i != j:  # Ensure a team does not play itself
                    all_matches.append((self.teams[i], self.teams[j]))
        
        random.shuffle(all_matches)  # Randomize match order
        month = 0
        match_count = 0
        while match_count < len(all_matches):  # Ensure enough matches are played
            for match in all_matches:
                if month >= 12:
                    month = 0
                Match(match, month).simulate()
                month += 1
                match_count += 1
                if match_count >= num_matches_per_team * len(self.teams) / 2:
                    break

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

    teams_sorted = sorted(teams, key=lambda team: team.name)
    team_names_sorted = [team.name for team in teams_sorted]
    total_points_sorted = [team.total_match_points for team in teams_sorted]
    total_goals_sorted = [team.total_goals_scored for team in teams_sorted]
    
    x = np.arange(len(team_names_sorted))  # label locations
    width = 0.15  # width of the bars

    fig, ax = plt.subplots(figsize=(12, 6))

    # Create bars for total match points and total goals scored
    rects1 = ax.bar(x - width/2, total_points_sorted, width, label='Total Points', color='lightgreen')
    rects2 = ax.bar(x + width/2, total_goals_sorted, width, label='Goals Scored', color='skyblue')

    # Add labels and title
    ax.set_xlabel('Teams')
    ax.set_ylabel('Points / Goals')
    ax.set_title('Total Points and Goals Scored by Team (Alphabetical Order)')
    ax.set_xticks(x)
    ax.set_xticklabels(team_names_sorted, rotation=45, ha="right")
    ax.legend()

    # Display bar values on top of the bars
    def autolabel(rects):
        """Attach a text label above each bar."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    plt.tight_layout()
    plt.show()

    # Generate another grouped bar chart for matches won, lost, and drawn
    total_wins_sorted = [team.matches_won for team in teams_sorted]
    total_draws_sorted = [team.matches_drawn for team in teams_sorted]
    total_losses_sorted = [team.matches_lost for team in teams_sorted]

    fig, ax = plt.subplots(figsize=(12, 6))

    # Create bars for matches won, drawn, and lost
    rects1 = ax.bar(x - width, total_wins_sorted, width, label='Matches Won', color='PaleTurquoise')  # For Matches Won
    rects2 = ax.bar(x, total_draws_sorted, width, label='Matches Drawn', color='LightSteelBlue')        # For Matches Drawn
    rects3 = ax.bar(x + width, total_losses_sorted, width, label='Matches Lost', color='LightSlateGray') #For Matches Lost

    # Add labels and title
    ax.set_xlabel('Teams')
    ax.set_ylabel('Matches')
    ax.set_title('Matches Won, Drawn, and Lost by Team (Alphabetical Order)')
    ax.set_xticks(x)
    ax.set_xticklabels(team_names_sorted, rotation=45, ha="right")
    ax.legend()

    # Display bar values on top of the bars
    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()



#Compiled by Arnav Chourey
