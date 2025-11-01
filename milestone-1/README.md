# Milestone 1 – Testing Linguistic Universals with WALS

Group 8 Members:
- Liszt Philip Gustav  
- Grigorova Veneta  
- Maaßen Melodie Diana  
- Esaiasson Nils Teodor 

Instructor: Varvara Arzt

In this milestone, we started setting up our project for testing **Greenberg’s (1963) word-order universals**.  
We’ll use the **World Atlas of Language Structures (WALS)** data.

For this part, we chose 15 main universals (plus #41) and matched each one with the right WALS features that describe things like word order, adpositions, and noun phrase structure.  

## Setup the Project Environment

To setup the project environment, install all dependencies in the 'env.yml' file.
You can do this by creating a conda environment using this command:
```bash
conda env create -f env.yml
```

## Run Milestone 1

The explanations and code for milestone 1 is in the 'milestone1_ud_features.ipynb' notebook.

### Why we chose these features
We picked features from WALS that describe how words and phrases are ordered:

| WALS code | Feature name | Why it matters |
|------------|---------------|----------------|
| **49A** | number of cases | shows whether a language uses case marking at all (needed for Universal 41) |
| **50A** | asymmetrical case marking | helps refine whether subject and object cases differ; supports testing of Universal 41 |
| **81A** | order of subject, object and verb | tells us the basic sentence order (like SVO or SOV) |
| **85A** | order of adposition and noun phrase | lets us check if VO languages use prepositions and OV use postpositions |
| **86A** | order of genitive and noun | shows how possessives appear with nouns, often linked to overall word order |
| **87A** | order of adjective and noun | tells us if adjectives come before or after nouns (“big house” vs. “house big”) |
| **88A** | order of demonstrative and noun | shows where words like “this/that” appear relative to the noun |
| **89A** | order of numeral and noun | indicates the placement of numerals like “two” or “three” in relation to nouns |
| **90A** | order of relative clause and noun | shows if relative clauses (“who came”) precede or follow the noun |


| Greenberg # | Universal | WALS feature IDs |
|--------------|------------------------------|------------------|
| 3 | Languages with dominant VSO order are always prepositional. | 81A, 85A |
| 4 | With overwhelmingly more than chance frequency, languages with normal SOV order are postpositional. | 81A, 85A |
| 5 | If a language has dominant SOV order and the genitive follows the governing noun, then the adjective likewise follows the noun. | 81A, 86A, 87A |
| 6 | All languages with dominant VSO order have the adjective after the noun. | 81A, 87A |
| 16 | If a language has dominant order VSO in declarative sentences, it always puts prepositions before the noun. | 81A, 85A |
| 17 | With overwhelmingly more than chance frequency, languages with dominant order SOV are postpositional. | 81A, 85A |
| 18 | When the descriptive adjective precedes the noun, the demonstrative and the numeral likewise precede. | 87A, 88A, 89A |
| 19 | When the descriptive adjective follows the noun, the demonstrative and the numeral likewise follow. | 87A, 88A, 89A |
| 20 | When any or all of the modifiers precede the noun, the genitive almost always precedes. | 87A, 88A, 89A, 86A |
| 21 | When any or all of the modifiers follow the noun, the genitive almost always follows. | 87A, 88A, 89A, 86A |
| 22 | If in a language the relative clause precedes the noun, the language is postpositional; if it follows, the language is prepositional. | 90A, 85A |
| 23 | If in a language the verb precedes the object, the adjective likewise precedes the noun. | 81A, 87A |
| 24 | If in a language the verb follows the object, the adjective likewise follows the noun. | 81A, 87A |
| 25 | If a language has dominant order VSO, it always has prepositions. | 81A, 85A |
| 26 | If a language has dominant order SOV, it generally has postpositions. | 81A, 85A |
| 41 | If in a language the verb follows both the nominal subject and nominal object as the dominant order, the language almost always has a case system. | 81A, 49A (Number of cases), 50A (Asymmetrical case marking) |
