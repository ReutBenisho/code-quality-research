import lombok.Value;

@Value
public class CustomException extends Exception {
    private String customValue; 
}
