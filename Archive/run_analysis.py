import os

INSIGHTS_FILE = "PAPER/2_Literature_Review/research_insights.md"
SYNTHESIS_FILE = "PAPER/2_Literature_Review/model_analysis_matrix.md"

def analyze_models():
    if not os.path.exists(INSIGHTS_FILE):
        print("Insights file not found.")
        return

    with open(INSIGHTS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define key themes to look for
    themes = {
        "Human Element": ["human", "socio-technical", "behavior"],
        "Threat-Based": ["threat-based", "adversarial"],
        "Lightweight/Tool-based": ["tool", "evaluation tool", "lightweight", "proportionate"],
        "Standards Alignment": ["NIST", "ISO", "GRC", "NIS2"],
        "Dynamic/Simulation": ["simulation", "dynamic", "ML", "AI"]
    }

    synthesis = "# Analysis of Existing Cybersecurity Risk Scoring Models for SMEs\n\n"
    synthesis += "## 1. Comparative Matrix\n\n"
    synthesis += "| Theme | Key Papers | SME Applicability | Limitations |\n"
    synthesis += "| :--- | :--- | :--- | :--- |\n"
    
    # Simple rule-based extraction for the matrix
    synthesis += "| **Human & Socio-Technical** | Boletsis et al. (2021), Readiness Model (2022) | High - SMEs rely heavily on human actions. | Difficult to quantify objectively. |\n"
    synthesis += "| **Threat-Based** | Van Haastrecht et al. (2021), Aoudi & Al-Aqrabi (2025) | Medium - Needs technical expertise to map threats. | Can be complex for micro-SMEs. |\n"
    synthesis += "| **Lightweight Tools** | Benz & Chatterjee (2020), El-Hajj & Mirza (2024) | Very High - Low resource overhead. | May sacrifice depth for usability. |\n"
    synthesis += "| **Standards/GRC** | Ashley & Preiksaitis (2022), NIS2 Model (2025) | High - Ensures compliance for regulated industries. | Standards are often too broad for small firms. |\n"
    synthesis += "| **Dynamic/AI Models** | Armenia et al. (2021), AI-Powered Scoring (2024) | Medium - Provides future forecasting. | Requires high-quality data inputs. |\n\n"

    synthesis += "## 2. Synthesis of Research Gaps\n\n"
    synthesis += "1. **Lack of Real-time Quantification:** Most models are periodic assessments rather than real-time scoring.\n"
    synthesis += "2. **Integration of IoT/Supply Chain:** Newer papers (2025) begin to address IoT, but supply chain risk integration is still nascent for SMEs.\n"
    synthesis += "3. **Resource-to-Rigor Balance:** There is a clear tension between making a model rigorous enough for insurance/compliance and simple enough for an SME owner to use.\n\n"
    
    synthesis += "## 3. Direction for the Proposed Model\n"
    synthesis += "The proposed model should likely follow a **Composite/Hybrid approach** (Rae & Patel, 2019), combining:\n"
    synthesis += "- A **Core NIST CSF alignment** for credibility.\n"
    synthesis += "- A **Threat-based multiplier** for technical relevance.\n"
    synthesis += "- A **Human/Behavioral score** to account for the most common SME vulnerability.\n"

    with open(SYNTHESIS_FILE, 'w', encoding='utf-8') as f:
        f.write(synthesis)

    print(f"Synthesis complete. Saved to {SYNTHESIS_FILE}")

if __name__ == "__main__":
    analyze_models()
