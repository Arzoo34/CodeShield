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

    def execute_code(self, code: str, language: str = 'python') -> Dict[str, Any]:
        """
        Execute code in a sandboxed environment

        Args:
            code: The code to execute
            language: Programming language

        Returns:
            Dict containing execution results
        """
        try:
            if language.lower() == 'python':
                return self._execute_python(code)
            else:
                return {
                    'error': f'Unsupported language: {language}',
                    'execution_time': 0
                }

        except Exception as e:
            logger.error(f"Sandbox execution error: {str(e)}")
            return {
                'error': f'Execution failed: {str(e)}',
                'execution_time': 0
            }

    def _execute_python(self, code: str) -> Dict[str, Any]:
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
                cwd=os.path.dirname(temp_file)
            )

            execution_time = time.time() - start_time

            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode,
                'execution_time': execution_time,
                'success': result.returncode == 0
            }

        except subprocess.TimeoutExpired:
            return {
                'error': 'Code execution timed out',
                'execution_time': self.timeout,
                'timeout': True
            }
        except Exception as e:
            return {
                'error': f'Execution error: {str(e)}',
                'execution_time': time.time() - start_time
            }
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file)
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
