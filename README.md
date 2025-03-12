# Real-time Speech-to-Speech Translation

This project uses Azure Cognitive Services to provide real-time speech-to-speech translation capabilities. It captures audio from your microphone, translates it to your target language, and speaks the translated text through your speakers.

## Features

- Real-time speech recognition
- Translation between multiple languages
- Text-to-speech output of translated content
- Configurable source and target languages

## Prerequisites

- Python 3.8 or higher
- An Azure account with access to:
  - Speech Service
- A microphone for speech input
- Speakers for audio output

## Getting Started

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd speech_to_speech_translation
```

### 2. Set Up a Virtual Environment

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

1. Copy the template environment file
   ```bash
   cp .env.template .env
   ```

2. Edit the `.env` file and add your Azure keys and regions:
   ```
   AZURE_SPEECH_API_KEY=your_speech_api_key
   AZURE_SPEECH_REGION=your_speech_region
   AZURE_TTS_API_KEY=your_tts_api_key
   AZURE_TTS_REGION=your_tts_region
   ```

### 5. Run the Application

```bash
python realtime_speech_to_speech_translation.py
```

## Usage

1. After starting the application, speak clearly into your microphone.
2. The application will recognize your speech, translate it to the target language (French by default), and play the translated speech through your speakers.
3. Press `Ctrl+C` to stop the application.

## Customizing Languages

To change the source or target language, modify the following variables in `realtime_speech_to_speech_translation.py`:

```python
# Configure speech translation
source_language = 'de-DE'  # Change to your preferred source language
target_language = 'fr'     # Change to your preferred target language

# TTS voice
tts_config.speech_synthesis_voice_name = "fr-FR-VivienneMultilingualNeural"  # Change to match your target language
```

## Supported Languages

For a complete list of supported languages for speech recognition, translation, and synthesis, refer to the [Azure Cognitive Services documentation](https://learn.microsoft.com/en-gb/azure/ai-services/speech-service/language-support?tabs=tts).