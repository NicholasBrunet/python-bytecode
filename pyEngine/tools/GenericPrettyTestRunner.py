import unittest
import time
import traceback

# Reusable standard ANSI colors for scannability
COLOR_PASS = "\033[92m"  # Green
COLOR_PASS2 = "\033[38;2;144;238;144m"
COLOR_FAIL = "\033[91m"  # Red
COLOR_SKIP = "\033[93m"  # Yellow
COLOR_TEXT = "\033[90m"  # Grey (for secondary details)
COLOR_BOLD = "\033[1m"   # Bold
COLOR_OFF  = "\033[0m"   # Reset formatting

class GenericPrettyTestResult(unittest.TextTestResult):
    """Tracks and formats test execution data uniformly in real-time."""
    
    def startTest(self, test):
        super().startTest(test)
        # Record structural telemetry start time
        self._start_time = time.time()

    def _get_test_info(self, test) -> str:
        """Extracts class and method structure cleanly from the test object."""
        class_name = type(test).__name__
        method_name = test._testMethodName
        duration = (time.time() - self._start_time) * 1000
        return f"{COLOR_BOLD}{class_name}{COLOR_OFF} -> {method_name} {COLOR_TEXT}({duration:.1f}ms){COLOR_OFF}"

    def addSuccess(self, test):
        print(f"  {COLOR_PASS}✓ PASS{COLOR_OFF} │ {self._get_test_info(test)} {COLOR_PASS}^^^^^{COLOR_OFF}")

    def addFailure(self, test, err):
        print(f"  {COLOR_FAIL}✗ FAIL{COLOR_OFF} │ {self._get_test_info(test)}")
        self.failures.append((test, err))

    def addError(self, test, err):
        print(f"  {COLOR_FAIL}‼ ERRR{COLOR_OFF} │ {self._get_test_info(test)}")
        self.errors.append((test, err))

    # def addSkip(self, test, reason):
    #     print(f"  {COLOR_SKIP}⤼ SKIP{COLOR_OFF} │ {self._get_test_info(test)} {COLOR_TEXT}[{reason}]{COLOR_OFF}")
    #     self.skips.append((test, reason))


class GenericPrettyTestRunner(unittest.TextTestRunner):
    """Renders high-density runtime analytics and structural issue reports."""
    
    resultclass = GenericPrettyTestResult

    def run(self, test):
        result = self._makeResult()
        
        print(f"\n{COLOR_BOLD}⚙ Execution Pipeline Init{COLOR_OFF}")
        print("─" * 60)
        
        start_time = time.time()
        test(result)
        total_time = time.time() - start_time
        
        print("─" * 60)
        print(f"{COLOR_BOLD}📈 Metrics Summary{COLOR_OFF} {COLOR_TEXT}({total_time:.2f} seconds total){COLOR_OFF}")
        print("─" * 60)
        
        # Calculate status counts dynamically
        total = result.testsRun
        failed = len(result.failures)
        errors = len(result.errors)
        # skipped = len(result.skips)
        passed = total - failed - errors
        
        # Punchy visual status block
        print(f"  Total Evaluated : {total}")
        print(f"  {COLOR_PASS}Passed          : {passed}{COLOR_OFF}")
        print(f"  {COLOR_FAIL}Failed          : {failed}{COLOR_OFF}")
        if errors > 0:
            print(f"  {COLOR_FAIL}Crashes/Errors  : {errors}{COLOR_OFF}")
        # if skipped > 0:
        #     print(f"  {COLOR_SKIP}Skipped         : {skipped}{COLOR_OFF}")
            
        # Group, indent, and format execution failure tracebacks directly
        if failed > 0 or errors > 0:
            print(f"\n{COLOR_BOLD}🔍 Structural Traceback Logs:{COLOR_OFF}")
            for report_label, dynamic_collection in [("Failure Context", result.failures), ("Runtime Error Context", result.errors)]:
                for failed_test, raw_trace in dynamic_collection:
                    print("\n" + "=" * 60)
                    print(f"{COLOR_FAIL}{COLOR_BOLD}⚠️ {report_label} in: {failed_test}{COLOR_OFF}")
                    print("=" * 60)
                    
                    exctype, value, tb = raw_trace
                    formatted_trace = "".join(traceback.format_exception(exctype, value, tb))
                    
                    # Indent the whole error output block so it reads cleanly
                    for line in formatted_trace.splitlines():
                        print(f"  {line}")
                        
        return result
