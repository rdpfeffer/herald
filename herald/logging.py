from contextlib import contextmanager

import attr
import clikit


@attr.s()
class Logger:

    io = attr.ib()
    indent_level = attr.ib(default=0)

    def log(self, message):
        indent_str = self._padd_indent()
        self.io.write_line("{}{}".format(indent_str, message))

    @contextmanager
    def indent(self, increment=1):
        previous_indent = self.indent_level
        self.indent_level += increment
        try:
            yield self
        finally:
            self.indent_level = previous_indent

    def _padd_indent(self):
        return "    " * self.indent_level + "→ " if self.indent_level > 0 else ""


def console_logger():
    """Create a logger with console io
    :returns: Logger

    """
    return Logger(clikit.io.console_io.ConsoleIO())


def buffered_logger():
    """Create a logger with a buffered io srtream.
    :returns: Logger

    """
    return Logger(clikit.io.buffered_io.BufferedIO())
