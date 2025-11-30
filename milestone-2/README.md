## Milestone 2

### (a) Universals that are strongly supported

From our cross-table of word order vs adposition type:

- VO languages (SVO + VSO + VOS) with clear data:
  - prepositional: 326 (SVO) + 96 (VSO) + 39 (VOS) = 461
  - postpositional: 46 (SVO) + 6 (VSO) + 0 (VOS) = 52

So about 90% of VO languages use prepositions and only about 10% use postpositions.

- OV languages (SOV + OSV + OVS) with clear data:
  - prepositional: 17 (SOV) + 0 (OSV) + 3 (OVS) = 20
  - postpositional: 381 (SOV) + 3 (OSV) + 10 (OVS) = 394

So about 95% of OV languages use postpositions.

In WALS, VO languages very strongly prefer prepositions, and OV languages very strongly prefer postpositions. This is a strongly supported trend, even though there are a few exception

### (b) Universals with many exceptions

The data shows these adjective-based universals are not strong rules:

- in 661 VO languages (verb before object):
  - 146 have adjective before noun. 22% follow the universal
  - 483 have adjective after noun. 78% break it. This universal fails for most VO languages.

- in 587 OV languages (object before verb):
  - 308 have adjective after noun. 52% follow the universal
  - 146 have adjective before noun. 48% break it. Only about half follow.

These are weak trends, not strong, universal rules.

### (c) Rule-based vs. Decision Tree baseline
- the rule-based baseline is easy to explain because every decision comes from a clear if&rarr;then rule, but it breaks often because real languages are more complex.
- the decision tree model gets higher accuracy because it can learn combinations of features and also learn exceptions, but the decisions are less tied to linguistic theory.

### Bias
WALS does not represent all languages equally. Europe and big Eurasian families have much more data than languages from Africa, the Americas, or the Pacific. Also, similar languages from the same family appear together, which can make a pattern look stronger than it really is.