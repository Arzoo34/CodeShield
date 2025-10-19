# TODO: Fix Java Compilation Error in Sandbox Worker

## Steps to Complete
- [x] Modify `_execute_java` method in `backend/sandbox_worker.py` to create temporary file with class name matching the file name (e.g., `Main.java` for `public class Main`)
- [x] Use `tempfile.mkdtemp()` to create a temporary directory and place the Java file inside it
- [x] Update compilation and execution commands to use the correct file paths
- [x] Ensure proper cleanup of temporary directory and files
- [x] Test the changes with sample Java code to verify compilation and execution work without errors (tested via Docker in backend container)
