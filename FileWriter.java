import java.util.Formatter;
import java.io.File;

/**
 * Whrites the DB to a file
 * 
 * @authour ToFran
 */
public class FileWriter{
    private static Formatter fmt = null;
    
    /**
     * Creates a fileWriter to output the DB to files
     * 
     * @param path the path to the new file
     * @param text the data to be saved in the file
     */
    public FileWriter(String path, String text){
        openFile(path);
        saveToFile(text);
        closeFile();
    }
    
    /**
     * Opens the file with Formatter
     * File cant exist
     * 
     * @param path the filepath/name
     */
    private static void openFile(String path){
        try{
            fmt = new Formatter(path);
        }
        catch(Exception e){
            System.out.println("Exeption - cant crate file!");
            System.exit(1);
        }
    }
    
    /**
     * @param text the data to be saved in the file
     */
    private static void saveToFile(String text){
        fmt.format(text);
    }
    
    /**
     * Closes the file
     */
    private static void closeFile(){
        try{
            fmt.close();
        }
        catch(Exception e){
            System.out.println();
        }
    }
    
    /**
     * Checks if theres a file/folder in the desired path
     * 
     * @param path the path to check
     * @return if it exists (true) or not (false)
     */
    public static boolean isFileThere(String path){
        File fl = new File(path);
        if(fl.exists()){
            return true;
        }
        return false;
    }
}
