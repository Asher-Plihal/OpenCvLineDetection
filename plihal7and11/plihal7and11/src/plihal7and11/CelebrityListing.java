package plihal7and11;

import java.util.ArrayList;
import java.util.Iterator;

public class CelebrityListing {
    public static void main(String[] args) 
    {
    	// TODO Auto-generated method stub
    	
        // Create an ArrayList
        ArrayList<String> celebrities = new ArrayList<>();
        
        // Add five names to the list
        celebrities.add("Lionel Messi");
        celebrities.add("Drake");
        celebrities.add("Adele");
        celebrities.add("Dwayne Johnson");
        celebrities.add("Beyonce");
        
        // Display the original list
        System.out.println("Here is the list");
        for (int i = 0; i < celebrities.size(); i++) 
        {
            System.out.println(celebrities.get(i));
        }
        
        // Pass the list to a void method
        modifyList(celebrities);
        
        // Use an iterator to display the final list
        System.out.println("Using an iterator, here is the list");
        Iterator<String> iterator = celebrities.iterator();
        while (iterator.hasNext()) {
            System.out.println(iterator.next());
        }
    }

    public static void modifyList(ArrayList<String> list) {
       
        list.add(2, "Taylor Swift"); // Insert at index 2
        list.remove(4); //Remove index 4
        
        // Display the modified list using a foreach loop
        System.out.println("Here is the new list");
        for (String name : list) {
            System.out.print(" * " + name);
        }
        System.out.println("");
    }
}