# Project Documentation

## 1. Problem Statement
Modern e-commerce platforms rely heavily on structured and trustworthy product content. For skincare and wellness products, buyers expect clear benefits, detailed usage instructions, safety guidance, ingredient transparency, and meaningful comparisons with similar items. Manually producing this content is repetitive, time-consuming, and error-prone.

The goal is to design and implement an automated multi-agent system that generates three essential product documents:

* A structured FAQ Page
* A structured Product Description Page
* A Comparison Page

All outputs must strictly follow predefined JSON templates, contain no hallucinated information, and rely only on the provided product data. The system must run without relying on a single GPT wrapper and must demonstrate agent-based modular design.

## 2. Solution Overview
The solution is a multi-agent content generation pipeline driven by a Directed Acyclic Graph (DAG). Each agent independently performs a focused task, while the orchestrator coordinates execution in a controlled sequence.

The system accepts a single input product and performs the following steps:

1.  Parses the raw product data and ensures structural consistency.
2.  Generates user-facing questions using a local LLM (BART) with deterministic fallback.
3.  Fills predefined JSON templates to produce a FAQ Page, Product Page, and Comparison Page.
4.  Ensures all content is derived solely from product data, avoiding assumptions.
5.  Produces consistently structured and reproducible JSON outputs.

This modular approach enables clear separation of responsibilities, easy extensibility, and predictable output quality.

## 3. Scopes and Assumptions

### In Scope
* Accepting a single well-formed product JSON as input.
* Producing three output documents strictly based on provided templates.
* Using local LLM models for question generation.
* Enforcing content safety: no claims beyond the input dataset.
* Structured, deterministic output through template-driven design.
* Multi-agent execution controlled by a DAG.

### Out of Scope
* Handling multiple products simultaneously in comparison mode.
* Real-time inference, UI layers, or API endpoints.
* Automatic correction of incomplete or inconsistent input.
* Domain-specific regulatory or medical validation.

### Key Assumptions
* Input JSON contains all essential fields (product name, benefits, ingredients, usage, safety, pricing).
* Template structures remain fixed and are the authoritative schema for output format.
* Agents operate independently and do not share internal state beyond explicit inputs and outputs.
* Local models are available and suitable for generating text without external API calls.

## 4. System Design

### 4.1 Architectural Overview
The architecture is intentionally modular. Each agent specializes in one responsibility, and a top-level orchestrator governs the overall data flow, forming a DAG-based execution pattern.

The major components are:

* **Parser Agent:** Responsible for loading and validating the product input. Produces a normalized product object consumed by downstream agents.
* **Question Generation Agent:** Generates categorized user questions using a local LLM (BART), ensuring coverage across usage, safety, ingredients, pricing, benefits, and comparison. Provides deterministic fallback for reliability.
* **FAQ Page Agent:** Uses the generated questions and product data to populate the FAQ JSON template. Produces a hallucination-free FAQ document.
* **Product Page Agent:** Uses defined template fields to assemble structured content blocks, including benefits, ingredients, usage, safety, and pricing.
* **Comparison Page Agent:** Builds a comparison document between two products. In a single-product scenario, the product is compared with itself to preserve template integrity.
* **Template Engine:** Injects agent-produced values into JSON templates safely. Ensures only valid JSON is produced and prevents uncontrolled free-text insertion.
* **DAG Orchestrator:** Executes all agents in the correct order. Ensures data dependencies are satisfied and that every component runs exactly once.

### 4.2 Data Flow Summary
1.  The orchestrator loads the raw product JSON.
2.  The parser agent validates and structures the data.
3.  The question generation agent produces categorized questions.
4.  The FAQ agent receives both the product data and the questions and fills the FAQ template.
5.  The product page agent uses the product data to create a structured product description based on template fields.
6.  The comparison agent generates comparison content using the same product as both inputs (single-product mode).
7.  All outputs are written to JSON files within the output folder.

This flow ensures every stage is deterministic, reproducible, and compliant with template schemas.

### 4.3 Error Handling and Reliability
The system uses layered safeguards:

* Template engine performs strict validation before creating final JSON.
* LLM fallback ensures question generation always succeeds.
* Agents use defensive programming to avoid missing keys or malformed content.
* The orchestrator prevents out-of-order execution and unintended shortcuts.

These safeguards guarantee stable execution and consistent output even under degraded conditions.

### 4.4 Extensibility
The agent-based architecture allows easy expansion:

* Additional content blocks can be added without modifying existing agents.
* New templates can be integrated by simply creating new agents that consume them.
* The question generator can be upgraded with larger or domain-specific local models.
* Multi-product comparison mode can be added with minimal architectural changes.

This forward-looking design enables long-term growth beyond the assignment scope.