from bribrimapper.data import tonal_transcription_map, ipa_transcription_map

def transcribe_bribri_tones(text):
    for key, value in tonal_transcription_map.items():
        text = text.replace(key, value)
    return text

def bribri_to_ipa(text):
    for key, value in ipa_transcription_map.items():
        text = text.replace(key, value)
    return text