__all__ = ("Kernel32",)
import ctypes


class Kernel32:
    """kernel.dllのAPIの一部を使いやすくしたクラス。

    現在実装されている関数は以下の通り。
    関数名の末尾に"[Ez]"が付いているものについては戻り値の型や一部処理の省略など簡素化された関数と、DLLオリジナルの関数の二つが実装されている。

    またdll関数を実行することでctypes.windll.user32へのアクセスを簡易化する。

    - GetCurrentThreadId
    """

    @staticmethod
    def GetCurrentThreadId() -> int:
        return Kernel32.dll().GetCurrentThreadId()

    @staticmethod
    def dll() -> ctypes.WinDLL:
        """ctypes.windll.kernel32"""
        return ctypes.windll.kernel32
