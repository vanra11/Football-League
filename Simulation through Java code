import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

class Player {
    private String name;
    private String position;
    private String team;
    private int points;

    public Player(String name, String position, String team) {
        this.name = name;
        this.position = position;
        this.team = team;
        this.points = 0;
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
    }

    public int getPoints() {
        return this.points;
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
    }

    public void addPlayer(Player player) {
        if (this.players.size() < 15) {
            this.players.add(player);
        }
    }

    public List<Player> getPlayers() {
        return this.players;
    }

    public int getMatchesPlayed() {
        return this.matchesPlayed;
    }

    public void setMatchesPlayed(int matchesPlayed) {
        this.matchesPlayed = matchesPlayed;
    }

    public String getName() {
        return this.name;
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

    public int calculateTotalPoints() {
        return this.players.stream().mapToInt(Player::getPoints).sum();
    }

    public void addMatchResult(int goalsScored, int goalsConceded, int month) {
        this.totalGoalsScored += Math.min(goalsScored, 70);
        this.totalGoalsConceded += Math.min(goalsConceded, 30);

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

    public double calculateAdditionalScore() {
        double K = 3;
        double G = 2;
        double M = 1;
        return (K * this.matchesWon) + (G * this.totalGoalsScored) - (M * this.totalGoalsConceded);
    }

    public double normalizePoints() {
        return (double) Arrays.stream(this.monthlyPoints).sum() / 12;
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

        Random random = new Random();
        int goalsTeam1 = random.nextInt(7);
        int goalsTeam2 = random.nextInt(7);

        team1.addMatchResult(goalsTeam1, goalsTeam2, this.month);
        team2.addMatchResult(goalsTeam2, goalsTeam1, this.month);

        for (Player player : team1.getPlayers()) {
            int minutesPlayed = random.nextInt(61) + 30;
            int goals = random.nextInt(3);
            player.updatePoints(minutesPlayed, goals);
        }

        for (Player player : team2.getPlayers()) {
            int minutesPlayed = random.nextInt(61) + 30;
            int goals = random.nextInt(3);
            player.updatePoints(minutesPlayed, goals);
        }
    }
}

class League {
    private List<Team> teams;

    public League(List<Team> teams) {
        this.teams = teams;
    }

    public void simulateSeason() {
        int numMatchesPerTeam = 12;
        List<List<Team>> allMatches = new ArrayList<>();
        for (int i = 0; i < this.teams.size(); i++) {
            for (int j = i + 1; j < this.teams.size(); j++) {
                Team team1 = this.teams.get(i);
                Team team2 = this.teams.get(j);
                while (team1.getMatchesPlayed() < numMatchesPerTeam && team2.getMatchesPlayed() < numMatchesPerTeam) {
                    allMatches.add(new ArrayList<>(List.of(team1, team2)));
                    team1.setMatchesPlayed(team1.getMatchesPlayed() + 1);
                    team2.setMatchesPlayed(team2.getMatchesPlayed() + 1);
                }
            }
        }

        Collections.shuffle(allMatches);
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
                .max((t1, t2) -> Double.compare(t1.calculateAdditionalScore() + t1.normalizePoints(),
                        t2.calculateAdditionalScore() + t2.normalizePoints()))
                .orElse(null);
    }
}

public class Main {
    public static void main(String[] args) {
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

        League league = new League(teams);
        league.simulateSeason();

        Team winner = league.getWinner();
        if (winner != null) {
            System.out.println("The winner is: " + winner.getName() + " with " + winner.calculateAdditionalScore() + " ovr");
            System.out.println("Total points scored: " + winner.getTotalMatchPoints() + " match points.");
            System.out.println("Goals Scored: " + winner.getTotalGoalsScored() + ", Goals Conceded: " + winner.getTotalGoalsConceded());
            System.out.println("Matches Won: " + winner.getMatchesWon() + ", Matches Drawn: " + winner.getMatchesDrawn() + ", Matches Lost: " + winner.getMatchesLost());
        } else {
            System.out.println("No teams were available to determine a winner.");
        }
    }
}
//Coded by Arnav Chourey
