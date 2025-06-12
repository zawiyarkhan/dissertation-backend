from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
import shutil, os, json, wave, ssl
from vosk import Model, KaldiRecognizer
import librosa
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import FreqDist
from pydub import AudioSegment

TEMP_DIR = "temp_uploads"
AUDIO_PATH = "converted.wav"
VOSK_MODEL_PATH = "/Users/zawiyarkhan/dev/disertation/alzehimer backend/backend/app/core/model"

os.makedirs(TEMP_DIR, exist_ok=True)

# -------------------------------
# 🔹 Save uploaded file
# -------------------------------
def save_uploaded_file(uploaded_file: UploadFile, path: str):
    with open(path, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)

# -------------------------------
# 🔹 Convert to WAV
# -------------------------------
def convert_to_wav(input_path: str, output_path: str):
    audio = AudioSegment.from_file(input_path, format="m4a")
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")

# -------------------------------
# 🔹 Extract prosodic features
# -------------------------------
def extract_voice_features(wav_path: str):
    y, sr = librosa.load(wav_path)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

    pitch_values = [pitches[magnitudes[:, i].argmax(), i] 
                    for i in range(pitches.shape[1]) 
                    if pitches[magnitudes[:, i].argmax(), i] > 0]
    pitch_values = np.array(pitch_values)
    mean_pitch = np.mean(pitch_values)

    jitter_local = (np.mean(np.abs(np.diff(pitch_values) / pitch_values[:-1]))
                    if len(pitch_values) > 1 else None)

    rms = librosa.feature.rms(y=y)[0]
    shimmer_local = (np.mean(np.abs(np.diff(rms)) / rms[:-1])
                     if len(rms) > 1 else None)

    intervals = librosa.effects.split(y, top_db=20)
    speech_duration = sum([(end - start) / sr for start, end in intervals])
    total_duration = len(y) / sr
    speech_ratio = speech_duration / total_duration

    return {
        "mean_pitch": mean_pitch,
        "jitter": jitter_local,
        "shimmer": shimmer_local,
        "speech_duration": speech_duration,
        "speech_ratio": speech_ratio
    }

# -------------------------------
# 🔹 Transcribe using VOSK
# -------------------------------
def transcribe_with_vosk(wav_path: str, model_path: str):
    if not os.path.exists(model_path):
        raise RuntimeError("VOSK model not found.")

    wf = wave.open(wav_path, "rb")
    model = Model(model_path)
    rec = KaldiRecognizer(model, wf.getframerate())

    transcript_parts = []
    while True:
        data = wf.readframes(8000)
        if not data:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            transcript_parts.append(result.get("text", ""))
    final_result = json.loads(rec.FinalResult())
    transcript_parts.append(final_result.get("text", ""))
    return " ".join(transcript_parts)

# -------------------------------
# 🔹 Analyze text linguistically
# -------------------------------
def analyze_transcript_nlp(text: str):
    try:
        _create_unverified_https_context = ssl._create_unverified_context
        ssl._create_default_https_context = _create_unverified_https_context
    except AttributeError:
        pass
    # nltk.download('punkt')

    words = word_tokenize(text)
    sentences = sent_tokenize(text)
    avg_sentence_len = np.mean([len(word_tokenize(s)) for s in sentences]) if sentences else 0
    vocab_richness = len(set(words)) / len(words) if words else 0
    word_freq = FreqDist(words).most_common(10)
    return {
        "avg_sentence_length": avg_sentence_len,
        "vocab_richness": vocab_richness,
        "top_words": word_freq
    }

# -------------------------------
# 🔹 FastAPI Handler
# -------------------------------
def upload_voice(file: UploadFile = File(...)):
    # if not file.content_type.startswith("audio/"):
    #     return JSONResponse(content={"error": "File is not an audio type."}, status_code=400)

    temp_path = os.path.join(TEMP_DIR, file.filename)
    try:
        save_uploaded_file(file, temp_path)
        convert_to_wav(temp_path, AUDIO_PATH)
        voice_features = extract_voice_features(AUDIO_PATH)
        transcript = transcribe_with_vosk(AUDIO_PATH, VOSK_MODEL_PATH)
        nlp_stats = analyze_transcript_nlp(transcript)

        # Clean up
        os.remove(temp_path)
        os.remove(AUDIO_PATH)

        return {
            "message": "Voice note processed successfully",
            "filename": file.filename,
            "voice_features": voice_features,
            "transcript": transcript,
            "nlp_analysis": nlp_stats
        }
    except Exception as e:
        if os.path.exists(temp_path): os.remove(temp_path)
        if os.path.exists(AUDIO_PATH): os.remove(AUDIO_PATH)
        return JSONResponse(content={"error": str(e)}, status_code=500)
