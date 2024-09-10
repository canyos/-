import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class SimpleStat {

    public static void printSum(long sum){
        System.out.println("Sum: " + sum);
    }
    public static void printProduct(long product){
        System.out.println("Product: " + product);
    }
    public static long calculateSum(List<Integer> numbers){
        long sum=0;
        for (int iterator : numbers) {
            sum += iterator;
        }
        return sum;
    }
    public static long calculateProduct(List<Integer> numbers){
        long product=1;
        for (int iterator : numbers) {
            product *= iterator;
        }
        return product;
    }
    public static void inputPositiveNumber(List<Integer> numbers){
        Scanner scanner = new Scanner(System.in);
        boolean notPositive;
        while (true) {
            int input = scanner.nextInt();
            notPositive = (input<=0);
            if(notPositive)break;
            numbers.add(input);
        }
    }
    public static void printAnnounce(){
        System.out.println("Enter integer ( 0 or minus for Exit)");
    }
    public static void main(String[] args) {
        printAnnounce();
        List<Integer> numbers = new ArrayList<>();
        inputPositiveNumber(numbers);

        long sum = calculateSum(numbers);
        long product = calculateProduct(numbers);

        printSum(sum);
        printProduct(product);

    }
}