public class SnapStartRecorder {
    private boolean enabled;
    private boolean fullWarmup;

    public void setWarmup(boolean fw) {
        enabled = true;
        fullWarmup = fw;
    }
}
