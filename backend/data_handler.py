"""
Module to handle XLSX file operations for Math Study Resources
"""
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional
import json


class MathResourcesManager:
    """Manages reading and processing math learning resources from XLSX file"""
    
    def __init__(self, file_path: str):
        """
        Initialize the manager with path to XLSX file
        
        Args:
            file_path: Path to the math_websites.xlsx file
        """
        self.file_path = file_path
        self.resources_df = None
        self.load_resources()
    
    def load_resources(self):
        """Load resources from XLSX file"""
        try:
            # Read the XLSX file
            self.resources_df = pd.read_excel(self.file_path, sheet_name='Websites')
            print(f"Loaded {len(self.resources_df)} resources from {self.file_path}")
        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
            self.resources_df = pd.DataFrame()
        except Exception as e:
            print(f"Error loading resources: {e}")
            self.resources_df = pd.DataFrame()
    
    def get_resources_for_topic(self, topic: str) -> List[Dict]:
        """
        Get resources related to a specific math topic
        
        Args:
            topic: The math topic to search for (e.g., 'Calculus', 'Algebra')
            
        Returns:
            List of resource dictionaries matching the topic
        """
        if self.resources_df.empty:
            return []
        
        # Search in topic and description columns
        matching = self.resources_df[
            self.resources_df['Topic'].str.contains(topic, case=False, na=False) |
            self.resources_df['Description'].str.contains(topic, case=False, na=False)
        ]
        
        return matching.to_dict('records')
    
    def get_all_resources(self) -> List[Dict]:
        """Get all available resources"""
        if self.resources_df.empty:
            return []
        return self.resources_df.to_dict('records')
    
    def get_resource_by_url(self, url: str) -> Optional[Dict]:
        """Get resource by URL"""
        if self.resources_df.empty:
            return None
        
        matching = self.resources_df[self.resources_df['URL'] == url]
        if not matching.empty:
            return matching.iloc[0].to_dict()
        return None
    
    def get_resources_as_context(self) -> str:
        """
        Convert resources to a formatted string for AI context
        
        Returns:
            Formatted string with all resources
        """
        if self.resources_df.empty:
            return "No resources available."
        
        context = "Available Math Learning Resources:\n"
        context += "=" * 60 + "\n"
        
        for idx, row in self.resources_df.iterrows():
            context += f"\n{idx + 1}. {row['Title']}\n"
            context += f"   Topic: {row['Topic']}\n"
            context += f"   URL: {row['URL']}\n"
            context += f"   Description: {row['Description']}\n"
        
        return context
    
    def search_resources(self, query: str) -> List[Dict]:
        """
        Search for resources using multiple fields
        
        Args:
            query: Search query
            
        Returns:
            List of matching resources
        """
        if self.resources_df.empty:
            return []
        
        # Search across multiple columns
        mask = (
            self.resources_df['Title'].str.contains(query, case=False, na=False) |
            self.resources_df['Topic'].str.contains(query, case=False, na=False) |
            self.resources_df['Description'].str.contains(query, case=False, na=False)
        )
        
        return self.resources_df[mask].to_dict('records')


def create_sample_excel():
    """
    Create a sample XLSX file with math learning resources
    This is a helper function for initial setup
    """
    data = {
        'Title': [
            'Khan Academy - Calculus',
            'MIT OpenCourseWare - Linear Algebra',
            'Paul\'s Online Math Notes - Algebra',
            'Brilliant.org - Problem Solving',
            '3Blue1Brown - Essence of Algebra',
            'Art of Problem Solving - AMC Prep',
            'Wolfram MathWorld - Reference',
            'CoolMath4Kids - Beginner Topics'
        ],
        'Topic': [
            'Calculus',
            'Linear Algebra',
            'Algebra',
            'Problem Solving',
            'Algebra',
            'Competition Math',
            'General Math',
            'Basics'
        ],
        'URL': [
            'https://www.khanacademy.org/math/calculus-all',
            'https://ocw.mit.edu/courses/mathematics/18-06-linear-algebra-spring-2010/',
            'https://tutorial.math.lamar.edu/',
            'https://brilliant.org/',
            'https://www.youtube.com/channel/UCYO_jab_esuFRV4b-r-ccEw',
            'https://artofproblemsolving.com/',
            'https://mathworld.wolfram.com/',
            'https://www.coolmath4kids.com/'
        ],
        'Description': [
            'Comprehensive calculus lessons covering limits, derivatives, and integrals',
            'Free university-level linear algebra course from MIT',
            'Detailed notes on algebra topics with examples and practice problems',
            'Interactive platform for learning advanced problem-solving techniques',
            'Visual explanations of algebra concepts through animations',
            'Preparation materials for AMC and other math competitions',
            'Extensive mathematical reference and definitions',
            'Interactive math games and lessons for beginners'
        ],
        'Difficulty': [
            'Intermediate',
            'Advanced',
            'Beginner-Intermediate',
            'Intermediate-Advanced',
            'Intermediate',
            'Advanced',
            'All Levels',
            'Beginner'
        ],
        'Type': [
            'Video Lessons',
            'Lectures',
            'Written Notes',
            'Interactive',
            'Video',
            'Courses',
            'Reference',
            'Games'
        ]
    }
    
    df = pd.DataFrame(data)
    return df
