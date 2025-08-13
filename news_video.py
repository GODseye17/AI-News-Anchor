import requests
import json
import time

class VideoGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.voice_id = "en-US-JennyNeural"  # Default voice
        
        # D-ID Presenter IDs (use these instead of URLs for D-ID avatars)
        self.presenters = {
            "amy-Aq6OmGZnMt": "Amy",
            "anna-R5OMsEJ3DK": "Anna", 
            "bella-lux-VbmPiYLq5M": "Bella",
            "fatha-rK5XHPPvRT": "Fatha",  # This is the Fatha presenter ID
            "josh-WNqtJIgqUp": "Josh",
            "matt-zcSXHQnCml": "Matt",
            "noelle-8Iy3QSlXV7": "Noelle"
        }

    def generate_video(self, input_text, source_url=None, voice_id=None, presenter_id=None):
        """
        Generate a video with the AI anchor reading the provided text.
        
        Args:
            input_text: The script for the AI anchor to read (can include SSML)
            source_url: URL of custom anchor image (use this OR presenter_id, not both)
            voice_id: Optional voice ID to override the default
            presenter_id: D-ID presenter ID for built-in avatars
        
        Returns:
            URL of the generated video or None if failed
        """
        url = "https://api.d-id.com/talks"
        
        # Use provided voice_id or default
        voice_to_use = voice_id if voice_id else self.voice_id
        
        # Detect if input contains SSML markup
        use_ssml = '<mstts:express-as' in input_text or '<speak' in input_text
        
        # Prepare the script payload
        if use_ssml:
            if not input_text.strip().startswith('<speak'):
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

        # Build payload based on whether using presenter or custom image
        if presenter_id and presenter_id in self.presenters:
            # Using D-ID presenter
            payload = {
                "script": script_payload,
                "presenter_id": presenter_id,
                "config": {
                    "fluent": "false",
                    "pad_audio": "0.0"
                }
            }
            print(f"Using D-ID Presenter: {self.presenters[presenter_id]} (ID: {presenter_id})")
        elif source_url:
            # Using custom image URL
            payload = {
                "script": script_payload,
                "source_url": source_url,
                "config": {
                    "fluent": "false",
                    "pad_audio": "0.0"
                }
            }
            print(f"Using custom image: {source_url}")
        else:
            print("Error: Must provide either source_url or presenter_id")
            return None

        # Determine auth format
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
            
            if response.status_code not in [201, 200]:
                print(f"Error Response: {response.text}")
                if "presenter_id" in response.text and "not found" in response.text:
                    print("\n⚠️  Presenter not found. Your account may not have access to this presenter.")
                    print("   Try using a custom image URL instead.")
                
            response.raise_for_status()
            _response = response.json()
            print("Initial Response: ", _response)

            if 'id' not in _response:
                print("Error: No ID in initial response:", _response)
                return None

            talk_id = _response['id']
            talk_url = f"{url}/{talk_id}"
            
            headers_polling = {
                "accept": "application/json",
                "authorization": auth_header
            }

            # Poll for video completion
            max_attempts = 30
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
                time.sleep(10)

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

    def list_available_presenters(self):
        """List all available D-ID presenters for your account"""
        
        url = "https://api.d-id.com/presenters"
        
        if ':' in self.api_key:
            auth_header = f"Basic {self.api_key}"
        else:
            auth_header = f"Bearer {self.api_key}"
            
        headers = {
            "accept": "application/json",
            "authorization": auth_header
        }
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                presenters = response.json()
                print("\nAvailable D-ID Presenters:")
                print("-" * 40)
                for p in presenters.get('presenters', []):
                    print(f"ID: {p.get('id')}")
                    print(f"Name: {p.get('name', 'N/A')}")
                    print(f"Gender: {p.get('gender', 'N/A')}")
                    print("-" * 40)
                return presenters
            else:
                print(f"Failed to get presenters: {response.status_code}")
                print(response.text)
                return None
        except Exception as e:
            print(f"Error listing presenters: {e}")
            return None