"""
AsyncIO Integration for Time Warp IDE

This module provides asyncio-based utilities for non-blocking UI operations,
allowing the IDE to remain responsive during long-running interpreter tasks.
"""

import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Awaitable, Callable, Optional, TypeVar

T = TypeVar("T")


class AsyncRunner:
    """
    Manages asyncio operations in a GUI application context.

    This class provides utilities for running async code from synchronous GUI
    callbacks and managing background tasks without blocking the UI.
    """

    def __init__(self, max_workers: int = 4):
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._running = False

    def start(self) -> None:
        """Start the asyncio event loop in a background thread"""
        if self._running:
            return

        def run_loop() -> None:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._running = True
            try:
                self._loop.run_forever()
            finally:
                self._running = False

        thread = threading.Thread(target=run_loop, daemon=True)
        thread.start()

        # Wait for loop to be ready
        while self._loop is None:
            pass

    def stop(self) -> None:
        """Stop the asyncio event loop"""
        if self._loop and self._running:
            self._loop.call_soon_threadsafe(self._loop.stop)
            self._running = False

    def run_async(self, coro: Awaitable[T]) -> asyncio.Future[T]:
        """Run an async coroutine and return a Future"""
        if not self._loop:
            raise RuntimeError("AsyncRunner not started")
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return future  # type: ignore

    def run_in_executor(self, func: Callable[..., T], *args: Any) -> asyncio.Future[T]:
        """Run a blocking function in the thread pool executor"""
        if not self._loop:
            raise RuntimeError("AsyncRunner not started")

        async def _run() -> T:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(self._executor, func, *args)

        return self.run_async(_run())

    def schedule_callback(
        self, callback: Callable[[], None], delay: float = 0.0
    ) -> None:
        """Schedule a callback to run after a delay (in seconds)"""
        if not self._loop:
            raise RuntimeError("AsyncRunner not started")

        async def _delayed_callback() -> None:
            if delay > 0:
                await asyncio.sleep(delay)
            callback()

        self.run_async(_delayed_callback())


class BackgroundTask:
    """
    Represents a background task that can be monitored and cancelled.

    This class provides a high-level interface for running long operations
    in the background while keeping the UI responsive.
    """

    def __init__(self, runner: AsyncRunner):
        self.runner = runner
        self._future: Optional[asyncio.Future] = None
        self._cancelled = False
        self._completed = False
        self._result: Any = None
        self._exception: Optional[Exception] = None

    def start(
        self,
        coro: Awaitable[T],
        on_complete: Optional[Callable[[T], None]] = None,
        on_error: Optional[Callable[[Exception], None]] = None,
    ) -> None:
        """Start the background task"""

        async def _task_wrapper() -> None:
            try:
                result = await coro
                self._result = result
                self._completed = True
                if on_complete:
                    on_complete(result)
            except asyncio.CancelledError:
                self._cancelled = True
            except Exception as e:
                self._exception = e
                self._completed = True
                if on_error:
                    on_error(e)

        self._future = self.runner.run_async(_task_wrapper())

    def cancel(self) -> None:
        """Cancel the running task"""
        if self._future and not self._future.done():
            self._future.cancel()
            self._cancelled = True

    @property
    def is_running(self) -> bool:
        """Check if the task is currently running"""
        return self._future is not None and not self._future.done()

    @property
    def is_completed(self) -> bool:
        """Check if the task has completed"""
        return self._completed

    @property
    def is_cancelled(self) -> bool:
        """Check if the task was cancelled"""
        return self._cancelled

    @property
    def result(self) -> Any:
        """Get the task result (if completed successfully)"""
        if not self._completed:
            raise RuntimeError("Task not completed")
        if self._exception:
            raise self._exception
        return self._result

    @property
    def exception(self) -> Optional[Exception]:
        """Get the task exception (if any)"""
        return self._exception


class AsyncInterpreterRunner:
    """
    Async wrapper for interpreter operations.

    This class provides async versions of interpreter operations that can
    run in the background without blocking the UI.
    """

    def __init__(self, interpreter_class: type, runner: AsyncRunner):
        self.interpreter_class = interpreter_class
        self.runner = runner

    async def execute_program_async(
        self, program_lines: list[str], variables: Optional[dict] = None
    ) -> dict:
        """
        Execute a program asynchronously.

        Args:
            program_lines: List of program lines to execute
            variables: Initial variables dictionary

        Returns:
            Final state dictionary with variables and execution results
        """

        def _execute() -> dict:
            interpreter = self.interpreter_class()
            if variables:
                interpreter.variables.update(variables)

            # Execute program lines
            for line in program_lines:
                try:
                    result = interpreter.execute_line(line)
                    if result == "end":
                        break
                except Exception as e:
                    return {"error": str(e), "variables": interpreter.variables}

            return {"variables": interpreter.variables, "success": True}

        # Run in executor to avoid blocking
        future = self.runner.run_in_executor(_execute)
        return await asyncio.wrap_future(future)

    async def evaluate_expression_async(
        self, expression: str, variables: Optional[dict] = None
    ) -> Any:
        """
        Evaluate an expression asynchronously.

        Args:
            expression: Expression to evaluate
            variables: Variable context

        Returns:
            Expression result
        """

        def _evaluate() -> Any:
            interpreter = self.interpreter_class()
            if variables:
                interpreter.variables.update(variables)
            return interpreter.evaluate_expression(expression)

        future = self.runner.run_in_executor(_evaluate)
        return await asyncio.wrap_future(future)


# Global async runner instance
_async_runner = AsyncRunner()


def get_async_runner() -> AsyncRunner:
    """Get the global async runner instance"""
    return _async_runner


def init_async_support() -> None:
    """Initialize asyncio support for the application"""
    _async_runner.start()


def shutdown_async_support() -> None:
    """Shutdown asyncio support"""
    _async_runner.stop()


# Convenience functions for common async operations
async def run_interpreter_operation(
    interpreter_class: type, operation: str, *args: Any, **kwargs: Any
) -> Any:
    """
    Run an interpreter operation asynchronously.

    Args:
        interpreter_class: The interpreter class to use
        operation: Operation name ('execute_program', 'evaluate_expression')
        *args: Positional arguments for the operation
        **kwargs: Keyword arguments for the operation
    """
    runner = get_async_runner()
    async_runner = AsyncInterpreterRunner(interpreter_class, runner)

    if operation == "execute_program":
        return await async_runner.execute_program_async(*args, **kwargs)
    elif operation == "evaluate_expression":
        return await async_runner.evaluate_expression_async(*args, **kwargs)
    else:
        raise ValueError(f"Unknown operation: {operation}")


def create_background_task(
    coro: Awaitable[T],
    on_complete: Optional[Callable[[T], None]] = None,
    on_error: Optional[Callable[[Exception], None]] = None,
) -> BackgroundTask:
    """
    Create and start a background task.

    Args:
        coro: The coroutine to run
        on_complete: Callback for successful completion
        on_error: Callback for errors

    Returns:
        BackgroundTask instance for monitoring/cancellation
    """
    runner = get_async_runner()
    task = BackgroundTask(runner)
    task.start(coro, on_complete, on_error)
    return task
