import os
import time
import azure.cognitiveservices.speech as speechsdk
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # Load environment variables
    speech_key = os.getenv("AZURE_SPEECH_API_KEY")
    service_region = os.getenv("AZURE_SPEECH_REGION")
    tts_key = os.getenv("AZURE_TTS_API_KEY")
    tts_region = os.getenv("AZURE_TTS_REGION")
    
    if not all([speech_key, service_region, tts_key, tts_region]):
        logger.error("Missing required environment variables. Please check your environment variables.")
        return
    
    # Configure speech translation
    source_language = 'de-DE'
    target_language = 'fr'  # Change target language as needed
    
    translation_config = speechsdk.translation.SpeechTranslationConfig(
        subscription=speech_key,
        region=service_region,
        speech_recognition_language=source_language,
        target_languages=(target_language,)
    )
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    
    recognizer = speechsdk.translation.TranslationRecognizer(
        translation_config=translation_config,
        audio_config=audio_config
    )
    
    # Configure speech synthesizer with proper audio output
    tts_config = speechsdk.SpeechConfig(
        subscription=tts_key,
        region=tts_region
    )
    tts_config.speech_synthesis_voice_name = f"fr-FR-VivienneMultilingualNeural"  # Voice matching the target language
    # Explicitly configure speaker output
    audio_output_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    logger.info("Audio output configured to use default speaker")

    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=tts_config,
        audio_config=audio_output_config
    )

    # Track current session state
    done = False
    last_translated_text = ""
    pending_synthesis = False
    
    # Callback for successful synthesis
    def synthesis_completed_cb(evt):
        nonlocal pending_synthesis
        if evt.result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            pending_synthesis = False
            logger.info("Speech synthesis completed")
    
    # Callback for synthesis errors
    def synthesis_error_cb(evt):
        nonlocal pending_synthesis
        pending_synthesis = False
        logger.error(f"Speech synthesis error: {evt.result.error_details}")
    
    # Connect synthesis callbacks
    synthesizer.synthesis_completed.connect(synthesis_completed_cb)
    synthesizer.synthesis_canceled.connect(synthesis_error_cb)
    
    # Handle intermediate recognition (partial results)
    def recognizing_callback(evt):
        # We don't synthesize partial results to avoid audio interruptions
        if evt.result.text:
            logger.info(f"[Partial]: {evt.result.text}")
    
    # Handle final recognized text
    def recognized_callback(evt):
        nonlocal last_translated_text, pending_synthesis
        
        if evt.result.reason == speechsdk.ResultReason.TranslatedSpeech:
            translated = list(evt.result.translations.values())[0]
            logger.info(f"[Translated]: {translated}")
            
            # Only synthesize if not already synthesizing and text is different
            if not pending_synthesis and translated != last_translated_text:
                pending_synthesis = True
                last_translated_text = translated
                logger.info(f"Attempting to speak text: {translated}")
                # Use synchronous speak_text instead of async to ensure audio completes
                result = synthesizer.speak_text(translated)
                if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                    logger.info("Speech synthesis succeeded")
                else:
                    logger.error(f"Speech synthesis failed: {result.reason}")
                # Small delay to ensure audio completes playing
                time.sleep(0.2)
                pending_synthesis = False
       
        elif evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            text = evt.result.text
            logger.info(f"[Recognized]: {text}")

    # Handle session end or errors
    def stop_cb(evt):
        nonlocal done
        done = True
        if isinstance(evt, speechsdk.translation.TranslationRecognitionCanceledEventArgs):
            logger.error(f"Recognition canceled: {evt.error_details}")
    
    # Connect event handlers
    recognizer.recognizing.connect(recognizing_callback)
    recognizer.recognized.connect(recognized_callback)
    recognizer.session_stopped.connect(stop_cb)
    recognizer.canceled.connect(stop_cb)
    
    # Start continuous recognition
    logger.info("Starting speech recognition. Speak into your microphone...")
    recognizer.start_continuous_recognition()
    
    try:
        while not done:
            time.sleep(0.5)
    except KeyboardInterrupt:
        logger.info("Stopping due to keyboard interrupt")
    finally:
        # Clean up resources
        logger.info("Stopping recognition")
        recognizer.stop_continuous_recognition()

if __name__ == "__main__":
    main()
