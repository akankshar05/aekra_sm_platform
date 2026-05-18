public class GradeCalculator {
    public static void main(String[] args) throws java.io.IOException {
        java.io.BufferedReader br = new java.io.BufferedReader(new java.io.InputStreamReader(System.in));
        String line = br.readLine();
        java.util.List<String> tokens = new java.util.ArrayList<>();
        if (line != null) {
            for (String t : line.trim().split("\\s+")) if (!t.isEmpty()) tokens.add(t);
        }
        while (tokens.size() < 3) {
            String l = br.readLine();
            if (l == null) break;
            for (String t : l.trim().split("\\s+")) if (!t.isEmpty()) tokens.add(t);
        }
        double sum = 0;
        int count = Math.min(3, tokens.size());
        for (int i = 0; i < count; i++) {
            try { sum += Double.parseDouble(tokens.get(i)); } catch (NumberFormatException e) {}
        }
        double avg = (count > 0) ? sum / count : 0;
        char grade;
        if (avg >= 90) grade = 'A';
        else if (avg >= 75) grade = 'B';
        else if (avg >= 60) grade = 'C';
        else if (avg >= 40) grade = 'D';
        else grade = 'F';
        System.out.println(grade);
    }
}
