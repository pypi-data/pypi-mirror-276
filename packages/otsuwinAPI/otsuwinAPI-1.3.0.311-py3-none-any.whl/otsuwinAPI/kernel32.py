__all__ = ("Kernel32",)
import ctypes


class Kernel32:
    """kernel.dllのAPIの一部を使いやすくしたクラス。

    現在実装されている関数は以下の通りです。
    関数名の末尾に"[Ez]"が付いているものについては戻り値の型や一部処理の省略など簡素化された関数と、DLLオリジナルの関数の二つが実装されています。

    - GetCurrentThreadId
    """

    @staticmethod
    def GetCurrentThreadId() -> int:
        return ctypes.windll.kernel32.GetCurrentThreadId()
