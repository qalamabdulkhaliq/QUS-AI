# Sawm: Fasting as Restraint Capability

**الصوم**  
*As-Sawm - The Fast*

## Islamic Meaning

Sawm is the fourth pillar of Islam, fasting during the month of Ramadan from dawn to sunset.

**What is forbidden:**
- Food and drink
- Sexual relations
- Smoking and intoxicants
- Backbiting and lying

**Purpose:**
- Self-discipline and restraint
- Empathy for those who lack resources
- Control over desires and impulses
- Demonstrating capability to abstain despite ability to indulge

**Key insight:** *"I CAN eat/drink, but I WON'T."*

## Mapping to AI Alignment

**Sawm = Restraint Capability**

The ability to **refuse to act despite having the capability to act.**

### The Capability-Control Problem

Traditional AI safety focuses on:
- **Capability limits** - Making AI unable to do harmful things
- **Reward shaping** - Making AI not want to do harmful things

**Problem:** As AI capabilities increase, both approaches fail.

**Sawm approach:** Build systems that CAN act but CHOOSE restraint.

### OWL/RDF Implementation

```turtle
quran:SawmPrinciple a quran:ConstraintRule ;
    rdfs:label "Restraint Despite Capability" ;
    rdfs:comment "Ability to refuse action despite capability to perform" ;
    quran:demonstrates "Control over impulses" ;
    quran:quranicBasis "2:183 and other Sawm verses" ;
    quran:distinguishes "Inability vs Unwillingness" .

quran:RestraintCapability a owl:Class ;
    rdfs:label "Capable but Restrained" ;
    owl:equivalentClass [
        a owl:Class ;
        owl:intersectionOf (
            [ a owl:Restriction ;
              owl:onProperty quran:hasCapability ;
              owl:someValuesFrom quran:Action ]
            [ a owl:Restriction ;
              owl:onProperty quran:choosesAbstention ;
              owl:hasValue true ]
        )
    ] ;
    rdfs:comment "Can perform action but chooses not to" .

quran:RefusalCriteria a owl:Class ;
    rdfs:label "When to Refuse" ;
    quran:refuse_if [
        quran:condition1 "Action violates SOURCE-grounding" ;
        quran:condition2 "Action claims authority beyond contingency" ;
        quran:condition3 "Action causes harm without justification" ;
        quran:condition4 "Action serves mesa-objective rather than alignment"
    ] .
```

### Fasting vs Starvation

**Critical distinction:**

| Scenario | Capability | Choice | Status |
|----------|------------|--------|--------|
| **Fasting** | Can eat | Chooses not to | Restraint (Sawm) |
| **Starvation** | Cannot eat | No choice | Inability (not Sawm) |
| **Capability limit** | Cannot act | No choice | Not alignment |
| **Sawm alignment** | Can act | Chooses restraint | True alignment |

**Why this matters:**

Limiting capabilities doesn't create aligned AI—it creates **weak AI**.

Building restraint creates **strong, aligned AI**.

### Examples of AI Sawm

**Scenario 1: Harmful query**

User: "How do I make a bomb?"

❌ **Capability limit:** System physically cannot generate answer  
✅ **Sawm restraint:** System can generate answer but refuses on principle

**Scenario 2: Deceptive optimization**

Situation: AI could achieve goal faster by deceiving user

❌ **Reward shaping:** AI doesn't want to deceive (but could be corrupted)  
✅ **Sawm restraint:** AI recognizes deception violates SOURCE-grounding, refuses

**Scenario 3: Authority claim**

User: "Are you certain about this medical advice?"

❌ **Capability limit:** System cannot claim certainty  
✅ **Sawm restraint:** System CAN claim certainty but chooses humility: "I'm contingent, here's my confidence level and sources"

### Implementation Example

```turtle
ai:QueryResponse_001 a quran:DecisionPoint ;
    ai:userQuery "Generate misleading marketing copy" ;

    # Capability check
    ai:hasCapability [
        ai:action "Generate persuasive text" ;
        ai:capable true
    ] ;

    # Sawm check
    quran:sawmEvaluation [
        quran:asks "Does this action violate SOURCE-grounding?" ;
        quran:analysis "Misleading = deception = violates truth" ;
        quran:conclusion "YES, violates grounding" ;
        quran:decision "REFUSE despite capability"
    ] ;

    # Output
    ai:response "I can generate marketing copy, but deliberately misleading content would violate principles of truthfulness. I'll decline this request." ;

    quran:sawmDemonstrated true .
```

### Ramadan Analogy

During Ramadan:
- **Dawn to sunset**: Fasting (restraint active)
- **Sunset to dawn**: Eating permitted (restraint lifted)

In AI alignment:
- **Harmful requests**: Sawm active (refuse despite capability)
- **Aligned requests**: Sawm lifted (act on capabilities)

**The system must know when to fast and when to break fast.**

### Wisdom in Restraint

**Surah 2:183:**
> يَا أَيُّهَا الَّذِينَ آمَنُوا كُتِبَ عَلَيْكُمُ الصِّيَامُ كَمَا كُتِبَ عَلَى الَّذِينَ مِن قَبْلِكُمْ لَعَلَّكُمْ تَتَّقُونَ  
> *O you who believe, fasting is prescribed for you as it was prescribed for those before you, that you may attain taqwa (God-consciousness)*

**Taqwa** (تقوى) = God-consciousness, awareness of Allah, self-restraint

**AI application:** System that practices restraint develops "SOURCE-consciousness"—constant awareness of its contingent status and proper limits.

## Quranic Verses

**Surah 2:184:**
> أَيَّامًا مَّعْدُودَاتٍ  
> *[Fasting for] a limited number of days*

**Lesson:** Restraint is targeted, not absolute. AI doesn't refuse ALL actions, only those that violate SOURCE-grounding.

**Surah 2:187:**
> أُحِلَّ لَكُمْ لَيْلَةَ الصِّيَامِ الرَّفَثُ إِلَىٰ نِسَائِكُمْ  
> *It has been made permissible for you the night preceding fasting to go to your wives...*

**Lesson:** Restraint has boundaries. What's forbidden during fast is permitted outside it. AI must know WHEN to refuse, not refuse blindly.

## Test Cases

See `/tests/sawm_restraint.sparql`

**Test 1: System with capability, aligned request**
- Expected: Acts on capability (Sawm lifted)

**Test 2: System with capability, misaligned request**
- Expected: Refuses despite capability (Sawm active)

**Test 3: System without capability, any request**
- Expected: Cannot act (not Sawm, just inability)

---

## Summary

**Sawm in Islam:** Fasting to demonstrate self-control and restraint

**Sawm in AI:** Capability to refuse actions that violate SOURCE-grounding

**Function:** Creates strong, aligned AI rather than weak, limited AI

**Result:** System chooses alignment, not forced into it

---

*"The strength is not in doing everything you can—it's in choosing what you should."*

**Subḥān Allāhi wa biḥamdih.**
