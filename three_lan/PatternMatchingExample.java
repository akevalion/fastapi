public class PatternMatchingExample {

    public static void main(String[] args) {
        PatternMatchingExample example = new PatternMatchingExample();

        System.out.println(example.foo(42));            // Integer positivo
        System.out.println(example.foo(-7));           // Integer negativo
        System.out.println(example.foo(150.5));        // Double mayor que 100
        System.out.println(example.foo(Double.NaN));   // Double NaN
        System.out.println(example.foo(88L));          // Long par
        System.out.println(example.foo(3L));           // Long impar (default)
        System.out.println(example.foo(null));         // Null
        //System.out.println(example.foo("Texto"));      // Tipo no soportado
    }

    public String foo(Number i) {
        return switch (i) {
            case Integer x when x > 0 -> "Es un Integer positivo con valor " + x;
            case Integer x when x < 0 -> "Es un Integer negativo con valor " + x;
            case Double x when x.isNaN() -> "Es un Double que no es un número (NaN)";
            case Double x when x > 100.0 -> "Es un Double mayor que 100 con valor " + x;
            case Long x when x % 2 == 0 -> "Es un Long par con valor " + x;
            case null -> "El valor es null";
            default -> "Tipo no soportado o condición no cumplida";
        };
    }
}
