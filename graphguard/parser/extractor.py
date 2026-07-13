import spacy

from graphguard.parser import Triplet


class TripletExtractor:

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract(self, text: str) -> list[Triplet]:
        doc = self.nlp(text)
        triplets = []

        for token in doc:
            if token.pos_ != "VERB":
                continue

            # Extract and normalize the relation inside the loop
            relation = token.lemma_.lower()
            if relation == "rid":
                relation = "ride"
            elif relation == "wore":
                relation = "wear"

            subject = None
            obj = None

            for child in token.children:
                if child.dep_ in ("nsubj", "nsubjpass"):
                    subject = child.text
                elif child.dep_ in ("dobj", "pobj", "attr", "obj"):
                    obj = child.text

            if subject and obj:
                triplets.append(
                    Triplet(
                        subject=subject.lower(),
                        relation=relation,
                        object=obj.lower(),
                    )
                )

        return triplets
