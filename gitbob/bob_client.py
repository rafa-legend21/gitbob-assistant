"""
IBM Bob API client for text generation
"""

import requests
import time
from typing import Optional, Dict, Any
from gitbob.config import Config


class BobClient:
    """Client for IBMpython -m pip install -e . Bob API"""
    
    def __init__(self, config: Config):
        """Initialize Bob client
        
        Args:
            config: Configuration instance
        """
        self.config = config
        self.api_key = config.get("ibm_bob.api_key")
        self.endpoint = config.get("ibm_bob.endpoint")
        self.model = config.get("ibm_bob.model")
        self.timeout = config.get("ibm_bob.timeout", 30)
        self.max_retries = config.get("ibm_bob.max_retries", 3)
        
        if not self.api_key:
            raise ValueError("IBM Bob API key not configured")
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })
    
    def generate(
        self, 
        prompt: str, 
        max_tokens: int = 500,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """Generate text using IBM Bob
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)
            **kwargs: Additional parameters
            
        Returns:
            Generated text
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            **kwargs
        }
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.post(
                    f"{self.endpoint}/generate",
                    json=payload,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("text", "").strip()
                elif response.status_code == 429:
                    # Rate limit - wait and retry
                    wait_time = 2 ** attempt
                    print(f"Rate limited. Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                    continue
                else:
                    error_msg = response.json().get("error", "Unknown error")
                    raise Exception(f"API error ({response.status_code}): {error_msg}")
                    
            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    print(f"Request timeout. Retrying... (attempt {attempt + 1}/{self.max_retries})")
                    continue
                raise Exception("Request timed out after multiple retries")
            
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries - 1:
                    print(f"Request failed. Retrying... (attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(1)
                    continue
                raise Exception(f"Request failed: {e}")
        
        raise Exception("Failed to generate text after multiple retries")
    
    def generate_commit_message(self, prompt: str) -> str:
        """Generate commit message
        
        Args:
            prompt: Formatted prompt for commit message
            
        Returns:
            Generated commit message
        """
        return self.generate(
            prompt=prompt,
            max_tokens=300,
            temperature=0.5,  # Lower temperature for more consistent output
        )
    
    def generate_branch_names(self, prompt: str) -> list[str]:
        """Generate branch name suggestions
        
        Args:
            prompt: Formatted prompt for branch names
            
        Returns:
            List of suggested branch names
        """
        response = self.generate(
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
        )
        
        # Parse numbered list
        lines = response.strip().split('\n')
        branch_names = []
        
        for line in lines:
            line = line.strip()
            # Remove numbering (1., 2., 3., etc.)
            if line and (line[0].isdigit() or line.startswith('-')):
                # Extract branch name after number/bullet
                parts = line.split('.', 1) if '.' in line else line.split(' ', 1)
                if len(parts) > 1:
                    branch_name = parts[1].strip()
                    if branch_name:
                        branch_names.append(branch_name)
        
        return branch_names[:3]  # Return max 3 suggestions
    
    def generate_pr_description(self, prompt: str) -> str:
        """Generate PR description
        
        Args:
            prompt: Formatted prompt for PR description
            
        Returns:
            Generated PR description
        """
        return self.generate(
            prompt=prompt,
            max_tokens=800,
            temperature=0.6,
        )
    
    def test_connection(self) -> bool:
        """Test API connection
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = self.generate(
                prompt="Test connection. Respond with 'OK'.",
                max_tokens=10,
                temperature=0.0
            )
            return bool(response)
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False


class MockBobClient(BobClient):
    """Mock Bob client for testing without API calls"""
    
    def __init__(self, config: Config):
        """Initialize mock client"""
        self.config = config
        self.api_key = "mock_key"
        self.endpoint = "mock_endpoint"
        self.model = "mock_model"
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate mock response"""
        if "commit message" in prompt.lower():
            return """feat(auth): implement JWT token refresh mechanism

- Add refresh token endpoint in auth controller
- Update token validation middleware
- Add token expiry configuration
- Include unit tests for token refresh flow"""
        
        elif "branch name" in prompt.lower():
            return """1. feature/jwt-token-refresh
2. feature/auth-token-refresh-mechanism
3. feat/implement-jwt-refresh"""
        
        elif "pull request" in prompt.lower():
            return """## Summary
Implements JWT token refresh mechanism to improve authentication security and user experience.

## Changes
- Added refresh token endpoint in authentication controller
- Updated token validation middleware to handle refresh tokens
- Added configuration for token expiry times
- Implemented comprehensive unit tests

## Testing
- Unit tests added for token refresh flow
- Manual testing completed for token expiry scenarios
- Verified backward compatibility with existing auth flow

## Related Issues
Closes #123"""
        
        return "Mock response"
    
    def test_connection(self) -> bool:
        """Mock connection test"""
        return True

# Made with Bob
