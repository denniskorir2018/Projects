import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;


public class Soccer {

	public static void main(String[]args){


		Scanner myScanner=new Scanner(System.in);


		//fixed number of teams
		Points[] teams=new Points[2];
		//an arraylist of type Scores
		ArrayList<Points> list=new ArrayList<Points>();

		//variables
		int wins, losses, draws;
		String team;

		//number of teams which begins at 0
		int i=0;



		do{
			//team name
			System.out.println("Please enter the team name: ");
			team=myScanner.next();


			//wins
			System.out.println("Please enter the number of wins: ");
			wins=myScanner.nextInt();

			//losses
			System.out.println("Please enter the number of losses: ");
			losses=myScanner.nextInt();

			//draws
			System.out.println("Please enter the number of draws: ");
			draws=myScanner.nextInt();

			//creates new teams object 
			teams[i]=new Points(team, wins,losses, draws);


			list.add(new Points(team, wins, losses, draws));

			//continues till i gets to maximum number of allowable teams
			i++;



		}


		while (i<2);

		//sorts teams in descending order based on number of points
		Collections.sort(list, new mySorter());
		
		//prints list of teams, sorted based on points
		System.out.println(list);


	}

















}
