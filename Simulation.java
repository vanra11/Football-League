import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Random;
import java.util.stream.Collectors;

class Player {
    private String name;
    private String position;
    private String team;
    private int points;
    private int yellowCards;
    private int redCards;
    private int suspensionGames;

    public Player(String name, String position, String team) {
        this.name = name;
        this.position = position;
        this.team = team;
        this.points = 0;
        this.yellowCards = 0;
        this.redCards = 0;
        this.suspensionGames = 0;
    }

    public int getPoints() {
        return this.points;
    }

    public int getSuspensionGames() {
        return this.suspensionGames;
    }

    public void setSuspensionGames(int suspensionGames) {
        this.suspensionGames = suspensionGames;
    }

    public void updatePoints(int minutesPlayed, int goals) {
        if (minutesPlayed >= 60) {
            this.points += 2;
        } else {
            this.points += 1;
        }

        if (this.position.equals("Goalkeeper") && goals > 0) {
            this.points += 10;
        } else if (this.position.equals("Defender") && goals > 0) {
            this.points += 6;
        } else if (this.position.equals("Midfielder") && goals > 0) {
            this.points += 5;
        } else if (this.position.equals("Forward") && goals > 0) {
            this.points += 4;
        }

        // Deduct points for cards
        this.points -= this.yellowCards;  // -1 point for each yellow card
        this.points -= (this.redCards * 2);  // -2 points for each red card
    }

    public void receiveCard(String cardType) {
        if (cardType.equals("yellow")) {
            if (this.yellowCards < 2) {  // A player can receive a max of 2 yellow cards in one game
                this.yellowCards++;
            }
            if (this.yellowCards == 2) {  // 2 yellow cards lead to a suspension
                this.suspensionGames += 1;
            }
        } else if (cardType.equals("red")) {
            this.redCards++;
            this.suspensionGames += 2;  // 1 red card leads to suspension for 2 games
        }
    }
}

class Team {
    private String name;
    private List<Player> players;
    private int totalGoalsScored;
    private int totalGoalsConceded;
    private int matchesWon;
    private int matchesDrawn;
    private int matchesLost;
    private int totalMatchPoints;
    private int[] monthlyPoints;
    private int matchesPlayed;
    private int totalCardsReceived;  // Make this private

    public Team(String name) {
        this.name = name;
        this.players = new ArrayList<>();
        this.totalGoalsScored = 0;
        this.totalGoalsConceded = 0;
        this.matchesWon = 0;
        this.matchesDrawn = 0;
        this.matchesLost = 0;
        this.totalMatchPoints = 0;
        this.monthlyPoints = new int[12];
        this.matchesPlayed = 0;
        this.totalCardsReceived = 0;
    }

    public String getName() {
        return this.name;
    }

    public List<Player> getPlayers() {
        return this.players;
    }

    public int getTotalMatchPoints() {
        return this.totalMatchPoints;
    }

    public int getTotalGoalsScored() {
        return this.totalGoalsScored;
    }

    public int getTotalGoalsConceded() {
        return this.totalGoalsConceded;
    }

    public int getMatchesWon() {
        return this.matchesWon;
    }

    public int getMatchesDrawn() {
        return this.matchesDrawn;
    }

    public int getMatchesLost() {
        return this.matchesLost;
    }

    public int getMatchesPlayed() {
        return this.matchesPlayed;
    }

    public void setMatchesPlayed(int matchesPlayed) {
        this.matchesPlayed = matchesPlayed;
    }

    public int getTotalCardsReceived() {
        return this.totalCardsReceived;
    }

    public void addPlayer(Player player) {
        if (this.players.size() < 15) {
            this.players.add(player);
        }
    }

    public void incrementTotalCardsReceived(int count) {
        this.totalCardsReceived += count;  // Method to modify totalCardsReceived
    }

    public int calculateTotalPoints() {
        return this.players.stream().mapToInt(Player::getPoints).sum();
    }

    public void addMatchResult(int goalsScored, int goalsConceded, int month) {
        this.totalGoalsScored += Math.min(goalsScored, 70);
        this.totalGoalsConceded += Math.min(goalsConceded, 30);
        this.totalGoalsScored = Math.min(this.totalGoalsScored, 70);
        this.totalGoalsConceded = Math.min(this.totalGoalsConceded, 30);

        if (goalsScored > goalsConceded) {
            this.matchesWon++;
            this.totalMatchPoints += 3;
        } else if (goalsScored == goalsConceded) {
            this.matchesDrawn++;
            this.totalMatchPoints += 1;
        } else {
            this.matchesLost++;
        }

        this.monthlyPoints[month] += this.totalMatchPoints;
        this.matchesPlayed++;
    }

    public int calculateAdditionalScore() {
        int K = 3;
        int G = 2;
        int M = 1;
        return (K * this.matchesWon) + (G * this.totalGoalsScored) - (M * this.totalGoalsConceded);
    }

    public double normalizePoints() {
        return Arrays.stream(this.monthlyPoints).average().orElse(0.0);
    }
}

class Match {
    private List<Team> teams;
    private int month;

    public Match(List<Team> teams, int month) {
        this.teams = teams;
        this.month = month;
    }

    public void simulate() {
        Team team1 = this.teams.get(0);
        Team team2 = this.teams.get(1);
        int goalsTeam1 = new Random().nextInt(7);
        int goalsTeam2 = new Random().nextInt(7);

        team1.addMatchResult(goalsTeam1, goalsTeam2, this.month);
        team2.addMatchResult(goalsTeam2, goalsTeam1, this.month);

        // Select players for card assignment
        List<Player> playersForCards = new ArrayList<>();
        playersForCards.addAll(selectPlayersForCards(team1));
        playersForCards.addAll(selectPlayersForCards(team2));
        Collections.shuffle(playersForCards);

        // Assign cards to selected players at a frequency of 1 card per 4 games
        if (new Random().nextDouble() < (1.0 / 4)) {
            for (Player player : playersForCards) {
                String cardType = new Random().nextBoolean() ? "yellow" : "red";
                player.receiveCard(cardType);
                team1.incrementTotalCardsReceived(cardType.equals("yellow") ? 1 : 2);
                team2.incrementTotalCardsReceived(cardType.equals("yellow") ? 1 : 2);
            }
        }

        // Simulate performance for all players
        for (Player player : team1.getPlayers()) {
            if (player.getSuspensionGames() > 0) {
                player.setSuspensionGames(player.getSuspensionGames() - 1);  // Reduce suspension games
                continue;  // Skip point update if suspended
            }

            // Simulate performance
            int minutesPlayed = new Random().nextInt(61) + 30;
            int goals = new Random().nextInt(3);
            player.updatePoints(minutesPlayed, goals);
        }

        for (Player player : team2.getPlayers()) {
            if (player.getSuspensionGames() > 0) {
                player.setSuspensionGames(player.getSuspensionGames() - 1);  // Reduce suspension games
                continue;  // Skip point update if suspended
            }

            // Simulate performance
            int minutesPlayed = new Random().nextInt(61) + 30;
            int goals = new Random().nextInt(3);
            player.updatePoints(minutesPlayed, goals);
        }
    }

    private List<Player> selectPlayersForCards(Team team) {
        int numPlayersForCards = new Random().nextInt(2) + 1;
        Collections.shuffle(team.getPlayers()); // Shuffle players to select randomly
        return team.getPlayers().subList(0, Math.min(numPlayersForCards, team.getPlayers().size()));
    }
}

class League {
    private List<Team> teams;

    public League(List<Team> teams) {
        this.teams = teams;
    }

    public void simulateSeason() {
        int numMatchesPerTeam = 14;
        List<List<Team>> allMatches = new ArrayList<>();
        for (int i = 0; i < this.teams.size(); i++) {
            for (int j = i + 1; j < this.teams.size(); j++) {
                Team team1 = this.teams.get(i);
                Team team2 = this.teams.get(j);
                // Schedule matches to ensure each team plays 14 matches
                while (team1.getMatchesPlayed() < numMatchesPerTeam && team2.getMatchesPlayed() < numMatchesPerTeam) {
                    allMatches.add(Arrays.asList(team1, team2));
                    team1.setMatchesPlayed(team1.getMatchesPlayed() + 1);
                    team2.setMatchesPlayed(team2.getMatchesPlayed() + 1);
                }
            }
        }

        Collections.shuffle(allMatches);  // Randomize match order
        int month = 0;
        for (List<Team> match : allMatches) {
            if (month >= 12) {
                month = 0;
            }
            new Match(match, month).simulate();
            month++;
        }
    }

    public Team getWinner() {
        return this.teams.stream()
                .max(Comparator.comparingInt(Team::calculateAdditionalScore)
                        .thenComparingInt(Team::getTotalMatchPoints))
                .orElse(null);
    }

    public List<Team> getMostAndLeastCardsTeams() {
        this.teams.sort(Comparator.comparingInt(Team::getTotalCardsReceived));
        return Arrays.asList(this.teams.get(this.teams.size() - 1), this.teams.get(0));
    }
}

public class Main {
    public static void main(String[] args) {
        // Create players and teams
        List<Team> teams = new ArrayList<>();
        String[] teamNames = {
            "Manchester United", "Liverpool", "Manchester City", "Arsenal",
            "Chelsea", "Tottenham Hotspur", "FC Barcelona", "Real Madrid",
            "Atlético Madrid", "Inter Milan", "AC Milan", "Juventus"
        };

        for (String teamName : teamNames) {
            Team team = new Team(teamName);
            for (int i = 0; i < 15; i++) {
                String[] positions = {"Forward", "Midfielder", "Defender", "Goalkeeper"};
                String position = positions[new Random().nextInt(positions.length)];
                Player player = new Player("Player " + (i + 1) + " of " + teamName, position, teamName);
                team.addPlayer(player);
            }
            teams.add(team);
        }

        // Create a league
        League league = new League(teams);

        // Simulate the season
        league.simulateSeason();

        // Get the winner
        Team winner = league.getWinner();
        if (winner != null) {
            System.out.println("The winner is: " + winner.getName() + " with " + winner.calculateAdditionalScore() + " ovr");
            System.out.println("Total points scored: " + winner.getTotalMatchPoints() + " match points.");
            System.out.println("Goals Scored: " + winner.getTotalGoalsScored() + ", Goals Conceded: " + winner.getTotalGoalsConceded());
            System.out.println("Matches Won: " + winner.getMatchesWon() + ", Matches Drawn: " + winner.getMatchesDrawn() + ", Matches Lost: " + winner.getMatchesLost());
        }

        // Get teams with most and least cards
        List<Team> cardsTeams = league.getMostAndLeastCardsTeams();
        //System.out.println("Team with the most cards: " + cardsTeams.get(1).getName() + " with " + cardsTeams.get(1).getTotalCardsReceived() + " cards.");
        System.out.println("Fairplay Award: " + cardsTeams.get(0).getName() + " with " + cardsTeams.get(0).getTotalCardsReceived() + " cards.");
    }
}
//Coded by Arnav Chourey
