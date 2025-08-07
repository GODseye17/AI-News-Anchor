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
            input_text: The script for the AI anchor to read (can include SSML)
            source_url: URL of the anchor image
            voice_id: Optional voice ID to override the default
        
        Returns:
            URL of the generated video or None if failed
        """
        url = "https://api.d-id.com/talks"
        
        # Use provided voice_id or default
        voice_to_use = voice_id if voice_id else self.voice_id
        
        # Detect if input contains SSML markup
        use_ssml = '<mstts:express-as' in input_text or '<speak' in input_text
        
        # Prepare the script payload based on whether SSML is used
        if use_ssml:
            # For SSML, we need to wrap it properly
            if not input_text.strip().startswith('<speak'):
                # Wrap with proper SSML speak tags
                ssml_script = f'''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" 
                                  xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
                                  <voice name="{voice_to_use}">
                                      {input_text}
                                  </voice>
                              </speak>'''
            else:
                ssml_script = input_text
                
            script_payload = {
                "type": "text",
                "subtitles": "false",
                "provider": {
                    "type": "microsoft",
                    "voice_id": voice_to_use
                },
                "ssml": "true",
                "input": ssml_script
            }
        else:
            # Regular text-to-speech without SSML
            script_payload = {
                "type": "text",
                "subtitles": "false", 
                "provider": {
                    "type": "microsoft",
                    "voice_id": voice_to_use
                },
                "ssml": "false",
                "input": input_text
            }

        payload = {
            "script": script_payload,
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
            print(f"SSML enabled: {use_ssml}")
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

    def get_supported_voices(self):
        """
        Get list of supported voices from D-ID API
        """
        try:
            url = "https://api.d-id.com/tts/voices"
            
            if ':' in self.api_key:
                auth_header = f"Basic {self.api_key}"
            else:
                auth_header = f"Bearer {self.api_key}"
                
            headers = {
                "accept": "application/json",
                "authorization": auth_header
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"Error getting supported voices: {e}")
            return None
            
    def test_voice(self, voice_id, test_text="Hello, this is a test.", style=None):
        """
        Test a specific voice with sample text
        """
        print(f"Testing voice: {voice_id}")
        
        if style:
            test_script = f'<mstts:express-as style="{style}">{test_text}</mstts:express-as>'
        else:
            test_script = test_text
            
        # Use a test image
        test_image = "https://i.ibb.co/hYcxXTW/anchor.png"
        
        return self.generate_video(test_script, test_image, voice_id)