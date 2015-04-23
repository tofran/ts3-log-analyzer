import java.util.Scanner;
import java.io.File;
import org.joda.time.DateTime;
import org.joda.time.format.DateTimeFormat;

public class FileReader{
    private Scanner input;
    private File sourceFile;
    
    /**
     * Creates a file reader
     * 
     * @param path the file path
     */
    public FileReader(String path){
        openFile(path);
        readFile();
        input.close();
    }   
    
    /**
     * Opens the file
     */
    private void openFile(String path){
        try{
            sourceFile = new File(path);
            input = new Scanner(sourceFile);
        }
        catch(Exception e){
            System.out.println("Exception 1 - ERROR READING FILE");
            System.exit(1);
        }
    }
    
    /**
     * Reads the file with Scanner
     */
    private void readFile(){
        while(input.hasNextLine()) {
            String line = input.nextLine();
            if(line.indexOf("| client connected")!=-1){ 
                clientJoined(line);
            }
            if(line.indexOf("| client disconnected")!=-1){ 
                clientLeft(line);
            }
        }
    }
        
    /**
     * 
     */
    private int getId(String text){
        text = text.substring(text.indexOf("(id:")+4,text.indexOf(")"));
        return Integer.parseInt(text);
    }
    
    private String getNickname(String text){
        text = text.substring(text.indexOf("connected '")+11,text.indexOf("'(id:"));
        return text;
    }
    
    /**
     * Converts a date in a string with the format yyyy-MM-dd HH:mm:ss (length = 19)
     *
     * @param the String with the date/time
     * @return DateTime the joda time of the provided time
     */
    private DateTime getTime(String text){
        text = text.substring(0,19);
        DateTime dt = DateTime.parse(text, DateTimeFormat.forPattern("yyyy-MM-dd HH:mm:ss"));
        return dt;
        // http://stackoverflow.com/questions/6252678/converting-a-date-string-to-a-datetime-object-using-joda-time-library
    }
    
    private void clientJoined(String line){
        int id = getId(line);
        DateTime date = getTime(line);
        String nickname = getNickname(line);
        if(DB.getPos(id)==-1){
            DB.add(new Client(id, nickname, date));
        }
        else{
            DB.connect(id, date);
        }
    }
    
    /**
     * @param line the log line where the client left
     */
    private void clientLeft(String line){
        DB.disconnect(getId(line), getTime(line));
    }
}
