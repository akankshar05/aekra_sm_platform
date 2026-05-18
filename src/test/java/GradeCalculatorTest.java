import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.io.*;

public class GradeCalculatorTest {
    private final PrintStream originalOut = System.out;
    private final InputStream originalIn = System.in;
    private ByteArrayOutputStream outContent;

    @BeforeEach
    public void setUp() {
        outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));
    }

    @AfterEach
    public void tearDown() {
        System.setOut(originalOut);
        System.setIn(originalIn);
    }

    private String runWithInput(String input) throws Exception {
        System.setIn(new ByteArrayInputStream(input.getBytes()));
        GradeCalculator.main(new String[0]);
        return outContent.toString().trim();
    }

    @Test
    public void testAverageExactly90A() throws Exception {
        assertEquals("A", runWithInput("90 90 90\n"));
    }

    @Test
    public void testAverage75B() throws Exception {
        assertEquals("B", runWithInput("75 75 75\n"));
    }

    @Test
    public void testAverage60C() throws Exception {
        assertEquals("C", runWithInput("60 60 60\n"));
    }

    @Test
    public void testAverage40D() throws Exception {
        assertEquals("D", runWithInput("40 40 40\n"));
    }

    @Test
    public void testFailingF() throws Exception {
        assertEquals("F", runWithInput("10 20 30\n"));
    }

    @Test
    public void testDecimalAverageB() throws Exception {
        assertEquals("B", runWithInput("90 90 89\n"));
    }
}
