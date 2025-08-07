import requests
import json
import time

class VideoGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.voice_id = "en-US-JennyNeural"  # Default voice

    def generate_video(self, input_text, source_url, voice_id=None):
        """
        Generate a video with the AI anchor reading the provided text.
        
        Args:
            input_text: The script for the AI anchor to read
            source_url: URL of the anchor image
            voice_id: Optional voice ID to override the default
        
        Returns:
            URL of the generated video or None if failed
        """
        url = "https://api.d-id.com/talks"
        
        # Use provided voice_id or default
        voice_to_use = voice_id if voice_id else self.voice_id

        payload = {
            "script": {
                "type": "text",
                "subtitles": "false",
                "provider": {
                    "type": "microsoft",
                    "voice_id": voice_to_use
                },
                "ssml": "false",
                "input": input_text
            },
            "config": {
                "fluent": "false",
                "pad_audio": "0.0"
            },
            "source_url": source_url
        }

        # Determine auth format based on API key structure
        # New D-ID keys use "email:token" format with Basic auth
        # Old keys use JWT format with Bearer auth
        if ':' in self.api_key:
            auth_header = f"Basic {self.api_key}"
            print("Using Basic authentication")
        else:
            auth_header = f"Bearer {self.api_key}"
            print("Using Bearer authentication")
            
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": auth_header
        }

        try:
            # Initial request to generate video
            print("Initiating video generation...")
            print(f"API Endpoint: {url}")
            print(f"Using voice: {voice_to_use}")
            print(f"Text length: {len(input_text)} characters")
            
            response = requests.post(url, json=payload, headers=headers)
            print(f"Response Status Code: {response.status_code}")
            
            if response.status_code != 201 and response.status_code != 200:
                print(f"Error Response: {response.text}")
                
            response.raise_for_status()  # Raise an exception for bad status codes
            _response = response.json()
            print("Initial Response: ", _response)

            if 'id' not in _response:
                print("Error: No ID in initial response:", _response)
                return None

            talk_id = _response['id']
            talk_url = f"{url}/{talk_id}"
            
            # Use same auth format for polling
            headers_polling = {
                "accept": "application/json",
                "authorization": auth_header
            }

            # Poll for video completion
            max_attempts = 30  # Maximum polling attempts
            attempt = 0
            
            while attempt < max_attempts:
                print(f"Checking video status... (Attempt {attempt + 1}/{max_attempts})")
                
                response = requests.get(talk_url, headers=headers_polling)
                response.raise_for_status()
                video_response = response.json()

                if 'status' not in video_response:
                    print("Error: No status in video response:", video_response)
                    return None

                status = video_response["status"]
                print(f"Current status: {status}")

                if status == "done":
                    print("Video generation completed!")
                    return video_response.get("result_url")
                elif status == "error" or status == "rejected":
                    print(f"Video generation failed with status: {status}")
                    if 'error' in video_response:
                        print(f"Error details: {video_response['error']}")
                    return None
                
                attempt += 1
                time.sleep(10)  # Wait 10 seconds before next poll

            print("Video generation timed out")
            return None

        except requests.exceptions.RequestException as e:
            print(f"Request error occurred: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None