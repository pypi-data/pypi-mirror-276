
import coloredlogs, logging, verboselogs, json
from typing import Literal, Optional
from yaspin import yaspin
import time
import threading
from contextlib import contextmanager

class EndpointFilter(logging.Filter):
    def __init__(self, endpoints):
        super().__init__()
        self.endpoints = endpoints

    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        return not any(endpoint in message for endpoint in self.endpoints)

def flexible_json_serializer(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif hasattr(obj, 'tolist'):
        return obj.tolist()
    elif hasattr(obj, 'to_json'):
        return json.loads(obj.to_json())
    return repr(obj)

class AutoFormatAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        if isinstance(msg, (dict, list, tuple, set)) or hasattr(msg, '__dict__'):
            try:
                msg = json.dumps(msg, indent=4, default=flexible_json_serializer)
            except TypeError:
                msg = repr(msg)
        return msg, kwargs
    
    def __getattr__(self, name):
        verboselogs_methods = {
            'verbose': logging.VERBOSE,
            'success': logging.SUCCESS,
            'spam': logging.SPAM,
            'notice': logging.NOTICE
        }
        if name in verboselogs_methods:
            level = verboselogs_methods[name]
            def log_method(message, *args, **kwargs):
                if self.isEnabledFor(level):
                    self.log(level, message, *args, **kwargs)

            return log_method

        raise AttributeError(f"{name} not found in LoggerAdapter or logger")

LevelType = Literal["DEBUG", "INFO", "NOTICE", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]
ColorType = Literal["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
TimerType = Literal["print", "debug", "info", "warning", "error", "critical"]
class CustomLogger:
    """
    A custom logger class that provides a flexible and customizable logging interface.
    Available log levels: SPAM, DEBUG, VERBOSE, INFO, NOTICE, WARNING, SUCCESS, ERROR, CRITICAL

    Currently available features:
    - Spinner
        - A context manager for displaying a progress spinner with a message.
        - `CustomLogger().spinner(message: str, timer: bool=True)`
        - See .spinner() for more information.

    - Timer
        - A context manager for timing a block of code.
        - `CustomLogger().timer(task_name: str, type: TimerType="info")`
        - See .timer() for more information.
        
    """
    def __init__(self, level: Optional[LevelType] ="INFO", name='werkzeug', ignore: list | None = None, include_date: bool=False, include_level: bool =False, date_color: ColorType ='yellow'):
        if ignore is None:
            ignore = []
        verboselogs.install()
        logging.VERBOSE = verboselogs.VERBOSE
        logging.SPAM = verboselogs.SPAM
        logging.NOTICE = verboselogs.NOTICE
        logging.SUCCESS = verboselogs.SUCCESS

        self.logger = logging.getLogger(name)
        self.logger.addFilter(EndpointFilter(ignore))

        if level is None:
            self.logger.disabled = True
        else:
            format_elements = []
            if include_date:
                format_elements.append('%(asctime)s')
            if include_level:
                format_elements.append('%(levelname)s')
            format_elements.append('%(message)s')
            log_format = ' '.join(format_elements)
            field_styles = {'asctime': {'color': date_color, 'bold': False}}

            coloredlogs.install(logger=self.logger, isatty=True, fmt=log_format, level=level.upper(), field_styles=field_styles)
            self.logger.disabled = False
            
        self.adapter = AutoFormatAdapter(self.logger)
    
    def __getattr__(self, name):
        return getattr(self.adapter, name)
    
    class ProgressSpinner:
        # ~ Will be expanding on this in the future.
        def __init__(self, message: str, timer: bool=True, frequency: float=0.1):
            self.message = message
            self.original_message = message
            self.spinner = None
            self.should_fail = False
            self.start_time = None
            self._stop_timer = threading.Event()
            self._should_time = timer
            self.frequency = frequency
            self._interrupted = False
            self.exited = False

        def _handle_exception(self, exception):
            self._stop_timer.set()
            if self.spinner:
                self.spinner.fail(f"💥 Exception - {exception}")
                self.spinner.stop()

        def _update_timer(self):
            try:
                while not self._stop_timer.is_set() and not self._interrupted:
                    elapsed_time = time.time() - self.start_time
                    self.spinner.text = f"{self.message} ({elapsed_time:.2f} seconds)"
                    time.sleep(self.frequency)
            except KeyboardInterrupt:
                self._interrupted = True

        def __enter__(self):
            try:
                self.spinner = yaspin(text=self.message, color="white")
                self.spinner.start()
                if self._should_time:
                    self.start_time = time.time()
                    self._stop_timer.clear()
                    self._timer_thread = threading.Thread(target=self._update_timer)
                    self._timer_thread.daemon = True # ~ This is important to prevent the thread from blocking the main thread.
                    self._timer_thread.start()
                return self
            except Exception as e:
                self._handle_exception(e)

        def __exit__(self, exc_type, exc_val, exc_tb):
            try:
                # ~ Only using self.exited temporarily, it's a workaround
                # ~ to prevent the spinner from running twice, such as when
                # ~ the spinner.fail() is called before the block exits.
                if not self.exited:
                    self.exited = True
                    self._interrupted = True
                    if self._should_time:
                        elapsed_time = time.time() - self.start_time
                        self._stop_timer.set()
                        self._timer_thread.join()
                    else:
                        self.spinner.text = self.message

                    self.spinner.text = f"{self.message} ({elapsed_time:.2f}s)"
                    if exc_type is not None or self.should_fail:
                        self.spinner.fail("💥 ")
                    else:
                        self.spinner.ok("✅ ")
            except Exception as e:
                self._handle_exception(e)
            finally:
                if self.spinner:
                    self.spinner.stop()

        def fail(self, message: str = ""):
            if message:
                self.change(message)
            self.should_fail = True
            self.__exit__(None, None, None)

        def success(self, message: str = ""):
            if message:
                self.change(message)
            self.should_fail = False
            self.__exit__(None, None, None)

        def log(self, message: str):
            if self._should_time:
                self.spinner.write(f"{message} ({time.time() - self.start_time:.2f}s)")
            else:
                self.spinner.write(message)

        def change(self, message: str):
            self.message = message
            if self._should_time:
                self.spinner.text = f"{message} ({time.time() - self.start_time:.2f}s)" 
            else:
                self.spinner.text = message

        def revert(self):
            self.change(self.original_message)

        def get_time(self):
            if self.start_time is None:
                return None
            return time.time() - self.start_time

    def spinner(self, message: str, timer: bool=True, frequency: float=0.1):
        """
        Returns a context manager for displaying a progress spinner with the given message.
        
        Parameters:
            message (str): The message to display alongside the spinner.
            timer (bool): Whether to display a timer alongside the spinner.
            frequency (float): The frequency at which to update the timer.
        
        Returns:
            ProgressSpinner: A context manager for the spinner.
        """
        return self.ProgressSpinner(message, timer, frequency)
    
    class TimerContext:
        def __init__(self, task_name: str, logger: AutoFormatAdapter, log_type: TimerType):
            self.task_name = task_name
            self.logger = logger
            self.log_type = log_type
            self.start_time = None
            self.end_time = None

        def __enter__(self):
            self.start_time = time.perf_counter()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.end_time = time.perf_counter()
            elapsed_time = self.end_time - self.start_time
            self._log_time(elapsed_time)

        def get_time(self):
            if self.start_time is None:
                return 0.0
            if self.end_time is not None:
                return self.end_time - self.start_time
            return time.perf_counter() - self.start_time

        def _log_time(self, elapsed_time):
            message = f"{self.task_name}: {elapsed_time:.4f}s"
            if self.log_type == "print":
                print(message)
            elif self.log_type == "debug":
                self.logger.debug(message)
            elif self.log_type == "info":
                self.logger.info(message)
            elif self.log_type == "warning":
                self.logger.warning(message)
            elif self.log_type == "error":
                self.logger.error(message)
            elif self.log_type == "critical":
                self.logger.critical(message)

    @contextmanager
    def timer(self, task_name: str, type: Optional[TimerType] ="info"):
        """
        Returns a context manager for timing a block of code.
        Automatically logs the elapsed time when the block exits.
        """
        timer_context = self.TimerContext(task_name, self.adapter, type)
        try:
            timer_context.__enter__()
            yield timer_context
        finally:
            timer_context.__exit__(None, None, None)
    
