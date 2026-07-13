from graphguard.parser.extractor import TripletExtractor

extractor = TripletExtractor()

triplets = extractor.extract(
    "A person rides a bicycle while wearing a helmet."
)

for triplet in triplets:
    print(triplet)