# AI News Anchor

## Overview

**AI News Anchor** is an automated news channel application built using Python, Streamlit, and D-ID's API. The application asks for a script and generates a video featuring an AI-driven news anchor delivering the news. The AI anchor's speech is dynamically generated, making it a unique and engaging way to consume news.

## Features

- **Provide Script:** Provide the script to it and it reads out the news.
- **AI News Anchor:** Generates videos of an AI news anchor reading out the news.
- **Customizable:** Users can select the number of news items to be read and customize the news category.
- **Interactive UI:** A user-friendly interface powered by Streamlit.


### Installation

1. **Clone the Repository:**

2. **Create and Activate a Virtual Environment (optional but recommended):**

3. **Install the Required Packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables:**

    Create a `.env` file in the root directory of your project with the following content:

    ```plaintext
    BEARER_TOKEN=your_did_bearer_token_here
    ```

5. **Run the Application:**

    ```bash
    streamlit run app.py
    ```

    This command will start the application, and you can access it through your browser at `http://localhost:8501`.



## File Structure

- **`app.py`:** The main application file.
- **`news_video.py`:** Contains the `VideoGenerator` class for generating videos with the D-ID API.
- **`requirements.txt`:** Lists all the required Python packages.
- **`.env`:** Stores environment variables (not included in the repo for security reasons).

## Customization

- **Logo:** Update the `logo_url` in `app.py` to point to your logo image.
- **Anchor Image:** Update the `image_url` to change the anchor's image.
- **Voice:** Customize the AI anchor's voice by modifying the `voice_id` in the `VideoGenerator` class.


