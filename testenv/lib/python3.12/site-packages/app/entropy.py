"""
Entropy analysis module for measuring randomness quality.
Provides various statistical tests for quantum random numbers.
"""

import numpy as np
import logging
from typing import List, Dict, Any, Optional
from collections import Counter

logger = logging.getLogger(__name__)


class EntropyAnalyzer:
    """Analyzes entropy and randomness quality of quantum random numbers."""
    
    def __init__(self):
        self.buffer_size = 1000
        self.number_buffer: List[int] = []
    
    def add_numbers(self, numbers: List[int]):
        """Add numbers to the analysis buffer."""
        self.number_buffer.extend(numbers)
        
        # Keep only the last buffer_size numbers
        if len(self.number_buffer) > self.buffer_size:
            self.number_buffer = self.number_buffer[-self.buffer_size:]
    
    def calculate_entropy_score(self, numbers: Optional[List[int]] = None) -> float:
        """Calculate entropy score (0-1, higher is better)."""
        if numbers is None:
            numbers = self.number_buffer
        
        if len(numbers) < 10:
            return 0.5  # Default score for small samples
        
        try:
            # Convert to numpy array
            arr = np.array(numbers, dtype=np.uint8)
            
            # Calculate Shannon entropy
            hist, _ = np.histogram(arr, bins=256, range=(0, 256))
            hist = hist[hist > 0]  # Remove zero counts
            if len(hist) == 0:
                return 0.0
            
            # Normalize histogram
            p = hist / np.sum(hist)
            
            # Calculate Shannon entropy
            entropy = -np.sum(p * np.log2(p))
            
            # Normalize to 0-1 scale (max entropy for 8-bit is 8)
            normalized_entropy = entropy / 8.0
            
            return min(1.0, max(0.0, normalized_entropy))
            
        except Exception as e:
            logger.error(f"Entropy calculation error: {e}")
            return 0.5
    
    def run_randomness_tests(self, numbers: Optional[List[int]] = None) -> Dict[str, Any]:
        """Run various randomness tests."""
        if numbers is None:
            numbers = self.number_buffer
        
        if len(numbers) < 100:
            return {"error": "Insufficient data for tests"}
        
        try:
            arr = np.array(numbers, dtype=np.uint8)
            
            results = {
                "entropy_score": self.calculate_entropy_score(numbers),
                "mean": float(np.mean(arr)),
                "std": float(np.std(arr)),
                "min": int(np.min(arr)),
                "max": int(np.max(arr)),
                "distribution_uniformity": self._test_uniformity(arr),
                "autocorrelation": self._test_autocorrelation(arr),
                "runs_test": self._runs_test(arr)
            }
            
            return results
            
        except Exception as e:
            logger.error(f"Randomness tests error: {e}")
            return {"error": str(e)}
    
    def _test_uniformity(self, arr: np.ndarray) -> float:
        """Test uniformity of distribution (0-1, higher is better)."""
        try:
            # Create histogram
            hist, _ = np.histogram(arr, bins=256, range=(0, 256))
            
            # Expected frequency for uniform distribution
            expected = len(arr) / 256
            
            # Calculate chi-square statistic
            chi_square = np.sum((hist - expected) ** 2 / expected)
            
            # Convert to uniformity score (lower chi-square = higher uniformity)
            # Using a simple transformation
            uniformity = 1.0 / (1.0 + chi_square / 1000)
            
            return float(min(1.0, max(0.0, uniformity)))
            
        except Exception as e:
            logger.error(f"Uniformity test error: {e}")
            return 0.5
    
    def _test_autocorrelation(self, arr: np.ndarray) -> float:
        """Test autocorrelation (0-1, lower is better for randomness)."""
        try:
            if len(arr) < 2:
                return 0.5
            
            # Calculate autocorrelation for lag 1
            autocorr = np.corrcoef(arr[:-1], arr[1:])[0, 1]
            
            if np.isnan(autocorr):
                return 0.5
            
            # Convert to score (lower autocorrelation = better randomness)
            score = 1.0 - abs(autocorr)
            
            return min(1.0, max(0.0, score))
            
        except Exception as e:
            logger.error(f"Autocorrelation test error: {e}")
            return 0.5
    
    def _runs_test(self, arr: np.ndarray) -> float:
        """Runs test for randomness."""
        try:
            if len(arr) < 10:
                return 0.5
            
            # Convert to binary sequence (above/below median)
            median = np.median(arr)
            binary = (arr > median).astype(int)
            
            # Count runs
            runs = 1
            for i in range(1, len(binary)):
                if binary[i] != binary[i-1]:
                    runs += 1
            
            # Expected number of runs for random sequence
            n = len(binary)
            expected_runs = (2 * np.sum(binary) * (n - np.sum(binary))) / n + 1
            
            # Calculate score based on how close actual runs are to expected
            if expected_runs == 0:
                return 0.5
            
            score = 1.0 - abs(runs - expected_runs) / expected_runs
            return min(1.0, max(0.0, score))
            
        except Exception as e:
            logger.error(f"Runs test error: {e}")
            return 0.5
    
    def get_quality_summary(self) -> Dict[str, Any]:
        """Get a summary of randomness quality."""
        if not self.number_buffer:
            return {"message": "No data available for analysis"}
        
        tests = self.run_randomness_tests()
        
        if "error" in tests:
            return tests
        
        # Calculate overall quality score
        scores = [
            tests["entropy_score"],
            tests["distribution_uniformity"],
            tests["autocorrelation"],
            tests["runs_test"]
        ]
        
        overall_score = float(np.mean(scores))
        
        return {
            "overall_quality": float(overall_score),
            "entropy_score": float(tests["entropy_score"]),
            "uniformity": float(tests["distribution_uniformity"]),
            "autocorrelation": float(tests["autocorrelation"]),
            "runs_test": float(tests["runs_test"]),
            "sample_size": len(self.number_buffer),
            "quality_level": self._get_quality_level(float(overall_score))
        }
    
    def _get_quality_level(self, score: float) -> str:
        """Get quality level description."""
        if score >= 0.9:
            return "Excellent"
        elif score >= 0.8:
            return "Very Good"
        elif score >= 0.7:
            return "Good"
        elif score >= 0.6:
            return "Fair"
        else:
            return "Poor"


# Global entropy analyzer instance
entropy_analyzer = EntropyAnalyzer() 