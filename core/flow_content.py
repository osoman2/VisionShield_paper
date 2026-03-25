FLOW_STAGES = {
    "Input": {
        "title": "Input and preprocessing",
        "summary": "The system receives an input image, optionally resizes it, and can enrich structure visibility with edge overlay.",
        "details": [
            "Image loading is robust and ready for user uploads.",
            "OpenCV preprocessing makes the demo more production-like.",
            "This stage prepares the asset for later protection and analysis.",
        ],
    },
    "Stage 1": {
        "title": "Stage 1: seeded diffusion",
        "summary": "A seed-derived transformation modifies pixel values and starts destroying direct visual readability.",
        "details": [
            "Inspired by the first chaos-based stage of the paper.",
            "Acts as an early diffusion layer.",
            "Useful for explaining deterministic but hard-to-read transformations.",
        ],
    },
    "Stage 2": {
        "title": "Stage 2: structural permutation",
        "summary": "Spatial organization is disrupted so that local neighborhoods lose their original meaning.",
        "details": [
            "Reduces recoverable spatial coherence.",
            "Makes the image less interpretable even if some information remains visible.",
            "Narratively aligned with the second chaos-inspired layer.",
        ],
    },
    "Stage 3": {
        "title": "Stage 3: nonlinear substitution",
        "summary": "A final substitution-like step further randomizes the protected output.",
        "details": [
            "Simulates dynamic S-box behavior at a portfolio-demo level.",
            "Produces stronger visual scrambling and histogram shift.",
            "Completes the three-stage storytelling of the paper-inspired pipeline.",
        ],
    },
    "Output": {
        "title": "Protected output and product framing",
        "summary": "The output is presented as a privacy-aware visual asset, not merely as a cryptographic artifact.",
        "details": [
            "Can protect the whole frame or only selected sensitive zones.",
            "Supports blur-based masking or stronger encryption-like obfuscation.",
            "Bridges secure imaging and applied computer vision product design.",
        ],
    },
}

USE_CASES = [
    "Privacy-preserving visual inspection systems",
    "Protected medical or industrial image sharing",
    "Drone and field imagery with sensitive regions",
    "Pre-annotation protection for outsourced data workflows",
    "Vision pipelines that must preserve explainability and confidentiality",
]

DISRUPTIVE_ANGLE = [
    "Reframes image encryption as a product system, not just a paper reproduction",
    "Adds user-facing explanation, visual analysis, and selective protection modes",
    "Blends privacy, computer vision, and system design into one artifact",
    "Makes a cryptography-inspired idea understandable to recruiters, founders, and engineering managers",
]