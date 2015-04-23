import java.util.*;
import java.io.File;
import org.joda.time.*;
import org.joda.time.format.DateTimeFormat;
import java.time.format.*;

public class FileReader{
    private Scanner input;
    
    public FileReader(){
        try{
            File sourceFile;
            sourceFile = new File("input.log");
            input = new Scanner(sourceFile);
        }
        catch(Exception e){
            System.out.println("Exception");
        }
    }   
    
    public void readFile(){
        int lineNum = 0;
        while (input.hasNextLine()) {
            String line = input.nextLine();
            lineNum++;
            if(line.indexOf("client connected")!=-1){ 
                clientLeft(line);
            }
            if(line.indexOf("client disconnected")!=-1){ 
                clientLeft(line);
            }
        }
    }
   
    public int getId(String text){
        text = text.substring(text.indexOf("(id:")+4,text.indexOf(")"));
        return Integer.parseInt(text);
    }
    
    public String getNickname(String text){
        text = text.substring(text.indexOf("connected '")+11,text.indexOf("'(id:"));
        return text;
    }
    
    /**
     * yyyy-MM-dd HH:mm:ss
     * length = 19
     * 
     */
    public DateTime getTime(String text){
        text = text.substring(0,19);
        DateTime dt = DateTime.parse(text, DateTimeFormat.forPattern("yyyy-MM-dd HH:mm:ss"));
        System.out.println(dt);
        return dt;
        // http://stackoverflow.com/questions/6252678/converting-a-date-string-to-a-datetime-object-using-joda-time-library
    }
    
    public void clientLeft(String line){
        int id = getId(line);
        DateTime date = getTime(line);
        String nickname = getNickname(line);
        if(DB.getPos(id)==-1){
            DB.add(new Client(id, nickname, date));
        }
    }
    
    public void clientJoined(String line){
        DB.disconnect(getId(line), getTime(line));
    }
}
