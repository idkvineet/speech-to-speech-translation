# 🎤 Speech-to-Speech Translator

## Overview
A powerful, user-friendly desktop application that provides real-time speech translation with audio output. Record your voice in any supported language and instantly receive both text and audio translations in multiple target languages simultaneously.

## ✨ Key Features

### 🗣️ Multi-Language Support
- **17 Languages Available**: English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, Chinese, Arabic, Hindi, Turkish, Swedish, Dutch, Polish, and Greek
- **Flexible Source Language**: Speak in any of the supported languages
- **Customizable Target Languages**: Choose which languages you want translations in

### 🎯 Core Functionality
- **Real-Time Speech Recognition**: Advanced voice recognition converts your speech to text instantly
- **Simultaneous Translation**: Translates to multiple languages at once
- **Text-to-Speech Output**: Each translation can be played as audio with natural-sounding voices
- **Visual Text Display**: See both your original speech and all translations on screen

### 🎨 Modern Interface
- **Clean, Professional Design**: Intuitive white interface with organized card layout
- **Resizable Window**: Adjust window size to your preference (minimum 800x650)
- **Responsive Grid Layout**: Automatically adjusts translation cards based on window size
- **Visual Waveform Display**: Audio visualization for better user feedback
- **Scrollable Translations**: Support for displaying any number of target languages

### ⚙️ Customization Options
- **Language Selector**: Easy-to-use popup window for selecting target languages
- **Default Languages**: Quick setup with pre-selected common languages
- **Individual Playback Controls**: Play any translation independently
- **Clear All Function**: Reset everything with one click

## 🚀 How It Works

1. **Select Source Language**: Choose the language you'll be speaking
2. **Choose Target Languages**: 
   - Click "Select Languages" to customize your target languages
   - Or click "Use Defaults" for Spanish, French, German, Italian, Japanese, and Chinese
3. **Record**: Click "🎤 Start Recording" and speak clearly (up to 10 seconds)
4. **View Results**: Your speech is displayed as text along with all translations
5. **Listen**: Click "▶ Play" on any translation card to hear it spoken

## 📋 Technical Requirements

### Required Python Libraries
```bash
pip install SpeechRecognition
pip install googletrans==4.0.0-rc1
pip install gTTS
pip install pygame
pip install pyaudio
```

### System Requirements
- Python 3.7 or higher
- Working microphone
- Internet connection (for translation and text-to-speech services)
- Windows, macOS, or Linux

## 🎓 Use Cases

### Education
- **Language Learning**: Practice pronunciation and hear correct translations
- **Classroom Tool**: Teachers can demonstrate multiple languages instantly
- **Study Aid**: Compare translations across different languages

### Business
- **International Meetings**: Quick translation for multilingual teams
- **Customer Service**: Communicate with customers in their native language
- **Travel Preparation**: Practice phrases before international trips

### Personal
- **Family Communication**: Bridge language gaps with family members
- **Travel Companion**: Real-time translation while traveling
- **Cultural Exploration**: Learn how phrases translate across cultures

## 🌟 Advantages

### Speed & Efficiency
- Translates to multiple languages simultaneously (not one at a time)
- No need to manually switch between languages
- Instant playback of translations

### Accuracy
- Uses Google's speech recognition technology
- Professional translation engine
- Natural-sounding text-to-speech voices

### Flexibility
- Choose exactly which languages you need
- Switch source language on the fly
- Save time by translating to multiple targets at once

### User-Friendly
- No complex setup or configuration
- Clear visual feedback at every step
- Intuitive controls and layout

## 🔧 Features in Detail

### Speech Recognition
- Automatic noise adjustment for better accuracy
- 5-second listening timeout to prevent long waits
- 10-second phrase limit for optimal processing
- Support for various accents and dialects

### Translation Engine
- Powered by Google Translate API
- High-quality translations
- Contextual understanding
- Support for 17 major world languages

### Text-to-Speech
- Natural-sounding voices via Google TTS
- Language-appropriate pronunciation
- Automatic temporary file management
- Smooth playback with pygame

### Status Indicators
- 🔴 Red: Recording in progress
- ⚙️ Blue: Processing/translating
- ✓ Green: Successfully completed
- ⚠️ Orange/Red: Warnings and errors

## 💡 Tips for Best Results

1. **Speak Clearly**: Enunciate words clearly for better recognition
2. **Quiet Environment**: Minimize background noise
3. **Good Microphone**: Use a quality microphone for best results
4. **Reasonable Pace**: Don't speak too fast or too slow
5. **Internet Connection**: Ensure stable internet for translation services

## 🎯 Perfect For

- Language students and teachers
- International business professionals
- Travelers and tourists
- Content creators and translators
- Anyone learning or working with multiple languages

## 🔒 Privacy & Security

- All processing uses secure Google services
- Audio is temporarily stored only during playback
- No permanent storage of your recordings
- Files are automatically deleted after use

## 📱 Future Enhancement Ideas

- Offline translation support
- Save translation history
- Export translations to file
- Custom voice settings
- Batch file translation
- Integration with other apps

---

Built with Python, Tkinter, Google Services
