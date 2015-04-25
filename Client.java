import org.joda.time.Duration;
import org.joda.time.Instant;
/**
 * This class defines a User/Client
 * 
 * @author ToFran
 */
public class Client{
    private String nickname;
    private int id, connections, timeOutCounter;
    private boolean isConnected;
    private Duration timeConnected, maxTimeConnected;
    private Instant lastJoined;

    /**
     * Construcs a client
     * 
     * @param id the client server sided unique ID
     * @param the nickname
     * @param 
     */
    public Client(int id, String nickname){
        this.nickname = removeAsciiArt(nickname);
        this.id = id;
        timeConnected = new Duration(0);
        maxTimeConnected = new Duration(0);
        connections=1;
        timeOutCounter=0;
        isConnected = false;
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
    public Duration getTime(){
        return timeConnected;
    }
    
    /**
     * @return the first nickname that the client used to join
     */
    public String getNickname(){
        return nickname;
    }
    
    public boolean isConnected(){
        return isConnected;
    }
    
    /**
     * Connects the clients to the server at a specific time
     * 
     * @param when the Instant when the client joined
     */
    public void joined(Instant when){
        connections++;
        lastJoined = when;
        isConnected = true;
    }
    
    /**
     * Disconnects the client from the server
     */
    public void disconnected(Instant when){
        if(isConnected){
            Duration dur = new Duration(lastJoined.getMillis(), when.getMillis());
            if(dur.compareTo(maxTimeConnected)>0){
                maxTimeConnected = dur;
            }
            isConnected = false;
            timeConnected = timeConnected.plus(dur);
        }
        else{
             System.out.println("Client id:" + id + " cant disconnect: NOT CONNECTED");
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
        return id + "\t" + nickname + "\t" + timeConnected.getStandardMinutes() + 
            "\t" + maxTimeConnected.getStandardMinutes() + "\t" + connections + "\t" +timeOutCounter;  
    }
    
    /**
     * Prints the client info to the console with the following format:
     * ID  | Nickname |  number of connections | Sum time of all connections | Longest connection
     */
    public void print(){
        System.out.printf("%-4d| %-30s| %-11d| %-6d| %d\n", 
            id, nickname, timeConnected.getStandardMinutes(),
            maxTimeConnected.getStandardMinutes(), connections);  
    }
}
