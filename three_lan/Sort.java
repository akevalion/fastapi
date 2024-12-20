import java.util.*;

public class OrdenarNumeros {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        List<Integer> numeros = new ArrayList<>();

        while (scanner.hasNextLine()) {
            String input = scanner.nextLine();
            if (input.isEmpty()) break;
            try {
                numeros.add(Integer.parseInt(input.trim()));
            } catch (NumberFormatException e) {
                continue;
            }
        }

        Collections.sort(numeros);

        for (int numero : numeros) {
            System.out.println(numero);
        }
    }
}
