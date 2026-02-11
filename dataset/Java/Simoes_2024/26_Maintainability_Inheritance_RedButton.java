
/**
 * Source: Simões & Venson (2024), Listing 8
 * Category: Design / Deep Inheritance
 * Project: Shattered Pixel Dungeon
 * SonarQube Rating: E (High repair cost vs code size)
 * Ground Truth: GPT models fail to see the context and give high scores (90).
 */
public class RedButton extends StyledButton {
    
    public RedButton(String label) {
        this(label, 9);
    }

    public RedButton(String label, int size) {
        super(Chrome.Type.RED_BUTTON, label, size);
    }
}