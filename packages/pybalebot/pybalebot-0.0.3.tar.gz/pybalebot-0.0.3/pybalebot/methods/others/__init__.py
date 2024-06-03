from .logout import Logout
from .close import Close
from .get_file import GetFile
from .answer_callback_query import AnswerCallbackQuery
from .answer_inline_query import AnswerInlineQuery
from .download import Download

class Others(
    Logout,
    Close,
    GetFile,
    AnswerCallbackQuery,
    AnswerInlineQuery,
    Download
):
    pass