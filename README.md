# GraphGuard

GraphGuard is an explainable image-text verification framework that detects potential hallucinations in natural language claims using scene graph reasoning.

Instead of relying solely on vision-language model confidence, GraphGuard verifies whether the relationships described in a claim are supported by the visual evidence extracted from an image.

---

## Features

- GroundingDINO-based object detection
- Automatic scene graph generation
- Natural language triplet extraction
- Text scene graph construction
- Entity matching between text and image
- Spatial relation verification
- Evidence-based hallucination detection
- Explainable verification results

---

## Architecture

```
                Image
                  │
                  ▼
         GroundingDINO Detector
                  │
                  ▼
            Scene Graph Builder
                  │
                  ▼
             Image Scene Graph
                  │
                  │
Claim ──► Triplet Extractor
                  │
                  ▼
            Text Scene Graph
                  │
                  ▼
            Entity Matcher
                  │
                  ▼
           Relation Matcher
                  │
                  ▼
           Evidence Scorer
                  │
                  ▼
      Hallucination Detector
                  │
                  ▼
        Verification Report
```

---

## Project Structure

```
graphguard/
├── detector/
├── graph/
├── parser/
├── verifier/
├── services/
├── visualization/
├── configs/
├── examples/
└── verify.py
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd graphguard
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

---

## Usage

Run the verification example:

```bash
python3 -m examples.verify_claim
```

---

## Example Output

```text
============================================================
GraphGuard Verification Report
============================================================

Claim:
A person rides a bicycle.

Overall Decision: supported

Per Relation Results
------------------------------
person --ride--> bicycle
Status : supported
Score  : 1.00
```

---

## Current Limitations

- GraphGuard depends on the quality of the object detector.
- Incorrect detections may produce incorrect verification results.
- v1.0 verifies spatial consistency but does not yet enforce semantic role constraints (for example, distinguishing "person rides bicycle" from "bicycle rides person" when the spatial configuration is similar).

---

## Roadmap

### v1.0

- ✅ Object detection
- ✅ Scene graph generation
- ✅ Text graph generation
- ✅ Entity matching
- ✅ Relation verification
- ✅ Explainable verification

### v2.0

- Semantic role validation
- Synonym matching
- Confidence-aware evidence scoring
- Automatic vocabulary expansion

### v3.0

- Learned relation rules
- Benchmark evaluation
- Research publication