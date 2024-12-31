# Job Buddy - Zero Model Version

Job Buddy is a platform designed to assist students and job seekers in preparing for interviews, finding job opportunities, and receiving AI mentorship. This repository contains the initial version of the project.

## Repository Contents

- **main.py**: The primary Python script for the application.
- **hi.py**: It's an testing site python file.
- **info.txt**: A text file containing relevant information or data used by the application.

## Prerequisites

Ensure you have the following installed on your system:

- Python 3.x
- Necessary Python packages (see below)

## Installation and Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/saiisback/Job-buddy.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd Job-buddy
   ```
The script uses the following Python modules:  


3. **Install dependencies**:

   **Built-in Modules**  
      1. **`re`**:  
         - For regular expressions to parse and extract structured data from the AI-generated response.  

   **Third-party Modules**  
      2. **`google.generativeai`**:  
         - To interact with Google's generative AI model (Gemini).  
         - Requires the `google-generativeai` library.  

      3. **`pyttsx3`**:  
         - For text-to-speech functionality to read out questions and feedback.  

      4. **`speech_recognition` (as `sr`)**:  
         - For converting user speech into text during the interview process.  

      ### Modules Installation  
      To use this script, you need to install the following third-party libraries using `pip`:  

      ```bash
      pip install google-generativeai pyttsx3 SpeechRecognition
      ```  

### Additional Notes  
      - Ensure your microphone and audio output devices are configured correctly for `speech_recognition` and `pyttsx3` to function seamlessly.  
      - The `google.generativeai` library requires an API key, which you must configure before running the script.  


   It's recommended to use a virtual environment to manage dependencies. If you're using `venv`, you can set it up as follows:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

4. **Run the application**:

   ```bash
   python main.py
   ```

## Usage

Provide detailed instructions on how to use the application. For example:

- How to navigate the user interface.
- How to input data or commands.
- Expected outcomes or results.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:

   ```bash
   git checkout -b feature-name
   ```

3. Make your changes and commit them:

   ```bash
   git commit -m "Description of changes"
   ```

4. Push to the branch:

   ```bash
   git push origin feature-name
   ```

5. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or issues, please reach out:

- **Author**: Sai Karthik Ketha
- **GitHub**: [saiisback](https://github.com/saiisback)
- **LinkedIn**: [Sai Karthik Ketha](https://www.linkedin.com/in/sai-karthik-ketha/)