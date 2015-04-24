import java.util.Formatter;
import java.io.File;
/**
 * @authour ToFran
 */
public class FileWriter{
    private static Formatter fmt;
    
    public FileWriter(String path, String text){
        openFile(path);
        saveToFile(text);
        closeFile();
    }
    
    private static void openFile(String path){
        try{
            fmt = new Formatter(path);
        }
        catch(Exception e){
            System.out.println("Exeption - cant crate file!");
            System.exit(1);
        
        }
    }
    
    private static void saveToFile(String text){
        fmt.format(text);
    }
    
    private static void closeFile(){
        fmt.close();
    }
    
    public static boolean isFileThere(String path){
        File fl = new File(path);
        if(fl.exists()){
            return true;
        }
        return false;
    }
}
