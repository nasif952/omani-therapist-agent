# Omani Therapist Agent

A speech-to-text system designed for Omani Arabic dialect using Google Cloud Speech-to-Text API and Azure Cognitive Services.

## Setup Instructions

### Prerequisites

1. Python 3.7 or higher
2. **Google Cloud Setup:**
   - Google Cloud account with Speech-to-Text API enabled
   - Google Cloud service account with appropriate permissions
3. **Azure Setup (Optional):**
   - Azure account with Cognitive Services
   - Speech Services resource created

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/nasif952/omani-therapist-agent.git
   cd omani-therapist-agent
   ```

2. Install required dependencies:
   ```bash
   # For Google Cloud
   pip install speech_recognition google-cloud-speech pyaudio
   
   # For Azure (optional)
   pip install azure-cognitiveservices-speech
   ```

3. Set up credentials:
   
   **Google Cloud:**
   - Download your Google Cloud service account JSON credentials file
   - Place it in the `speech2texttest/google/` directory
   - Update the filename in `testgoogle.ipynb` if different from the default
   
   **Azure (Optional):**
   - Copy `speech2texttest/azure/credentials_template.md` to `speech2texttest/azure/credentials.md`
   - Fill in your Azure Speech Services keys and endpoint
   - The credentials.md file is automatically excluded from version control

### Usage

**Google Cloud Speech-to-Text:**
1. Open the Jupyter notebook:
   ```bash
   jupyter notebook speech2texttest/google/testgoogle.ipynb
   ```
2. Run the cells to test speech-to-text with Omani Arabic (`ar-OM`)

**Azure Cognitive Services (when available):**
1. Navigate to the Azure notebooks in `speech2texttest/azure/`
2. Choose from the available notebooks:
   - `testazureaudio.ipynb` - Audio file transcription
   - `testazuremic.ipynb` - Microphone input transcription  
   - `testazure_realtime_continuous recoginition.ipynb` - Real-time continuous recognition

### Features

- Real-time speech recognition for Omani Arabic dialect
- Ambient noise calibration
- **Google Cloud Speech-to-Text integration**
- **Azure Cognitive Services Speech integration** (planned)
- Error handling for authentication and recognition issues
- Secure credentials management

### Security Note

- **Never commit credentials to version control**
- Google Cloud JSON credentials are excluded in `.gitignore`
- Azure credentials.md file is excluded in `.gitignore`
- Keep your service account credentials secure and rotate them regularly
- Use credential templates provided for secure setup

### Project Structure

```
omani-therapist-agent/
├── speech2texttest/
│   ├── google/
│   │   ├── testgoogle.ipynb          # Google Cloud testing notebook
│   │   └── [your-credentials].json   # Google Cloud credentials (not tracked)
│   └── azure/
│       ├── credentials_template.md   # Template for Azure credentials
│       ├── credentials.md            # Your Azure credentials (not tracked)
│       ├── testazureaudio.ipynb      # Azure audio file transcription
│       ├── testazuremic.ipynb        # Azure microphone transcription
│       └── testazure_realtime_continuous recoginition.ipynb # Real-time recognition
├── .gitignore                        # Excludes credentials and sensitive files
└── README.md                         # This file
```

### Troubleshooting

1. **FileNotFoundError**: Ensure your credentials JSON file is in the correct directory
2. **DefaultCredentialsError**: Verify you're using `credentials_json_path` parameter
3. **ValueError for language**: Use `language_code="ar-OM"` instead of `language="ar-OM"`
4. **Audio issues**: Check microphone permissions and PyAudio installation

### Contributing

Feel free to contribute by:
- Adding support for other Arabic dialects
- Improving speech recognition accuracy
- Adding Azure Cognitive Services integration
- Enhancing error handling and user experience

### License

This project is intended for educational and research purposes. 