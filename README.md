# Omani Therapist Agent

A speech-to-text system designed for Omani Arabic dialect using Google Cloud Speech-to-Text API.

## Setup Instructions

### Prerequisites

1. Python 3.7 or higher
2. Google Cloud account with Speech-to-Text API enabled
3. Google Cloud service account with appropriate permissions

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/nasif952/omani-therapist-agent.git
   cd omani-therapist-agent
   ```

2. Install required dependencies:
   ```bash
   pip install speech_recognition google-cloud-speech pyaudio
   ```

3. Set up Google Cloud credentials:
   - Download your Google Cloud service account JSON credentials file
   - Place it in the `speech2texttest/google/` directory
   - Update the filename in `testgoogle.ipynb` if different from the default

### Usage

1. Open the Jupyter notebook:
   ```bash
   jupyter notebook speech2texttest/google/testgoogle.ipynb
   ```

2. Run the cells to test speech-to-text with Omani Arabic (`ar-OM`)

### Features

- Real-time speech recognition for Omani Arabic dialect
- Ambient noise calibration
- Google Cloud Speech-to-Text integration
- Error handling for authentication and recognition issues

### Security Note

- **Never commit your Google Cloud credentials JSON file to version control**
- The credentials file is included in `.gitignore` for security
- Keep your service account credentials secure and rotate them regularly

### Project Structure

```
omani-therapist-agent/
├── speech2texttest/
│   ├── google/
│   │   ├── testgoogle.ipynb          # Main testing notebook
│   │   └── [your-credentials].json   # Google Cloud credentials (not tracked)
│   └── azure/                        # Future Azure integration
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