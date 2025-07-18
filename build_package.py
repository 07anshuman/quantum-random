#!/usr/bin/env python3
"""
Build script for the Quantum Randomness Service package.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def clean_build():
    """Clean previous build artifacts."""
    print("🧹 Cleaning build artifacts...")
    
    dirs_to_clean = ["build", "dist", "*.egg-info"]
    files_to_clean = ["*.pyc", "__pycache__"]
    
    for pattern in dirs_to_clean:
        for path in Path(".").glob(pattern):
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
                print(f"   Removed directory: {path}")
    
    for pattern in files_to_clean:
        for path in Path(".").rglob(pattern):
            if path.is_file():
                path.unlink()
                print(f"   Removed file: {path}")
            elif path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
                print(f"   Removed directory: {path}")
    
    print("✅ Clean completed")


def check_dependencies():
    """Check if all required dependencies are available."""
    print("📦 Checking dependencies...")
    
    required_packages = [
        "setuptools",
        "wheel",
        "build",
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"   ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"   ❌ {package} (missing)")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        
        for package in missing_packages:
            if not run_command(f"pip install {package}", f"Installing {package}"):
                return False
    
    print("✅ All dependencies available")
    return True


def build_package():
    """Build the package."""
    print("🔨 Building package...")
    
    # Build the package
    if not run_command("python -m build", "Building package"):
        return False
    
    print("✅ Package built successfully")
    return True


def test_package():
    """Test the built package."""
    print("🧪 Testing built package...")
    
    # Find the built wheel
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("❌ No dist directory found")
        return False
    
    wheels = list(dist_dir.glob("*.whl"))
    if not wheels:
        print("❌ No wheel files found in dist/")
        return False
    
    wheel_file = wheels[0]
    print(f"📦 Testing wheel: {wheel_file}")
    
    # Install the wheel in a test environment
    if not run_command(f"pip install {wheel_file}", "Installing wheel for testing"):
        return False
    
    # Test basic functionality
    test_code = """
import sys
try:
    from qrandom import QuantumRandom, get_random, get_random_batch
    print("✅ Package imports work")
    
    # Test client instantiation
    client = QuantumRandom()
    print("✅ Client instantiation works")
    
    print("✅ Package test passed")
    sys.exit(0)
except Exception as e:
    print(f"❌ Package test failed: {e}")
    sys.exit(1)
"""
    
    if not run_command(f"python -c '{test_code}'", "Testing package functionality"):
        return False
    
    print("✅ Package test completed successfully")
    return True


def show_build_info():
    """Show information about the built package."""
    print("\n📊 Build Information:")
    print("-" * 30)
    
    dist_dir = Path("dist")
    if dist_dir.exists():
        files = list(dist_dir.glob("*"))
        for file in files:
            size = file.stat().st_size
            print(f"📦 {file.name} ({size:,} bytes)")
    
    print("\n📦 Installation commands:")
    print("   pip install dist/*.whl")
    print("   pip install quantum-randomness-service")


def main():
    """Main build function."""
    print("🌊 Quantum Randomness Service Package Builder")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("setup.py").exists():
        print("❌ setup.py not found. Please run this script from the project root.")
        return False
    
    # Run build steps
    steps = [
        ("Clean build artifacts", clean_build),
        ("Check dependencies", check_dependencies),
        ("Build package", build_package),
        ("Test package", test_package),
    ]
    
    for step_name, step_func in steps:
        print(f"\n{'='*50}")
        print(f"📋 {step_name}")
        print(f"{'='*50}")
        
        if not step_func():
            print(f"\n❌ Build failed at step: {step_name}")
            return False
    
    # Show build information
    show_build_info()
    
    print(f"\n{'='*50}")
    print("🎉 Package build completed successfully!")
    print("=" * 50)
    print("\n📦 The package is ready for distribution!")
    print("   Files are in the dist/ directory")
    print("   Users can install with: pip install dist/*.whl")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 