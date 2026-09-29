# 🚁 AeroRescue — Real-Time Disaster Needs Dispatch

![AeroRescue Cover Banner](aerorescue_cover.jpg)

[![AssemblyAI](https://img.shields.io/badge/Voice%20Agent-AssemblyAI-blue)](https://www.assemblyai.com/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-teal)](https://fastapi.tiangolo.com/)
[![native.builder](https://img.shields.io/badge/Built%20With-native.builder-blueviolet)](https://builder.nativelyai.com)
[![Lablab.ai](https://img.shields.io/badge/Hackathon-AssemblyAI%20Voice%20Agent-blue)](https://lablab.ai/ai-hackathons/assemblyai-voice-agent-hackathon)

> **AeroRescue** is an autonomous, voice-first disaster response and emergency triage platform built for the **AssemblyAI Voice Agent Hackathon**. It transforms chaotic, panicked audio distress calls during natural disasters (earthquakes, floods, cyclones, and wildfires) into organized, prioritized, and actionable rescue intelligence using AssemblyAI's cutting-edge **Voice Agent API** and **LeMUR** models.

---

## 🔗 Live Deliverables & Links

*   **🌐 Live Deployed Application:** [https://c0wme2t9c9cfku83yqo5roibf.nativelyai.app/](https://c0wme2t9c9cfku83yqo5roibf.nativelyai.app/)
*   **🐙 GitHub Code Repository:** [https://github.com/swatiicfai/AeroRescue-](https://github.com/swatiicfai/AeroRescue-)

---

## 🌊 Supported Disaster Scenarios

AeroRescue is engineered to parse different needs profiles across four major climate emergency categories:

| Disaster Type | Primary Hazards | Core AI Extraction Target | Primary Dispatch Unit |
| :--- | :--- | :--- | :--- |
| 🌍 **Earthquake** | Structural collapse, gas leaks, trapped victims | Rubble location, trapped counts, injury severity | USAR Search & Rescue |
| 🌧️ **Rain & Flood** | Rising floodwaters, submerged homes | Stranded level (roof/attic), boat requirements | Water Rescue & Boats |
| 🌪️ **Cyclone** | High winds, destroyed shelters, power loss | Evacuation route safety, shelter allocations | Evacuation Transport |
| 🔥 **Wildfire** | Rapidly shifting fire perimeters, smoke | Escape path clearance, oxygen & burn priority | Fire Response & Medics |

---

## 💡 The Solution & Core Workflow

AeroRescue bridges the gap between panicked victims and volunteer coordinators in less than 90 seconds:

1.  **Real-Time Voice Agent (Mobile):** A victim opens AeroRescue on their phone, and speaks naturally to our **AssemblyAI Voice Agent**. GPS coordinates are automatically captured.
2.  **Universal-3 Pro STT Engine:** Accurately converts noisy, high-speed, or breathless emergency audio into clean text transcripts with sub-second latency.
3.  **AssemblyAI LeMUR Triage Engine:** Parses the transcript to extract specific disaster hazards, categorizes emergency needs (Medical, Evacuation, Rescue, Shelter), and assigns a calculated **Urgency Score (1–10)**.
4.  **Volunteer Dispatch Dashboard:** Displays a prioritized, color-coded triage queue for coordinators to deploy teams instantly.

---

## 🛠️ Technology Stack & Partner Integrations

*   **[AssemblyAI](https://www.assemblyai.com/):** Powers the core interaction via the **Voice Agent API** (STT + LLM + TTS), and uses **LeMUR** for extracting structured JSON (Location, Category, Urgency) from transcripts.
*   **[FastAPI](https://fastapi.tiangolo.com/):** High-performance Python framework orchestrating secure token generation and LeMUR API calls.
*   **[native.builder](https://builder.nativelyai.com/):** Scaffolded the mobile-first victim UI, admin triage dashboard, database schema, and agent workflows.

---

## 🚀 How to Run the Backend Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/swatiicfai/AeroRescue-.git
   cd AeroRescue-
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your AssemblyAI API Key & Agent ID:**
   Create a Voice Agent in your AssemblyAI dashboard, note the Agent ID, and add it along with your API key to a `.env` file in the root directory:
   ```env
   ASSEMBLYAI_API_KEY=your_api_key_here
   ASSEMBLYAI_AGENT_ID=your_agent_id_here
   ```

4. **Run the FastAPI server:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Available Endpoints:**
   * `POST /voice-agent-token`: Generates a temporary auth token to connect your browser frontend directly to the AssemblyAI Voice Agent API over WebSockets.
   * `POST /analyze-distress-call`: Upload a `.wav` file to batch-transcribe and extract emergency triage data using LeMUR.

---

*Built with ❤️ for the AssemblyAI Voice Agent Hackathon.*

