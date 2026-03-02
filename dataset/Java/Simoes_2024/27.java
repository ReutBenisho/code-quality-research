public class ParalyticDart extends TippedDart {
    {
        image = ItemSpriteSheet.PARALYTIC_DART;
    }

    @Override
    public int proc(Char attacker, Char defender, int damage) {
        if (!processChargingShot || attacker.alignment != defender.alignment) {
            Buff.prolong(defender, Paralysis.class, 5f);
        }
        return super.proc(attacker, defender, damage);
    }
}
