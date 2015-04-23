import org.joda.time.Duration;
import org.joda.time.DateTime;
/**
 * This class defines a User/Client
 * 
 * @author ToFran
 */
public class Client{
    private String nickname;
    private int id;
    private int connections;
    private Duration timeConnected;
    private Duration maxTimeConnected;
    private DateTime lastJoined;

    /**
     * Construcs a client
     * 
     * @param id the client server sided unique ID
     * @param the nickname
     */
    public Client(int id, String nickname){
        this.nickname = nickname;
        this.id = id;
        timeConnected = new Duration(0);
        maxTimeConnected = new Duration(0);
        connections=1;
    }
    
    /**
     * Construcs a client
     * 
     * @param id the client server sided unique ID
     * @param the nickname
     * @param lastJoined when he joined the server (see joined(DateTime when) )
     */
    public Client(int id, String nickname, DateTime lastJoined){
        this.nickname = nickname;
        this.id = id;
        this.lastJoined = lastJoined;
        timeConnected = new Duration(0);
        maxTimeConnected = new Duration(0);
        connections=1;
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
    
    /**
     * Connects the clients to the server at a specific time
     * 
     * @param when the DateTime when the client joined
     */
    public void joined(DateTime when){
        connections++;
        lastJoined = when;
    }
    
    /**
     * Disconnects the client from the server
     */
    public void disconnected(DateTime when){
        Duration dur = new Duration(lastJoined.getMillis(), when.getMillis());
        if(dur.compareTo(maxTimeConnected)>0){
            maxTimeConnected = dur;
        }
        timeConnected = timeConnected.plus(dur);
    }
    
    /**
     * @return a String with the client info (separeted by \t)
     */
    public String toString(){
        return id + "\t" + nickname + "\t" + connections +
                "\t" + timeConnected.getStandardMinutes() + "\t" + maxTimeConnected.getStandardMinutes();  
    }
    
    /**
     * Prints the client info to the console with the following format:
     * ID  | Nickname                      |  * |SumTime(min)| Max Time
     * where * is the number of connections;
     * 
     */
    public void print(){
        System.out.printf("%-4d| %-30s| %-3d| %s\n", id, nickname, connections, timeConnected.getStandardMinutes());  
    }
}
