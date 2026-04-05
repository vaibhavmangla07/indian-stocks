import sys

def error_message_detail(error: Exception, error_detail: sys) -> str:
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = (
        f"Error occurred in python script [{file_name}] "
        f"at line [{line_number}]: {str(error)}"
    )
    return error_message


class StocksyException(Exception):
    def __init__(self, error_message: Exception, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self) -> str:
        """Return the detailed error message."""
        return self.error_message

# Maintain backward compatibility
CustomException = StocksyException

if __name__ == "__main__":
    try:
        result = 10 / 0
    except Exception as e:
        raise StocksyException(e, sys)
