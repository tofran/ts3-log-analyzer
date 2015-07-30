import org.joda.time.Duration;
import org.joda.time.Instant;
import java.util.HashMap;

/**
 * This class defines a User/Client
 * 
 * @author ToFran
 */
public class Client{
    public static final boolean DEBUG = false;
    //private String nickname;
    private HashMap<String,Integer> nicknames;
    private int id, connections, timeOutCounter, aditionalConnections;
    private boolean isConnected;
    private int timeConnected, maxTimeConnected;
    private int lastJoined;

    /**
     * Construcs a client
     * 
     * @param id the client server sided unique ID
     * @param the nickname
     * @param 
     */
    public Client(int id, String nickname){
        //this.nickname = removeAsciiArt(nickname);
        this.id = id;
        timeConnected = 0;
        maxTimeConnected = 0;
        nicknames = new HashMap<String,Integer>();
        connections=1;
        timeOutCounter=0;
        isConnected = false;
        aditionalConnections = 0;
    }
    
    /**
     * Removes TS3 ascii art in the format: "(&#...;)|(&#....;)|(&#.....;)" and trims adjacebt spaces
     * Ex: "&#0000; &#995; NAME_ &#90695; &#A778;"
     * will return "NAME_"
     */
    private String removeAsciiArt(String text){
        text = text.trim().replaceAll("(&#...;)|(&#....;)|(&#.....;)", "").trim();
        return text;
    }
    
    /**
     * @return the client id
     */
    public int getId(){
        return id;
    }
    
    /**
     * @return the cumulative connection time
     */
    public int getTime(){
        return timeConnected;
    }
    
    /**
     * @return the moast used nickname
     */
    public String getNickname(){
        int max = 0;
        String maxNickname = "";
        for(String each : nicknames.keySet()){
            if(nicknames.get(each)>max){
                max = nicknames.get(each);
                maxNickname = each;
            }
        }
        return maxNickname;
    }
    
    /**
     * Increases teh count of the desired nickname
     * 
     * @param the nockname to increase
     */
    private void usedNickname(String name){
        if(name!=null && !name.equals("")){
            name = removeAsciiArt(name);
            if(nicknames.containsKey(name)){
                nicknames.put(name, (nicknames.get(name)+1));
            }
            else{
                nicknames.put(name, 1);
            }
        }
    }
    
    /**
     * @return if the client is connected or not
     */
    public boolean isConnected(){
        return isConnected;
    }
    
    /**
     * Connects the clients to the server at a specific time
     * 
     * @param when the Instant when the client joined
     * @param nickname
     */
    public void joined(int when, String nickname){
        if(!isConnected){
            connections++;
            lastJoined = when;
            isConnected = true;
        }
        else{
            aditionalConnections++;
            if(DEBUG){
                System.out.println("creted an adition connection for id:" + id + " currently @" + aditionalConnections);
            }
        }
        usedNickname(nickname);
    }
    
    /**
     * Disconnects the client from the server
     */
    public void disconnected(int when, String nickname){
        if(isConnected){
            if(aditionalConnections==0){
                try{
                    int dur = when - lastJoined;
                    if(dur > maxTimeConnected){
                        maxTimeConnected = dur;
                    }
                    isConnected = false;
                    timeConnected += dur;
                }
                catch(Exception e){
                    System.out.println("Something went whrong disconectiong " + nickname + " @time:" + when);
                }
            }
            else{
                aditionalConnections--;
                if(DEBUG){
                    System.out.println("decremented adition connection for id:" + id + " currently @" + aditionalConnections);
                }
            }
            usedNickname(nickname);
        }
        else{
             System.out.println("Client id:" + id + " cant disconnect on " + when + ": CLIENT NOT CONNECTED");
        }
    }

    /**
     * Increments the time out counter
     */
    public void timedOut(){
        timeOutCounter++;
    }
    
    /**
     * @return a String with the client info (separeted by \t)
     */
    public String toString(){
        return id + "\t" + getNickname() + "\t" + timeConnected + 
            "\t" + maxTimeConnected + "\t" + connections + "\t" +timeOutCounter;  
    }
    
    /**
     * Prints the client info to the console with the following format:
     * ID  | Nickname |  number of connections | Sum time of all connections | Longest connection
     */
    public void print(){
        System.out.printf("%-4d| %-30s| %-11d| %-6d| %d\n", 
            id, getNickname(), timeConnected,
            maxTimeConnected, connections);  
    }
}
