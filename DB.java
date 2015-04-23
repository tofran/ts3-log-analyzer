import java.util.ArrayList;
import org.joda.time.*;
/**
 * 
 * @author ToFran 
 */
public class DB{
    private static ArrayList<Client> clients = new ArrayList<Client>();
    
    public static void add(Client clientToAdd){
        clients.add(clientToAdd);
    }
    
    public static void get(int i){
        clients.get(i);
    }
    
    public static void disconnect(int who, DateTime when){
        clients.get(who).disconnected(when);
    }

    public static int getPos(int id){
        int i = 0;
        while(clients.get(i).getId() == id && i<clients.size()){
            i++;
        }
        if(i>=clients.size()){
            i = -1;
        }
        return i;
    }
}
