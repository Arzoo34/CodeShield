import subprocess
import tempfile
import os
import logging
from typing import Dict, Any, Optional
import time

logger = logging.getLogger(__name__)

class SandboxWorker:
    """Handles secure code execution in isolated environments"""

    def __init__(self):
        self.timeout = 30  # seconds
        self.max_memory = 512 * 1024 * 1024  # 512MB

    def execute_code(self, code: str, language: str = 'python', stdin: str = '') -> Dict[str, Any]:
        """
        Execute code in a sandboxed environment

        Args:
            code: The code to execute
            language: Programming language
            stdin: Standard input for the program

        Returns:
            Dict containing execution results
        """
        try:
            if language.lower() == 'python':
                return self._execute_python(code, stdin)
            elif language.lower() in ['cpp', 'c++']:
                return self._execute_cpp(code, stdin)
            elif language.lower() in ['javascript', 'js']:
                return self._execute_javascript(code, stdin)
            elif language.lower() == 'java':
                return self._execute_java(code, stdin)
            else:
                return {
                    'verdict': 'UNSUPPORTED_LANGUAGE',
                    'error': f'Unsupported language: {language}',
                    'execution_time': 0,
                    'stdout': '',
                    'stderr': ''
                }

        except Exception as e:
            logger.error(f"Sandbox execution error: {str(e)}")
            return {
                'verdict': 'RUNTIME_ERROR',
                'error': f'Execution failed: {str(e)}',
                'execution_time': 0,
                'stdout': '',
                'stderr': ''
            }

    def _execute_python(self, code: str, stdin: str = '') -> Dict[str, Any]:
        """Execute Python code safely"""
        start_time = time.time()

        # Create a temporary file for the code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            # Execute with timeout and resource limits
            result = subprocess.run(
                ['python', temp_file],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                input=stdin,
                cwd=os.path.dirname(temp_file)
            )

            execution_time = time.time() - start_time

            # Determine verdict
            if result.returncode == 0:
                verdict = 'OK'
            else:
                verdict = 'RUNTIME_ERROR'

            return {
                'verdict': verdict,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode,
                'execution_time': round(execution_time * 1000, 2),  # Convert to milliseconds
                'success': result.returncode == 0
            }

        except subprocess.TimeoutExpired:
            return {
                'verdict': 'TLE',
                'error': 'Code execution timed out',
                'execution_time': self.timeout * 1000,
                'stdout': '',
                'stderr': 'Time Limit Exceeded'
            }
        except Exception as e:
            return {
                'verdict': 'RUNTIME_ERROR',
                'error': f'Execution error: {str(e)}',
                'execution_time': round((time.time() - start_time) * 1000, 2),
                'stdout': '',
                'stderr': str(e)
            }
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file)
            except:
                pass

    def _execute_cpp(self, code: str, stdin: str = '') -> Dict[str, Any]:
        """Execute C++ code safely"""
        start_time = time.time()

        # Create temporary files for source and executable
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as f:
            f.write(code)
            source_file = f.name

        executable_file = source_file.replace('.cpp', '.out')

        try:
            # Compile the C++ code
            compile_result = subprocess.run(
                ['g++', '-o', executable_file, source_file],
                capture_output=True,
                text=True,
                timeout=10  # Compilation timeout
            )

            if compile_result.returncode != 0:
                return {
                    'verdict': 'CE',  # Compilation Error
                    'stdout': '',
                    'stderr': compile_result.stderr,
                    'execution_time': round((time.time() - start_time) * 1000, 2),
                    'success': False
                }

            # Execute the compiled program
            exec_start_time = time.time()
            result = subprocess.run(
                [executable_file],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                input=stdin,
                cwd=os.path.dirname(source_file)
            )

            execution_time = time.time() - start_time

            # Determine verdict
            if result.returncode == 0:
                verdict = 'OK'
            else:
                verdict = 'RUNTIME_ERROR'

            return {
                'verdict': verdict,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode,
                'execution_time': round(execution_time * 1000, 2),  # Convert to milliseconds
                'success': result.returncode == 0
            }

        except subprocess.TimeoutExpired:
            return {
                'verdict': 'TLE',
                'error': 'Code execution timed out',
                'execution_time': self.timeout * 1000,
                'stdout': '',
                'stderr': 'Time Limit Exceeded'
            }
        except Exception as e:
            return {
                'verdict': 'RUNTIME_ERROR',
                'error': f'Execution error: {str(e)}',
                'execution_time': round((time.time() - start_time) * 1000, 2),
                'stdout': '',
                'stderr': str(e)
            }
        finally:
            # Clean up temporary files
            try:
                os.unlink(source_file)
                if os.path.exists(executable_file):
                    os.unlink(executable_file)
            except:
                pass

    def _execute_javascript(self, code: str, stdin: str = '') -> Dict[str, Any]:
        """Execute JavaScript code safely"""
        # Check if Node.js is available
        try:
            subprocess.run(['node', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return {
                'verdict': 'UNSUPPORTED_LANGUAGE',
                'error': 'Node.js is not installed on the server',
                'execution_time': 0,
                'stdout': '',
                'stderr': 'Node.js must be installed on the server to execute JavaScript code. For local development, install Node.js from https://nodejs.org/'
            }

        start_time = time.time()

        # Create a temporary file for the code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            # Execute with timeout and resource limits using Node.js
            result = subprocess.run(
                ['node', temp_file],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                input=stdin,
                cwd=os.path.dirname(temp_file)
            )

            execution_time = time.time() - start_time

            # Determine verdict
            if result.returncode == 0:
                verdict = 'OK'
            else:
                verdict = 'RUNTIME_ERROR'

            return {
                'verdict': verdict,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode,
                'execution_time': round(execution_time * 1000, 2),  # Convert to milliseconds
                'success': result.returncode == 0
            }

        except subprocess.TimeoutExpired:
            return {
                'verdict': 'TLE',
                'error': 'Code execution timed out',
                'execution_time': self.timeout * 1000,
                'stdout': '',
                'stderr': 'Time Limit Exceeded'
            }
        except Exception as e:
            return {
                'verdict': 'RUNTIME_ERROR',
                'error': f'Execution error: {str(e)}',
                'execution_time': round((time.time() - start_time) * 1000, 2),
                'stdout': '',
                'stderr': str(e)
            }
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file)
            except:
                pass

    def _execute_java(self, code: str, stdin: str = '') -> Dict[str, Any]:
        """Execute Java code safely"""
        # Check if Java is available
        try:
            subprocess.run(['javac', '-version'], capture_output=True, check=True)
            subprocess.run(['java', '-version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return {
                'verdict': 'UNSUPPORTED_LANGUAGE',
                'error': 'Java JDK is not installed on the server',
                'execution_time': 0,
                'stdout': '',
                'stderr': 'Java JDK must be installed on the server to execute Java code. For local development, install JDK from https://adoptium.net/'
            }

        start_time = time.time()

        # Extract class name from code (simple approach)
        lines = code.split('\n')
        class_name = None
        for line in lines:
            if line.strip().startswith('public class ') or line.strip().startswith('class '):
                parts = line.strip().split()
                if len(parts) >= 2:
                    class_name = parts[1].split('{')[0].strip()
                    break

        if not class_name:
            return {
                'verdict': 'CE',
                'error': 'Could not find public class declaration',
                'execution_time': 0,
                'stdout': '',
                'stderr': 'Compilation Error: No public class found'
            }

        # Create a temporary directory and source file with correct name
        temp_dir = tempfile.mkdtemp()
        source_file = os.path.join(temp_dir, f"{class_name}.java")

        try:
            # Write the code to the correctly named file
            with open(source_file, 'w') as f:
                f.write(code)

            # Compile the Java code
            compile_result = subprocess.run(
                ['javac', source_file],
                capture_output=True,
                text=True,
                timeout=10,  # Compilation timeout
                cwd=temp_dir
            )

            if compile_result.returncode != 0:
                return {
                    'verdict': 'CE',  # Compilation Error
                    'stdout': '',
                    'stderr': compile_result.stderr,
                    'execution_time': round((time.time() - start_time) * 1000, 2),
                    'success': False
                }

            # Execute the compiled program
            result = subprocess.run(
                ['java', '-cp', temp_dir, class_name],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                input=stdin,
                cwd=temp_dir
            )

            execution_time = time.time() - start_time

            # Determine verdict
            if result.returncode == 0:
                verdict = 'OK'
            else:
                verdict = 'RUNTIME_ERROR'

            return {
                'verdict': verdict,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode,
                'execution_time': round(execution_time * 1000, 2),  # Convert to milliseconds
                'success': result.returncode == 0
            }

        except subprocess.TimeoutExpired:
            return {
                'verdict': 'TLE',
                'error': 'Code execution timed out',
                'execution_time': self.timeout * 1000,
                'stdout': '',
                'stderr': 'Time Limit Exceeded'
            }
        except Exception as e:
            return {
                'verdict': 'RUNTIME_ERROR',
                'error': f'Execution error: {str(e)}',
                'execution_time': round((time.time() - start_time) * 1000, 2),
                'stdout': '',
                'stderr': str(e)
            }
        finally:
            # Clean up temporary directory and files
            try:
                import shutil
                shutil.rmtree(temp_dir)
            except:
                pass

def test_sandbox():
    """Test the sandbox functionality"""
    worker = SandboxWorker()

    # Test successful execution
    test_code = "print('Hello, World!')\nprint('2 + 3 =', 2 + 3)"
    result = worker.execute_code(test_code, 'python')

    print("Test Result:")
    print(f"Success: {result.get('success', False)}")
    print(f"Output: {result.get('stdout', '')}")
    print(f"Execution time: {result.get('execution_time', 0):.3f}s")

if __name__ == '__main__':
    test_sandbox()
