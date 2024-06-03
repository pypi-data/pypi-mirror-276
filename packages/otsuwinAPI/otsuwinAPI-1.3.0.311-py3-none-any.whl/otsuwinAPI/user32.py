__all__ = ("User32",)
import ctypes
import ctypes.wintypes as wintypes

from typing import Optional, cast


class User32:
    """user32.dllのAPIの一部を使いやすくしたクラス。

    現在実装されている関数は以下の通りです。
    関数名の末尾に"[Ez]"が付いているものについては戻り値の型や一部処理の省略など簡素化された関数と、DLLオリジナルの関数の二つが実装されています。

    - AttachThreadInput
    - BringWindowToTop
    - FindWindowExW
    - GetWindowRect[Ez]
    - GetWindowTextLengthW
    - GetWindowTextW[Ez]
    - GetWindowThreadProcessId[Ez]
    - IsWindowEnabled
    - MoveWindow
    - SendMessageW
    - SetActiveWindow
    - SetFocus
    - SetForegroundWindow
    - SetWindowPos
    - ShowWindow
    """

    @staticmethod
    def AttachThreadInput(idAttach: int, idAttachTo: int, fAttach: bool) -> bool:
        """スレッドの入力処理メカニズムを別のスレッドの入力処理メカニズムにアタッチまたはデタッチします。

        Args:
            idAttach (int): 別のスレッドにアタッチするスレッドの識別子。
            idAttachTo (int): idAttachがアタッチされるスレッドの識別子。
            fAttach (bool): Trueでアタッチ。Falseでデタッチ。

        Returns:
            bool: 成否。
        """
        return bool(ctypes.windll.user32.AttachThreadInput(idAttach, idAttachTo, fAttach))

    @staticmethod
    def BringWindowToTop(hWnd: int) -> bool:
        """ウィンドウをZオーダーの先頭に移動します。

        Args:
            hWnd (int): ウィンドウハンドル。

        Returns:
            bool: 成否。
        """
        return bool(ctypes.windll.user32.BringWindowToTop(hWnd))

    @staticmethod
    def FindWindowExW(
        hWndParent: Optional[int] = None,
        hWndChildAfter: Optional[int] = None,
        lpszClass: Optional[str] = None,
        lpszWindow: Optional[str] = None,
    ) -> int:
        """クラス名とウィンドウ名が指定した文字列と一致するウィンドウのハンドルを取得します。

        Args:
            hWndParent (Optional[int], optional): 子ウィンドウを検索する親ウィンドウハンドル。
            hWndChildAfter (Optional[int], optional): 子ウィンドウハンドル。
            lpszClass (Optional[str], optional): クラス名またはクラスアトム。
            lpszWindow (Optional[str], optional): ウィンドウ名。

        Returns:
            int: ウィンドウハンドル。
        """
        return ctypes.windll.user32.FindWindowExW(hWndParent, hWndChildAfter, lpszClass, lpszWindow)

    @staticmethod
    def GetWindowRect(hWnd: int, lpRect: wintypes.LPRECT) -> bool:
        """ウィンドウの外接する四角形のサイズを取得します。

        寸法は左上隅を基準とした画面座標です。

        この関数を簡素化したGetWindowRectEzがあります。

        Args:
            hWnd (int): ウィンドウハンドル。
            lpRect (wintypes.LPRECT): 寸法を受け取るポインタ。

        Returns:
            bool: 成否。
        """
        return bool(ctypes.windll.user32.GetWindowRect(hWnd, lpRect))

    @staticmethod
    def GetWindowRectEz(hWnd: int) -> tuple[int, int, int, int]:
        """ウィンドウの外接する四角形のサイズを取得します。

        寸法は左上隅を基準とした画面座標です。

        本来のGetWindowRectを簡素化しています。

        Args:
            hWnd (int): ウィンドウハンドル。

        Returns:
            tuple[int, int, int, int]: (左x座標, 左y座標, 右x座標, 右y座標)のタプル。
        """
        rect = wintypes.RECT()
        if not User32.GetWindowRect(hWnd, ctypes.pointer(rect)):
            return -1, -1, -1, -1
        return cast(tuple[int, int, int, int], (rect.left, rect.top, rect.right, rect.bottom))

    @staticmethod
    def GetWindowTextLengthW(hWnd: int) -> int:
        """ウィンドウのタイトルテキストの文字数を返します。

        Args:
            hWnd (int): ウィンドウハンドル。

        Returns:
            int: ウィンドウのタイトルテキストの文字数または0。
        """
        return ctypes.windll.user32.GetWindowTextLengthW(hWnd)

    @staticmethod
    def GetWindowTextW(hWnd: int, lpString: ctypes.Array[wintypes.WCHAR], nMaxCount: int) -> int:
        """ウィンドウ(コントロール)のテキストをlpStringにコピーします。

        文字列がバッファーより長い場合、文字列は切り捨てられ、`null`文字で終了します。

        この関数を簡素化したGetWindowTextWEzがあります。

        Args:
            hWnd (int): ウィンドウハンドル。
            lpString (ctypes.Array[wintypes.WCHAR]): テキストを受け取るバッファー。
            nMaxCount (int): バッファにコピーする最大文字数。

        Returns:
            int: コピーされた文字列の長さ、または0。
        """
        return ctypes.windll.user32.GetWindowTextW(hWnd, lpString, nMaxCount)

    @staticmethod
    def GetWindowTextWEz(hWnd: int) -> str:
        """ウィンドウ(コントロール)のテキストを返します。

        DLL本来のGetWindowTextWを簡素化しています。

        Args:
            hWnd (int): ウィンドウハンドル。

        Returns:
            str: ウィンドウのタイトル。
        """
        text_length = User32.GetWindowTextLengthW(hWnd) + 1
        title = ctypes.create_unicode_buffer(text_length)
        User32.GetWindowTextW(hWnd, title, text_length)
        return title.value

    @staticmethod
    def GetWindowThreadProcessId(hWnd: int, lpdwProcessId: Optional[wintypes.LPDWORD] = None) -> int:
        """ウィンドウを作成したスレッドIDを返し、lpdwProcessIdにポインタを渡していればポインタにプロセスIDをコピーします。

        この関数を簡素化したGetWindowThreadProcessIdEzがあります。

        Args:
            hWnd (int): ウィンドウハンドル。
            lpdwProcessId (Optional[wintypes.LPDWORD], optional): プロセスIDを受け取るポインタ。 Defaults to None.

        Returns:
            int: スレッドID。
        """
        return ctypes.windll.user32.GetWindowThreadProcessId(hWnd, lpdwProcessId)

    @staticmethod
    def GetWindowThreadProcessIdEz(hWnd: int) -> tuple[int, int]:
        """ウィンドウのスレッドIDとプロセスIDを返します。

        DLL本来のGetWindowThreadProcessIdを簡素化しています。

        Args:
            hWnd (int): ウィンドウハンドル。

        Returns:
            tuple[int, int]: (スレッドID, プロセスID)のタプル。
        """
        proc = wintypes.DWORD()
        return User32.GetWindowThreadProcessId(hWnd, ctypes.pointer(proc)), proc.value

    @staticmethod
    def IsWindowEnabled(hWnd: int) -> bool:
        """ウィンドウがマウスとキーボードの入力に対して有効になっているかどうかを返します。

        Args:
            hWnd (int): ウィンドウハンドル。

        Returns:
            bool: 有効かどうか。
        """
        return bool(ctypes.windll.user32.IsWindowEnabled(hWnd))

    @staticmethod
    def MoveWindow(hWnd: int, X: int, Y: int, nWidth: int, nHeight: int, bRepaint: bool) -> bool:
        """ウィンドウを指定座標に動かします。

        Args:
            hWnd (int): ウィンドウハンドル。
            X (int): 左上X座標。
            Y (int): 左上Y座標。
            nWidth (int): ウィンドウの幅
            nHeight (int): ウィンドウの高さ
            bRepaint (bool): 再描画の有無。

        Returns:
            bool: 成否。
        """
        return bool(ctypes.windll.user32.MoveWindow(hWnd, X, Y, nWidth, nHeight, bRepaint))

    @staticmethod
    def SendMessageW(
        hWnd: int,
        Msg: int,
        wParam: int,
        lParam: int,
    ) -> int:
        """指定したメッセージをウィンドウに送信します。

        Args:
            hWnd (int): ウィンドウハンドル。
            Msg (int): 送信するメッセージ。
            wParam (int): 追加のメッセージ固有情報。
            lParam (int): 追加のメッセージ固有情報。

        Returns:
            int: ウィンドウからの応答。
        """
        return ctypes.windll.user32.SendMessageW(hWnd, Msg, wParam, lParam)

    @staticmethod
    def SetActiveWindow(hWnd: int) -> int:
        """ウィンドウをアクティブ化します。

        Args:
            hWnd (int): ウィンドウハンドル。

        Returns:
            int: 以前アクティブだったウィンドウのハンドル。または0。
        """
        return ctypes.windll.user32.SetActiveWindow(hWnd)

    @staticmethod
    def SetFocus(hWnd: int) -> int:
        """キーボードフォーカスをウィンドウに設定します。

        Args:
            hWnd (int): ウィンドウハンドル。

        Returns:
            int: 以前キーボードフォーカスを持っていたウィンドウのハンドル。または0。
        """
        return ctypes.windll.user32.SetFocus(hWnd)

    @staticmethod
    def SetForegroundWindow(hWnd: int) -> bool:
        """ウィンドウを作成したスレッドをフォアグラウンドに移動し、ウィンドウをアクティブにします。

        Args:
            hWnd (int): ウィンドウハンドル。

        Returns:
            bool: 成否。
        """
        return bool(ctypes.windll.user32.SetForegroundWindow(hWnd))

    @staticmethod
    def SetWindowPos(
        hWnd: int,
        hWndInsertAfter: Optional[int] = None,
        X: Optional[int] = None,
        Y: Optional[int] = None,
        cx: Optional[int] = None,
        cy: Optional[int] = None,
        uFlags: Optional[int] = None,
    ) -> bool:
        """子ウィンドウ、ポップアップウィンドウ、トップレベルウィンドウのサイズ、位置、Zの順序を変更します。

        Args:
            hWnd (int): ウィンドウハンドル。
            hWndInsertAfter (Optional[int], optional): Z順序で位置指定されたウィンドウの前にあるウィンドウへのハンドル。 ウィンドウハンドルまたは`constants.hWndInsertAfter`内の定数。 Defaults to None.
            X (Optional[int], optional): ウィンドウ左側の新しいX座標。 Defaults to None.
            Y (Optional[int], optional): ウィンドウ左側の新しいY座標。 Defaults to None.
            cx (Optional[int], optional): ウィンドウの新しい幅(ピクセル)。 Defaults to None.
            cy (Optional[int], optional): ウィンドウの新しい高さ(ピクセル)。 Defaults to None.
            uFlags (Optional[int], optional): ウィンドウサイズ設定とフラグ。`constants.uFlags`内の定数を`|`演算子で組み合わせて使用。 Defaults to None.

        Returns:
            bool: 成否。
        """
        return bool(ctypes.windll.user32.SetWindowPos(hWnd, hWndInsertAfter, X, Y, cx, cy, uFlags))

    @staticmethod
    def ShowWindow(hWnd: int, nCmdShow: int) -> bool:
        """指定したウィンドウの表示状態に設定します。

        Args:
            hWnd (int): ウィンドウハンドル。
            nCmdShow (int): ウィンドウの表示方法。constants.nCmdShow内の定数を使用。

        Returns:
            bool: 以前のウィンドウの表示状態。
        """
        return bool(ctypes.windll.user32.ShowWindow(hWnd, nCmdShow))
