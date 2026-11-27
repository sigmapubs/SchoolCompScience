// AP CSA Unit 2: Selection and Iteration, all in one program.
public class NumberReport {
    public static void main(String[] args) {
        int n = 28;
        System.out.println("Report for " + n);

        // 1. Factors: for loop + if
        int count = 0;
        int sum = 0;
        String factors = "";
        for (int f = 1; f <= n; f++) {
            if (n % f == 0) {
                factors += f + " ";
                count++;
                if (f < n) {
                    sum += f;
                }
            }
        }
        System.out.println("Factors: " + factors);

        // 2. Classify: if / else if / else
        if (count == 2) {
            System.out.println(n + " is prime");
        } else if (sum == n) {
            System.out.println(n + " is perfect");
        } else {
            System.out.println(n + " is composite");
        }

        // 3. Binary: while loop + String building
        String binary = "";
        int m = n;
        while (m > 0) {
            binary = (m % 2) + binary;
            m /= 2;
        }
        System.out.println("Binary: " + binary);

        // 4. Compound boolean expression
        boolean twoDigitEven = n >= 10 && n <= 99 && n % 2 == 0;
        System.out.println("Two-digit even: " + twoDigitEven);

        // 5. Pattern: nested loops
        for (int row = 1; row <= 4; row++) {
            for (int col = 1; col <= row; col++) {
                System.out.print("*");
            }
            System.out.println();
        }
    }
}
