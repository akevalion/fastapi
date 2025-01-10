import java.util.*;
import javax.swing.*;

public class OrdenarNumeros {
    public static void main(String[] args) {
        JFrame window = new JFrame("hola");
        window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        window.setVisible(true);
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
