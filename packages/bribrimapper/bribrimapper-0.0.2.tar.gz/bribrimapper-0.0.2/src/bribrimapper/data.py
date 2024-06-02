"""
This module contains the tonal and IPA transcription maps for Bribrí.

The tonal_transcription_map dictionary maps tonal transcriptions to their corresponding numerical representation.
The ipa_transcription_map dictionary maps tonal transcriptions to their corresponding IPA representation.
"""

tonal_transcription_map = {
    'éq': 'ë4',
    'óq': 'ö4',
    'áx': 'ã4',
    'óx': 'õ4',
    'à': 'a1',
    'a\'': 'a2',
    'ã\'': 'ã2',
    'â': 'a3',
    'á': 'a4',
    'è': 'e1',
    'e\'': 'e2',
    'ẽ\'': 'ẽ2',
    'ê': 'e3',
    'é': 'e4',
    'ì': 'i1',
    'i\'': 'i2',
    'ĩ\'': 'ĩ2',
    'î': 'i3',
    'í': 'i4',
    'ò': 'o1',
    'o\'': 'o2',
    'õ\'': 'õ2',
    'ô': 'o3',
    'ó': 'o4',
    'ù': 'u1',
    'u\'': 'u2',
    'ũ\'': 'ũ2',
    'û': 'u3',
    'ú': 'u4'
}

ipa_transcription_map = {
    'éq': 'ë˥˧',  # 'ë4' -> 'ë˩'
    'óq': 'ö˥˧',  # 'ö4' -> 'ö˩'
    'áx': 'ã˥˧',  # 'ã4' -> 'ã˩'
    'óx': 'õ˥˧',  # 'õ4' -> 'õ˩'
    'à': 'a˥',   # 'a1' -> 'a˧'
    'a\'': 'a˩˧',  # 'a2' -> 'a˥'
    'ã\'': 'ã˩˧',  # 'ã2' -> 'ã˥'
    'â': 'a˨˩˦', # 'a3' -> 'a˨˩˦'
    'á': 'a˥˧',   # 'a4' -> 'a˩'
    'è': 'e˧',   # 'e1' -> 'e˧'
    'e\'': 'e˩˧',  # 'e2' -> 'e˥'
    'ẽ\'': 'ẽ˩˧',  # 'ẽ2' -> 'ẽ˥'
    'ê': 'e˨˩˦', # 'e3' -> 'e˨˩˦'
    'é': 'e˥˧',   # 'e4' -> 'e˩'
    'ì': 'i˥',   # 'i1' -> 'i˧'
    'i\'': 'i˩˧',  # 'i2' -> 'i˥'
    'ĩ\'': 'ĩ˩˧',  # 'ĩ2' -> 'ĩ˥'
    'î': 'i˨˩˦', # 'i3' -> 'i˨˩˦'
    'í': 'i˥˧',   # 'i4' -> 'i˩'
    'ò': 'o˥',   # 'o1' -> 'o˧'
    'o\'': 'o˩˧',  # 'o2' -> 'o˥'
    'õ\'': 'õ˩˧',  # 'õ2' -> 'õ˥'
    'ô': 'o˨˩˦', # 'o3' -> 'o˨˩˦'
    'ó': 'o˥˧',   # 'o4' -> 'o˩'
    'ù': 'u˥',   # 'u1' -> 'u˧'
    'u\'': 'u˩˧',  # 'u2' -> 'u˥'
    'ũ\'': 'ũ˩˧',  # 'ũ2' -> 'ũ˥'
    'û': 'u˨˩˦', # 'u3' -> 'u˨˩˦'
    'ú': 'u˥˧'    # 'u4' -> 'u˩'
}