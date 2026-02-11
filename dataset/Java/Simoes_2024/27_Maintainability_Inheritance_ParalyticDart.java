
/**
 * Source: Simões & Venson (2024), Listing 9
 * Category: Design / Deep Inheritance & Magic Numbers
 * Project: Shattered Pixel Dungeon
 * SonarQube Rating: E
 * Ground Truth: GPT-3.5 identified the magic number but missed the inheritance issue.
 */
public class ParalyticDart extends TippedDart {
    {
        image = ItemSpriteSheet.PARALYTIC_DART;
    }

    @Override
    public int proc(Char attacker, Char defender, int damage) {
        // Magic number '5f' and deep inheritance are the main issues here.
        if (!processChargingShot || attacker.alignment != defender.alignment) {
            Buff.prolong(defender, Paralysis.class, 5f);
        }
        return super.proc(attacker, defender, damage);
    }
}