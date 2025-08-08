package plihal7and11;

public class SumIntegers {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
        
        // Convert command-line arguments to integers and display them
        System.out.print("Passing [");
        int[] numbers = new int[args.length];
        for (int i = 0; i < args.length; i++) 
        {
            numbers[i] = Integer.parseInt(args[i]);
            System.out.print(numbers[i] + (i < args.length - 1 ? ", " : ""));
        }
        System.out.println("]");
        
        // Calculate and display the sum
        System.out.println("Sum is " + sumInts(numbers));
    }
    
    // Method to sum a variable number of integers
    public static int sumInts(int... numbers) 
    {
        int sum = 0;
        for (int num : numbers) 
        {
            sum += num;
        }
        return sum;
    }
}
