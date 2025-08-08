package plihal7and11;

import java.util.Arrays;

public class NumberSorter 
{

	public static void main(String[] args) 
	{
		// TODO Auto-generated method stub
		int[] numbers = new int[8];
		 
		 //Added 8 number to the Array
		for (int i = 0; i < numbers.length; i++) 
		{
	           numbers[i] = (int) (Math.random() * 51) + 50; // Generates numbers from 50 to 100
	    }
		 
		// Sort the array
	    int[] minMax = sortAndFindMinAndMax(numbers);
	        
	    // Print min and max values
	    System.out.println("The lowest element is " + minMax[0]);
	    System.out.println("The highest element is " + minMax[1]);
	        
	    //Print sorted array and count even/odd numbers
	        System.out.println("Here is the array");
	        int evenCount = 0, oddCount = 0, totalSum = 0;
	        for (int num : numbers)
	        {
	            System.out.print(num + " ");
	            totalSum += num;
	            if (num % 2 == 0) 
	            {
	                evenCount++;
	            } 
	            else 
	            {
	                oddCount++;
	            }
	        }
	        System.out.println();
	        
	        // Print even/odd count and total sum
	        System.out.println("Evens: " + evenCount + ", odds: " + oddCount);
	        System.out.println("Total: " + totalSum);
	    }
	
	//Find the Min and Max of the Array  
	public static int[] sortAndFindMinAndMax(int[] arr) 
	{
	     Arrays.sort(arr);
	     return new int[]{arr[0], arr[7]};
	 }
}
