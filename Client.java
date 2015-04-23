import org.joda.time.*;
import java.util.*;
/**
 * 
 * 
 * @author ToFran
 */
public class Client{
    private ArrayList<String> nicknames;
    private int id;
    private int connections;
    private Duration timeConnected;
    private Duration maxTimeConnected;
    private DateTime lastJoined;

    public Client(int id, String nickname, DateTime lastJoined){
        nicknames = new ArrayList<String>();
        nicknames.add(nickname);
        this.id = id;
        this.lastJoined = lastJoined;
        timeConnected = new Duration(0);
        maxTimeConnected = new Duration(0);
    }
    
    public int getId(){
        return id;
    }

    /**
     * @return the Duration of all connections
     */
    public Duration getTime(){
        return timeConnected;
    }
    
    /**
     * @param time connected instance
     */
    public void joined(DateTime when){
        connections++;
        lastJoined = when;
    }
    
    public void disconnected(DateTime when){
        Duration dur = new Duration(lastJoined.getMillis(), when.getMillis());
        //verificar se é maior do que o maximo
        timeConnected = timeConnected.plus(dur);
    }
}
