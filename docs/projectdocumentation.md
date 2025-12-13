# Project Documentation

## 1. Problem Statement

Modern e-commerce platforms require structured, reliable, and reproducible product content. For skincare and wellness products in particular, users expect clear FAQs, transparent ingredient listings, safe usage instructions, and consistent product summaries.

Manually creating such content is repetitive, error-prone, and difficult to scale. While Large Language Models can assist, uncontrolled generation often leads to hallucinations, inconsistent formats, and brittle outputs that are unsuitable for production systems.

The objective of this project is to design a **deterministic, agent-based content generation system** that produces **strictly structured JSON outputs** for:

- A FAQ Page  
- A Product Description Page  
- A Comparison Page  

The system must:

- Enforce minimum content requirements (e.g., ≥15 FAQs)
- Avoid hallucinated claims
- Run locally without proprietary APIs
- Demonstrate agent-based design using an accepted orchestration framework

---

## 2. Solution Overview

This solution implements a **multi-agent content generation pipeline** using **CrewAI-compatible agents combined with deterministic execution logic**.

Each agent is responsible for a single, well-defined task, while a central orchestrator coordinates execution and manages shared inputs. Local open-source language models from the **FLAN-T5 family** are used selectively, with deterministic fallbacks ensuring system reliability when model inference fails.

All outputs are rendered from **predefined JSON templates** using a **safe Jinja2-based template engine**, guaranteeing valid and reproducible structures.

### High-Level Flow

1. Load and normalize input product data  
2. Generate or fallback to a minimum set of FAQs  
3. Render structured product content from templates  
4. Produce a deterministic comparison document  
5. Persist all outputs as valid JSON  

This design prioritizes **robustness, reproducibility, and clarity** over free-form generation.

---

## 3. Scope and Assumptions

### In Scope

- Single-product JSON input
- Deterministic generation of:
  - FAQ Page (≥15 questions)
  - Product Page
  - Comparison Page
- Use of CrewAI-compatible agents
- Local LLM usage with safe fallback
- Template-driven JSON rendering
- Pytest-based automated testing

### Out of Scope

- Real-time APIs or UI layers
- Multi-product comparison logic
- Domain-specific regulatory validation
- External search or retrieval augmentation

### Assumptions

- Input product JSON is structurally valid
- Templates define the authoritative output schema
- Agents communicate only via explicit inputs and outputs
- Local models may be unavailable and must fail safely

---

## 4. System Design

### 4.1 Architectural Overview

The system follows a **modular agent-based architecture**.

Each agent encapsulates a single responsibility and is orchestrated through a central controller. CrewAI is used to demonstrate agent orchestration semantics, while actual execution logic remains deterministic, testable, and reproducible.

#### Core Components

**FAQ Agent**  
Generates or enforces a minimum of 15 FAQs using a local LLM or deterministic fallback logic.

**Product Page Agent**  
Renders structured product data (benefits, ingredients, usage, safety, pricing) into a JSON template.

**Comparison Page Agent**  
Produces a structured comparison JSON. In the single-product scenario, the product is compared with itself to preserve schema integrity.

**LLM Client (Singleton)**  
Centralized loader for FLAN-T5 models. Ensures models are loaded once and reused across agents to avoid repeated initialization overhead.

**Template Engine (Jinja2)**  
Safely injects agent-produced data into JSON templates without unsafe string replacement or fragile parsing.

**Hybrid Orchestrator**  
Coordinates agent execution order and output persistence. CrewAI agents are instantiated for architectural compliance, while deterministic agent logic produces the final artifacts.

> **Note:** While execution order is linear, the documentation intentionally avoids claiming a full computational DAG to prevent architectural misrepresentation.

---

### 4.2 Execution Flow

1. The orchestrator loads the input product JSON.
2. The FAQ agent generates FAQs using the LLM or fallback logic.
3. The FAQ template is rendered into a valid JSON document.
4. The product page agent renders structured product data.
5. The comparison agent generates comparison output.
6. All outputs are written to the `outputs/` directory.

Each step executes exactly once, ensuring predictability and reproducibility.

---

### 4.3 Error Handling and Reliability

The system includes layered safeguards:

- **LLM Fallbacks:** Deterministic JSON is returned if model inference fails.
- **Singleton Model Loading:** Prevents repeated memory-heavy model initialization.
- **Template Validation:** Jinja templates enforce valid JSON structure.
- **Defensive Access Patterns:** Missing product fields are handled safely using defaults.
- **Automated Tests:** Pytest validates schema correctness, minimum content requirements, and orchestration outputs.

These measures ensure stable execution even under degraded model conditions.

---

### 4.4 Testing Strategy

The project includes a comprehensive **pytest-based test suite** covering:

- Minimum FAQ enforcement (≥15)
- FAQ schema validation
- Product page JSON validity
- Comparison logic correctness
- Singleton LLM behavior
- Fallback behavior when LLM is unavailable
- Orchestrator output completeness
- Configuration integrity

All tests are deterministic, fast, and offline-safe, requiring no external services.

---

## 5. Extensibility

The architecture supports future growth:

- New content types can be added by introducing new agents and templates.
- LLM models can be swapped without modifying agent logic.
- Multi-product comparison can be added by extending the comparison agent.
- Retrieval or ranking agents can be integrated upstream if required.

This design favors **clarity, correctness, and maintainability** over opaque generative pipelines.

---

## 6. Conclusion

This project demonstrates a **production-aware, agent-based content generation system** that balances the power of local LLMs with deterministic safeguards.

By combining CrewAI-compatible agents, centralized model management, template-driven rendering, and professional testing practices, the system delivers reliable, reproducible, and auditable outputs suitable for real-world e-commerce workflows.
