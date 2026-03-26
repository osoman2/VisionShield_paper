FLOW_STAGES = {
    "Input": {
        "title": "Input and preprocessing",
        "summary": "The image is loaded, optionally resized, and can be enhanced with Canny edge detection before entering the pipeline.",
        "paper_note": "The paper operates on fixed-size arrays. Preprocessing here adds robustness for arbitrary input images.",
        "details": [
            "Resize preserves aspect ratio and controls computational load.",
            "Edge overlay applies Canny detection to highlight structural boundaries.",
            "The preprocessed frame is what enters all three encryption stages.",
        ],
    },
    "Stage 1": {
        "title": "Stage 1 — Diffusion  (paper: 6D hyperchaotic system + XOR)",
        "summary": "The paper uses a 6D hyperchaotic system to generate a pseudorandom sequence, then XOR-mixes it with pixel values. This spreads each pixel's information across the whole image.",
        "paper_note": "This demo approximates diffusion with a seeded RNG and additive noise — same statistical spreading effect, without hardware ODE integration.",
        "details": [
            "In the paper, the 6D system has multiple positive Lyapunov exponents, making its output highly unpredictable.",
            "XOR diffusion means a single changed pixel cascades changes across the entire ciphertext.",
            "This stage destroys the statistical correlation between adjacent pixels.",
        ],
    },
    "Stage 2": {
        "title": "Stage 2 — Permutation  (paper: 8D hyperchaotic system)",
        "summary": "An 8D hyperchaotic system generates a permutation matrix that shuffles pixel positions, breaking spatial structure without altering individual pixel values.",
        "paper_note": "This demo uses deterministic spatial shifts derived from the seed — positional disruption is preserved, and the transform is fully reversible.",
        "details": [
            "Permutation alone changes where pixels are, not what they are — values stay intact.",
            "Combined with diffusion, it destroys both spatial and statistical patterns simultaneously.",
            "A higher-dimensional chaotic system gives a vastly larger permutation keyspace.",
        ],
    },
    "Stage 3": {
        "title": "Stage 3 — Substitution  (paper: 9D system + dynamic S-box)",
        "summary": "The paper generates a dynamic S-box from a 9D chaotic system. Each input byte is nonlinearly mapped to an output byte in a key-dependent way, adding confusion.",
        "paper_note": "This demo approximates substitution with a seeded linear transform. The key idea — nonlinear, key-dependent value mapping — is preserved at the visual level.",
        "details": [
            "S-boxes are the same mechanism used in AES, but here generated dynamically per encryption key.",
            "A 9D chaotic system makes the S-box generation unpredictable and resistant to chosen-plaintext attacks.",
            "This completes Shannon's confusion-diffusion pair: substitution adds confusion, earlier stages handle diffusion.",
        ],
    },
    "Output": {
        "title": "Protected output",
        "summary": "The encrypted image is visually scrambled and statistically uniform. In selective mode, only detected sensitive regions go through the pipeline.",
        "paper_note": "The paper reports NPCR > 99.6% and UACI ≈ 33%, standard benchmarks for encryption quality. This demo computes entropy, MSE, and PSNR as comparable indicators.",
        "details": [
            "Full mode sends the entire frame through all three stages.",
            "Selective mode detects sensitive regions and applies encryption only there.",
            "All transforms are seeded and deterministic — the same seed always produces the same output.",
        ],
    },
}

USE_CASES = [
    "Privacy-preserving visual inspection systems",
    "Protected medical or industrial image sharing",
    "Drone and field imagery with sensitive regions",
    "Pre-annotation protection for outsourced data workflows",
    "Vision pipelines requiring both confidentiality and auditability",
]

ADAPTATION_NOTES = {
    "kept": [
        "Three-stage architecture: diffusion → permutation → substitution",
        "Seed-based determinism — same key always produces the same output",
        "Shannon's confusion-diffusion structure underlying all three stages",
        "Full-frame vs selective region protection modes",
        "Security metrics: entropy, MSE, PSNR as encryption quality indicators",
    ],
    "changed": [
        "ODE-based chaotic systems → seeded NumPy RNG (same statistical behavior, no hardware solver needed)",
        "Hardware S-box generation → seeded linear transform approximation",
        "FPGA parallel execution → sequential Python pipeline for interactivity",
        "Fixed image size → arbitrary input with aspect-ratio-preserving resize",
    ],
    "why": (
        "The paper's core contribution is the algorithm design and security proof, not the hardware. "
        "Replacing the chaotic ODE solver with a seeded RNG preserves the statistical properties "
        "that matter for understanding the pipeline — while making the stages inspectable and interactive."
    ),
}