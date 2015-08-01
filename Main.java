import java.util.Scanner;

/**
 * This is the main interface for the TS log analyzer
 * 
 * @author ToFran
 */
public class Main{
    private static Scanner sc = new Scanner(System.in);
    private static boolean hasData = false;
    
    /**
     * The main console executed method
     * Its the interface with the program, run it to start
     * 
     * No parameters available, yet
     */
    public static void main(String[] args){
        System.out.printf("##############################\n# TS3 Log analyser by ToFran #\n##############################\n");
        boolean exit = false;
        String input;
        
        while(!exit){
            hasData = DB.hasData();
            System.out.printf(help());
            input = sc.next().trim();
            if(hasData || (!hasData && (input.equals("1") || input.equals("5")))){
                switch(input){  
                    case "1":
                        readFile();
                        break; 
                        
                    case "2":
                        saveToFile();
                        break; 
                        
                    case "3":
                        DB.printAllFormatted();
                        break;
                    
                    case "4":
                        DB.clear();
                        System.out.printf("Database cleared!\n");
                        hasData = false;
                        break;
                        
                    case "5":
                        exit=true;
                        break;
                }
            }
        } 
    }
    
    /**
     * Calls help menu
     * 
     * @return the help text to be displayed
     */
    private static String help(){
        String st = "\nAvailable commands:";
        if(!hasData){
            st += "\n 1 - Read file/folder;";
        }
        else{
            st += "\n 1 - Read another file/folder (combine data);" +
                "\n 2 - Save database to file;" + 
                "\n 3 - Print results to screen;" +
                "\n 4 - Flush database;";        
        }
        return st + "\n 5 - exit\n:";
    }
    
    /**
     * A sub-menu for reading files
     */
    private static void readFile(){
        System.out.printf("log file/folder path: ");
        String input = sc.next().replace("\\", "\\\\");
        FileReader.execute(input);
        System.out.println(FileReader.getAndResetTotalLines() + " lines analized!");
    }
    
    /**
     * A sub-menu for saving files
     */
    private static void saveToFile(){
        System.out.printf("Output file path: ");
        String input = sc.next().replace("\\", "\\\\");
        while(FileWriter.isFileThere(input)){
            System.out.printf("File already there. File path: ");
            input = sc.next().replace("\\", "\\\\");
        }

        System.out.println("1 - Save as tab separated data (for importing w/ excel, etc)\n2 - Save as extensive JSON file");
        switch(sc.next().trim()){
            case "1":
                new FileWriter(input, DB.toStringAll());
                System.out.println("Success!"); 
                break;
                
            case "2":
                new FileWriter(input, DB.toJson());
                System.out.println("NOT IMPLEMENTED YET"); 
                break;
                
            default:
                System.out.printf("Cancelled");
                break;
        }
        
    }
}
