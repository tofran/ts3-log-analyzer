import java.util.Scanner;
/**
 * This is the main interface for the TS log analyzer
 * 
 * @author ToFran
 */
public class Main{
    private static Scanner sc = new Scanner(System.in);
    
    public static void main(String[] args){
        System.out.println("Log analyzer for TS3 by ToFran v1.0");
        boolean hasData = false;
        boolean exit = false;
        String choice;
        
        readFile();
        while(!exit){
            System.out.printf( "\n 1 - Save to file;" + 
                                "\n 2 - Print results to screen;" +
                                "\n 3 - Combine with another file;" +
                                "\n 4 - Flush database;" +
                                "\n 5 - exit" +
                                "\n: ");
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
                    DB.clear();
                    System.out.printf("Database cleared!");
                    break;
                    
                case "5":
                    exit=true;
                    break;
            }
        } 
    }
    
    private static void readFile(){
        System.out.printf("log name/path: ");
        String input = sc.next();            
        FileReader.execute(input);
        System.out.println("Finished!");
    }
      
    private static void saveToFile(){
        System.out.printf("File path: ");
        String input = sc.next();
        while(FileWriter.isFileThere(input)){
            System.out.printf("File already in use. File path: ");
            input = sc.next();
        }
        new FileWriter(input, DB.toStringAll());
        System.out.println("Success");
    }
}
