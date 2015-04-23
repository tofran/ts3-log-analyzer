import java.util.Formatter;
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
    
    public static void openFile(String path){
        try{
            fmt = new Formatter(path);
        }
        catch(Exception e){
            System.out.println("Exeption - cant crate file!");
            System.exit(1);
        }
    }
    
    public static void saveToFile(String text){
        fmt.format(text);
    }
    
    public static void closeFile(){
        fmt.close();
    }
}
