import java.util.Scanner;
/**
 * This is the main interface for the TS log analyzer
 * @author ToFran
 */
public class Main{
    private static Scanner sc = new Scanner(System.in);
    
    public static void main(String[] args){
        System.out.println("Log analyzer for TS3 by ToFran v1.0");
        boolean exit = false;
        String choice;
        
        readFile();
        while(!exit){
            System.out.println("\nWhat do you want to do next?" +
                                "\n 1 - Save to file;" + 
                                "\n 2 - Print results to screen;" +
                                "\n 3 - Combine with another file;" +
                                "\n 4 - exit");
            choice = sc.next();
            switch(choice.trim()){                
                case "2":
                    DB.printAllFormatted();
                    break;
                
                case "1":
                    saveToFile();
                    break;
                    
                case "3":
                    readFile();
                    break;                     
                     
                case "4":
                    exit=true;
                    break;
            }
            
        } 
    }
    
    private static void readFile(){
        System.out.printf("log name/path: ");
        String input = sc.next();            
        FileReader fr = new FileReader(input);
        System.out.println("File loaded to memory!");
    }
    
    private static void saveToFile(){
        System.out.printf("file path (WILL OVERWRITE): ");
        String input = sc.next();  
        new FileWriter(input, DB.toStringAll());
        System.out.println("Success");
    }
}
