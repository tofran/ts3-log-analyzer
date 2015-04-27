import java.util.Scanner;
import java.io.File;
import org.joda.time.DateTime;
import org.joda.time.Instant;
import org.joda.time.format.DateTimeFormat;

/**
 * Reads TS3 log files and adds them to the database
 * 
 * @author ToFran
 */
public class FileReader{
    private static Scanner input;
    public static final boolean debug = false;
    private static int totalLines = 0;

    /**
     * Executes the file reading to memmory
     * 
     * @param path the path for the file 
     */
    public static void execute(String path){
        File sourceFile = null;
        try{
            sourceFile = new File(path);
        }
        catch(Exception e){
            System.out.println("Exception 1 - ERROR READING FILE/PATH: " + path);
            System.exit(1);
        }
        
        if(sourceFile.isFile()){
            openFile(sourceFile);
            readFile();
            input.close();
        }
        else if(sourceFile.isDirectory()){
            File[] fileList = sourceFile.listFiles();
            if(fileList.length>=2){
                System.out.printf("Found " + fileList.length + " files:\nFROM: %s \nTO: %s\nContinue? (y/n)", 
                        fileList[0].getName(), fileList[fileList.length-1].getName());
                Scanner consoleScanner = new Scanner(System.in);
                String consoleInput = consoleScanner.next();
                if(consoleInput.equals("y")){
                    for(File each : fileList){
                        System.out.printf("Reading file %s ...", each.getName());
                        openFile(each);
                        readFile();
                        input.close();
                        System.out.printf(" done\n");
                    }
                }
            }
            else{
                System.out.println("FOLDER DOESNT HAVE (ENOUGH) FILES");
            }
        }
    }
    
    /**
     * Opens the file
     * 
     * @param sourceFile the file
     */
    private static void openFile(File sourceFile){
        try{
            input = new Scanner(sourceFile);
        }
        catch(Exception e){
            System.out.println("Exception 1 - ERROR OPENING FILE");
            System.exit(1);
        }
    }
    
    /**
     * Reads the file with Scanner
     */
    private static void readFile(){
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
            if(debug){
                System.out.println("@line:" + lineNumber);
            }
        }
        DB.disconnectAll(getTime(line));
        totalLines += lineNumber;
        if(debug){
                System.out.printf(" processed " + lineNumber + " lines\n");
        }
    }
        
    private static int getId(String text){
        text = text.substring(text.indexOf("'(id:")+5);
        text = text.substring(0,text.indexOf(") "));
        return Integer.parseInt(text);
    }
    
    private static String getNickname(String text){
        text = text.substring(text.indexOf("connected '")+11,text.indexOf("'(id:"));
        return text;
    }
    
    /**
     * Converts a date in a string with the format yyyy-MM-dd HH:mm:ss (length = 19)
     *
     * @param the String with the date/time
     * @return DateTime the joda time of the provided time
     */
    private static Instant getTime(String line){
        String text = line;
        text = text.substring(0,19);
        Instant dt = null;
        try{
             dt = Instant.parse(text, DateTimeFormat.forPattern("yyyy-MM-dd HH:mm:ss"));
        }
        catch(Exception e){
            System.out.println("id:" + getId(line) + 
                " Tried to join in a in a local time does not exist: " + line.substring(0,19) +
                " joda.time.IllegalInstantException Daylight saving time?");
        }
        return dt;
    }
    
    /**
     * @param line the log line where the client left
     */
    private static void clientJoined(String line){
        int id = getId(line);
        Instant date = getTime(line);
        String nickname = getNickname(line);
        if(DB.getPos(id)==-1){
            DB.add(new Client(id, nickname));
        }
        DB.connect(id, date, nickname);
    }
    
    /**
     * @param line the log line where the client left
     */
    private static void clientLeft(String line){
        boolean didClientTimedOut = false;
        if(line.indexOf(") reason 'reasonmsg=connection lost'")!=-1){
            didClientTimedOut = true;
        }
        DB.disconnect(getId(line), getNickname(line), getTime(line), didClientTimedOut);
    }
    
    /**
     * @return the total lines analyzed
     */
    public static int getAndResetTotalLines(){
        int lines = totalLines;
        totalLines = 0;
        return lines;
    }
}
