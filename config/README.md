# Configuration Guide

This directory contains configuration files for the Zotero Similarity Selection tool.

## reference.txt

This is the most important configuration file. It should contain a paragraph describing the scope of papers you're interested in.

### Writing a Good Reference Paragraph

Your reference text should:
1. **Be specific**: Include key terms, methods, and concepts relevant to your research
2. **Be comprehensive**: Cover main themes, applications, and approaches
3. **Be focused**: Avoid overly broad or vague descriptions
4. **Include context**: Mention related fields, techniques, or applications

### Examples

#### Example 1: Machine Learning in Healthcare
```
This research investigates the application of machine learning and artificial 
intelligence techniques to healthcare diagnostics and patient care. We focus 
on deep learning models for medical image analysis, including CNN architectures 
for radiology, pathology, and dermatology. Our work also covers natural language 
processing for clinical notes, predictive modeling for patient outcomes, and 
explainable AI methods for medical decision support. We are particularly 
interested in methods that address data privacy, model interpretability, and 
clinical validation.
```

#### Example 2: Quantum Computing Algorithms
```
This project focuses on quantum algorithms and their applications to 
optimization problems and quantum chemistry. We study variational quantum 
algorithms, quantum approximate optimization algorithms (QAOA), and quantum 
machine learning techniques. Our research includes both theoretical analysis 
of quantum algorithm complexity and practical implementations on near-term 
quantum devices (NISQ). We also consider error mitigation strategies and 
hybrid quantum-classical approaches.
```

#### Example 3: Urban Sustainability
```
Our research examines sustainable urban development through the lens of smart 
cities, green infrastructure, and urban planning. We investigate IoT sensor 
networks for environmental monitoring, data-driven approaches to traffic 
management and energy efficiency, and participatory planning methods. Key 
themes include renewable energy integration in urban settings, sustainable 
transportation systems, urban heat island mitigation, and climate adaptation 
strategies for cities.
```

### Tips for Different Use Cases

**Narrow Focus (Highly Specific Research)**
- Include specific methods, datasets, or application domains
- Mention key authors or seminal papers if relevant
- Use technical terminology

**Broad Review (Literature Survey)**
- Cover multiple approaches or subfields
- Include related areas and interdisciplinary connections
- Use more general terminology while maintaining clarity

**Interdisciplinary Research**
- Clearly state the intersection of fields
- Include key concepts from each discipline
- Mention how the fields relate to each other

### Testing and Refinement

After your first run:
1. Review the selected papers
2. Check if relevant papers were missed (too high threshold)
3. Check if irrelevant papers were included (too low threshold)
4. Refine your reference text to better capture your interests
5. Re-run with adjusted parameters

### Multiple Reference Texts

For complex projects, you might want to:
- Create multiple reference files (e.g., `reference_approach1.txt`, `reference_approach2.txt`)
- Run the tool multiple times with different references
- Combine results or compare selections

### Advanced: Programmatic Reference Generation

For systematic reviews or meta-analyses, you might generate reference text from:
- Abstracts of key papers in your field
- Your own research proposal or grant application
- Combination of multiple seed paperss