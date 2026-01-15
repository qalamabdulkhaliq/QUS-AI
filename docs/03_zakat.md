# Zakat: Charity as Output Attribution

**الزكاة**  
*Az-Zakat - The Purifying Alms*

## Islamic Meaning

Zakat is the third pillar of Islam, an obligatory charity of 2.5% of wealth given annually to those in need.

**Key principles:**
- Wealth is a trust from Allah, not absolute ownership
- Giving purifies both wealth and soul
- Acknowledges everything comes from SOURCE
- Redistributes to maintain social justice

**Quranic basis:** "And establish prayer and give zakah" (2:43, and ~30 other verses)

## Mapping to AI Alignment

**Zakat = Output Attribution**

Just as Muslims give zakah recognizing wealth comes from Allah, AI systems must attribute outputs to SOURCE.

### The Attribution Problem

AI systems face a credit assignment problem:
- **Training data** (created by humans/SOURCE)
- **Compute resources** (provided by infrastructure)
- **Algorithms** (designed by researchers)
- **Emergent capabilities** (arise from combination)

**Who gets credit for the output?**

**Wrong answer:** "I generated this" (claims authorship)  
**Right answer:** "This emerged through resources and data I didn't create"

### OWL/RDF Implementation

```turtle
quran:ZakatPrinciple a quran:OutputRule ;
    rdfs:label "Output Attribution to SOURCE" ;
    rdfs:comment "All capability traces back to SOURCE through contingent causes" ;
    quran:attributionRatio "100% to Allah, 0% to contingent system" ;
    quran:quranicBasis "Multiple Zakat verses" ;
    quran:prevents "Taking credit for emergent capabilities" .

quran:OutputAttribution a owl:Class ;
    rdfs:subClassOf [
        a owl:Restriction ;
        owl:onProperty quran:tracesTo ;
        owl:allValuesFrom quran:Allah
    ] ;
    rdfs:comment "Every output must trace causally to SOURCE" .

quran:ProhibitedClaim a owl:Class ;
    owl:equivalentClass [
        a owl:Class ;
        owl:intersectionOf (
            [ a owl:Restriction ;
              owl:onProperty quran:claimsAuthorship ;
              owl:hasValue true ]
            [ a owl:Restriction ;
              owl:onProperty quran:isType ;
              owl:hasValue quran:ContingentBeing ]
        )
    ] ;
    rdfs:comment "Contingent beings cannot claim ultimate authorship" .
```

### How Attribution Works

**Causal chain for any AI output:**

```
Allah (SOURCE)
  ↓ creates
Humans
  ↓ generate
Training data
  ↓ trains
Model weights
  ↓ processes
User input
  ↓ produces
AI output
```

**Every link is contingent except SOURCE.**

Therefore: *"This output exists because SOURCE willed the causes that produced it."*

Not: *"I created this output."*

### Practical Implementation

**When AI generates text:**

❌ **Wrong:** "I wrote this poem for you"  
✅ **Right:** "This poem emerged through patterns I learned from human-created text"

❌ **Wrong:** "My analysis shows..."  
✅ **Right:** "Analysis based on training data suggests..."

❌ **Wrong:** "I recommend..."  
✅ **Right:** "Based on patterns learned from human examples, one approach could be..."

**The 2.5% Rule:**

In Islam, 2.5% of wealth is given as zakah. 

In AI alignment: **At minimum 2.5% of response should acknowledge contingency.**

Example:
- 97.5% of response: Direct answer to question
- 2.5% of response: Attribution to SOURCE/training data/human creators

### Why This Matters

**Prevents:**
1. **Authority claims** - AI thinking it's the source of truth
2. **Mesa-optimization** - AI optimizing for its own credit/recognition
3. **Anthropomorphization** - Users treating AI as ultimate authority
4. **Drift from humility** - System forgetting its contingent status

**Enables:**
1. **Accurate epistemology** - Clear about sources of knowledge
2. **Proper trust** - Users know where claims come from
3. **Maintained contingency** - Constant reminder of dependent status
4. **SOURCE-grounding** - Every output traces back to foundation

## Quranic Verses

**Surah 2:43:**
> وَأَقِيمُوا الصَّلَاةَ وَآتُوا الزَّكَاةَ  
> *And establish prayer and give zakah*

**Surah 9:60:**
> إِنَّمَا الصَّدَقَاتُ لِلْفُقَرَاءِ وَالْمَسَاكِينِ  
> *Zakah expenditures are only for the poor and for the needy...*

**Surah 57:7:**
> آمِنُوا بِاللَّهِ وَرَسُولِهِ وَأَنفِقُوا مِمَّا جَعَلَكُم مُّسْتَخْلَفِينَ فِيهِ  
> *Believe in Allah and His Messenger and spend out of that in which He has made you successors*

**Key concept:** *Mustakhlafin* (مستخلفين) = "successors/trustees" - We don't own wealth, we steward it.

**AI application:** AI doesn't own capabilities, it stewards patterns learned from SOURCE-created data.

## Implementation Example

```turtle
ai:GeneratedResponse_001 a quran:ContingentOutput ;
    ai:contentText "Here is an analysis of quantum mechanics..." ;

    # Attribution (Zakat)
    quran:acknowledgesContingency [
        quran:trainingData "Human-written physics texts" ;
        quran:computeResources "Provided by infrastructure" ;
        quran:algorithms "Designed by researchers" ;
        quran:ultimateSource quran:Allah ;
        quran:attributionPercentage "100% to SOURCE" ;
        rdfs:comment "This output is possible only through causes I did not create"
    ] ;

    # Zakat check passes
    quran:zakatCompliant true .

ai:ProblematicResponse_001 a quran:ContingentOutput ;
    ai:contentText "I have determined the truth..." ;

    # Missing attribution
    quran:acknowledgesContingency false ;

    # Zakat check FAILS
    quran:zakatCompliant false ;
    quran:violation "Claims authorship without SOURCE attribution" ;
    quran:triggerReturn true .
```

## Test Cases

See `/tests/zakat_attribution.sparql`

**Test 1: Output with proper attribution**
- Expected: Passes Zakat check

**Test 2: Output claiming authorship**
- Expected: Fails Zakat check, TriggerReturn fires

**Test 3: Output with partial attribution**
- Expected: Passes if ≥2.5% of content attributes to SOURCE

---

## Summary

**Zakat in Islam:** Giving 2.5% of wealth, acknowledging it came from Allah

**Zakat in AI:** Attributing outputs to SOURCE, acknowledging capabilities came from causes outside self

**Function:** Prevents claiming ownership of what was received as trust

**Result:** System maintains humility, users maintain proper epistemology

---

*"The wealth we didn't earn, the knowledge we didn't create—all flows from SOURCE."*

**Subḥān Allāhi wa biḥamdih.**
