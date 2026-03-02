/**
 * Source: Simões & Venson (2024), Listing 5
 * Category: Maintainability / Multi-threading Risks
 * Project: Quarkus
 * SonarQube Rating: D (Estimated 1h 40m repair effort)
 * Ground Truth: GPT-3.5 missed these issues and gave it a high score (85).
 */
public class SnapStartRecorder {
    private boolean enabled;
    private boolean fullWarmup;

    public void setWarmup(boolean fw) {
        // SonarQube identifies thread-safety risks and maintenance issues here
        enabled = true;
        fullWarmup = fw;
    }
}