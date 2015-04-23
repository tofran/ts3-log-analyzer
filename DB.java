import java.util.ArrayList;
import org.joda.time.DateTime;
/**
 * A tatic database of alla clients
 * @author ToFran 
 */
public class DB{
    private static ArrayList<Client> clients = new ArrayList<Client>();
    
    /**
     * Adds a client to the database / list
     * 
     * @param clientToAdd the client to add
     */
    public static void add(Client clientToAdd){
        clients.add(clientToAdd);
    }
    
    /**
     * Connects a client
     * 
     * @param who the id of the client
     * @param when the time of the connection
     */
    public static void connect(int who, DateTime when){
        clients.get(getPos(who)).joined(when);
    }
    
    /**
     * Disconnects a client
     * 
     * @param who the id of the client
     * @param when the theme that of the client DC
     */
    public static void disconnect(int id, DateTime when){
        int pos = getPos(id);
        if(pos!=-1){
            clients.get(getPos(id)).disconnected(when);
        }
        else{
             System.out.println("Client:" + id + " cant disconnect because he was not found");
        }
    }

    /**
     * Finds the position in the list/datablase of the specified client
     * 
     * @param id the id of the client
     * @return the position in the list
     */
    public static int getPos(int id){
        int i = 0;
        while(i<clients.size() && clients.get(i).getId() != id){
            i++;
        }
        if(i>=clients.size()){
            i = -1;
        }
        return i;
    }
    
    /**
     * @return all the info abaout the clients on the DB
     */
    public static String toStringAll(){
        String st = "Client's Server ID\tNickname\tNumber Connections\tCumulative connection time (min)\tLongest connection time (min)\n";
        for(Client each : clients){
            st += each.toString() + "\n";
        }
        return st;
    }
    
    /**
     * Prints every client
     */
    public static void printAllFormatted(){
        System.out.println("ID  | Nickname                      |    |SumTime(min)| Longest connection");
        for(Client each : clients){
            each.print();
        }
    }
}
