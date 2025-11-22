import requests
import json
from config import API_BASE_URL

class DjangoAPIClient:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/api/auth"
        self.token = None
    
    def set_token(self, token):
        self.token = token
    
    def get_headers(self):
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Token {self.token}"
        return headers
    
    def register(self, full_name, username, email, password, date_of_birth, gender):
        try:
            print("=" * 50)  
            print(f"📝 REGISTRATION - Username: {username}, Email: {email}") 
            print("=" * 50) 
            
            response = requests.post(
                f"{self.base_url}/register/",
                headers={"Content-Type": "application/json"},
                json={
                    "full_name": full_name,
                    "username": username,
                    "email": email,
                    "password": password,
                    "date_of_birth": date_of_birth,
                    "gender": gender
                },
                timeout=30
            )
            
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text}")
            
            if response.status_code == 400:
                try:
                    error_data = response.json()
                    print(f"❌ Validation errors: {error_data}") 
                    return {"error": self._format_error(error_data)}
                except:
                    return {"error": f"Bad Request: {response.text}"}
            
            response.raise_for_status()
            result = response.json()
            
            if "requires_otp" in result and result["requires_otp"]:
                print(f"✅ Registration successful! OTP sent to {email}") 
            
            return result
            
        except requests.exceptions.ConnectionError as e:
            print(f"❌ Connection error: {e}") 
            return {"error": "Cannot connect to server. Make sure Django is running."}
        except requests.exceptions.Timeout:
            print("❌ Request timeout")  
            return {"error": "Request timeout. Server is not responding."}
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")  
            return {"error": str(e)}
        
    def get_analysis_results(self, upload_id):
        try:
            print("=" * 50)
            print(f"📊 FETCHING ANALYSIS RESULTS - Upload ID: {upload_id}")
            print("=" * 50)
            response = requests.get(
                f"{self.base_url}/uploads/{upload_id}/",
                headers=self.get_headers(),
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ Analysis results loaded successfully!")
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching analysis: {e}")
            return {"error": str(e)}
    
    def _format_error(self, error_data):
        if isinstance(error_data, dict):
            errors = []
            for field, messages in error_data.items():
                if isinstance(messages, list):
                    errors.append(f"{field}: {', '.join(messages)}")
                else:
                    errors.append(f"{field}: {messages}")
            return '\n'.join(errors)
        return str(error_data)
    
    def login(self, username, password):
        try:
            print("=" * 50)  
            print(f"🔐 LOGIN ATTEMPT - Username: {username}")  
            print("=" * 50)  
            
            response = requests.post(
                f"{self.base_url}/login/",
                headers={"Content-Type": "application/json"},
                json={"username": username, "password": password},
                timeout=30
            )
            
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text}")
            
            if response.status_code == 400:
                try:
                    error_data = response.json()
                    print(f"❌ Login failed: {error_data}")  
                    return {"error": self._format_error(error_data)}
                except:
                    return {"error": f"Bad Request: {response.text}"}
            
            response.raise_for_status()
            result = response.json()
            
            if "requires_otp" in result and result["requires_otp"]:
                print(f"✅ OTP sent to {result.get('email', 'your email')}")  
            
            return result
            
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to server")  
            return {"error": "Cannot connect to server. Make sure Django is running."}
        except requests.exceptions.Timeout:
            print("❌ Request timeout")  
            return {"error": "Request timeout. Server is not responding."}
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")  
            return {"error": str(e)}
    
    def verify_otp(self, email, otp):
        try:
            print("=" * 50)  
            print(f"🔢 OTP VERIFICATION - Email: {email}, OTP: {otp}") 
            print("=" * 50)  
            
            response = requests.post(
                f"{self.base_url}/verify-otp/",
                headers={"Content-Type": "application/json"},
                json={"email": email, "otp": otp},
                timeout=30
            )
            
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 400:
                try:
                    error_data = response.json()
                    print(f"❌ OTP verification failed: {error_data}") 
                    return {"error": self._format_error(error_data)}
                except:
                    return {"error": f"Bad Request: {response.text}"}
            
            response.raise_for_status()
            data = response.json()
            
            if "token" in data:
                self.set_token(data["token"])
                print(f"✅ OTP VERIFIED! User logged in: {data.get('username', 'User')}") 
            
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")  
            return {"error": str(e)}
    
    def resend_otp(self, email):
        try:
            print("=" * 50)
            print(f"🔄 RESEND OTP - Email: {email}")
            print("=" * 50)
            
            response = requests.post(
                f"{self.base_url}/resend-otp/",
                headers={"Content-Type": "application/json"},
                json={"email": email},
                timeout=30
            )
            
            if response.status_code == 400:
                try:
                    error_data = response.json()
                    print(f"❌ Resend OTP failed: {error_data}")
                    return {"error": self._format_error(error_data)}
                except:
                    return {"error": f"Bad Request: {response.text}"}
            
            response.raise_for_status()
            result = response.json()
            print(f"✅ New OTP sent to {email}")
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error: {e}")
            return {"error": str(e)}
    
    def google_login(self, google_token):
        try:
            print("=" * 50)
            print(f"🔑 GOOGLE LOGIN ATTEMPT")
            print("=" * 50)
            
            response = requests.post(
                f"{self.base_url}/google/",
                headers={"Content-Type": "application/json"},
                json={"token": google_token},
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            if "token" in data:
                self.set_token(data["token"])
                print(f"✅ Google login successful: {data.get('username', 'User')}")
            
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Google login error: {e}")
            return {"error": str(e)}
    
    def upload_file(self, file_path):
        try:
            print("=" * 50)
            print(f"📤 UPLOADING FILE: {file_path}")
            print("=" * 50)
            
            with open(file_path, 'rb') as f:
                files = {'file': f}
                headers = {"Authorization": f"Token {self.token}"} if self.token else {}
                response = requests.post(
                    f"{self.base_url}/upload/",
                    files=files,
                    headers=headers,
                    timeout=60
                )
                response.raise_for_status()
                result = response.json()
                
                print(f"✅ Upload successful! Upload ID: {result.get('upload_id', 'N/A')}")
                return result
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Upload error: {str(e)}")
            return {"error": str(e)}
    
    def get_upload_history(self):
        try:
            response = requests.get(
                    f"{self.base_url}/uploads/history/",
                headers=self.get_headers(),
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def download_pdf_report(self, upload_id, save_path):
        try:
            print("=" * 50)
            print(f"📥 DOWNLOADING PDF - Upload ID: {upload_id}")
            print("=" * 50)
            
            response = requests.get(
                f"{self.base_url}/reports/download/{upload_id}/",
                headers=self.get_headers(),
                stream=True,
                timeout=60
            )
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ PDF saved to: {save_path}")
            return {"success": True}
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Download error: {str(e)}")
            return {"error": str(e)}
    
    def get_profile(self):
        try:
            response = requests.get(
                f"{self.base_url}/profile/",
                headers=self.get_headers(),
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def update_profile(self, profile_data):
        try:
            response = requests.put(
                f"{self.base_url}/profile/update/",
                json=profile_data,
                headers=self.get_headers(),
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def delete_account(self):
        try:
            print("=" * 50)
            print(f"🗑️  DELETING ACCOUNT")
            print("=" * 50)
            
            response = requests.delete(
                f"{self.base_url}/profile/delete/",
                headers=self.get_headers(),
                timeout=30
            )
            response.raise_for_status()
            
            print("✅ Account deleted successfully")
            return {"success": True}
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Delete account error: {e}")
            return {"error": str(e)}
    
    def change_password(self, current_password, new_password):
        try:
            print("=" * 50)
            print(f"🔐 CHANGING PASSWORD")
            print("=" * 50)
            
            response = requests.post(
                f"{self.base_url}/change-password/",
                headers=self.get_headers(),
                json={
                    "current_password": current_password,
                    "new_password": new_password
                },
                timeout=30
            )
            
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 400:
                try:
                    error_data = response.json()
                    print(f"❌ Password change failed: {error_data}")
                    return {"error": self._format_error(error_data)}
                except:
                    return {"error": f"Bad Request: {response.text}"}
            
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ Password changed successfully!")
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Change password error: {e}")
            return {"error": str(e)}
    
    def get_upload_detail(self, upload_id):
        try:
            print(f"🔍 Fetching upload detail: {upload_id}")
            response = requests.get(
                f"{self.base_url}/uploads/{upload_id}/",
                headers=self.get_headers(),
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching upload detail: {e}")
            return {"error": str(e)}
    
    def delete_upload(self, upload_id):
        try:
            print("=" * 50)
            print(f"🗑️  DELETING UPLOAD: {upload_id}")
            print("=" * 50)
            
            response = requests.delete(
                f"{self.base_url}/uploads/{upload_id}/delete/",
                headers=self.get_headers(),
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ Upload deleted: {result.get('message', 'Success')}")
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Delete upload error: {e}")
            return {"error": str(e)}

api_client = DjangoAPIClient()