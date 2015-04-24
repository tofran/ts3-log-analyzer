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
    public void readFile(){
        int lineNumber = 0;
        String line = "";
        while(input.hasNextLine()) {
            try{
                lineNumber++; 
                line = input.nextLine();
                if(line.indexOf("| client connected")!=-1){ 
                    clientJoined(line);
                }
                else if(line.indexOf("| client disconnected")!=-1){ 
                    clientLeft(line);
                }
            }
            catch(Exception e){
                System.out.println("Exception @line:" + lineNumber + "\n" + line);
                input.close();
                System.exit(1);
            }
        }
        input.close();
    }
        
    /**
     * 
     */
    public int getId(String text){
        text = text.substring(text.indexOf("'(id:")+5);
        text = text.substring(0,text.indexOf(") "));
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
    }
    
    private void clientJoined(String line){
        int id = getId(line);
        DateTime date = getTime(line);
        String nickname = getNickname(line);
        if(DB.getPos(id)==-1){
            DB.add(new Client(id, nickname));
        }
        DB.connect(id, date);
    }
    
    /**
     * @param line the log line where the client left
     */
    private void clientLeft(String line){
        boolean didClientTimedOut = false;
        if(line.indexOf(") reason 'reasonmsg=connection lost'")!=-1){
            didClientTimedOut = true;
            System.out.println("connection lost @"+line);
        }
        DB.disconnect(getId(line), getTime(line), didClientTimedOut);
    }
}
