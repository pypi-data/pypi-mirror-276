__all__ = ("User32",)
import ctypes
import ctypes.wintypes as wintypes


class User32:
    """user32.dllのAPIの一部を使いやすくしたクラス。

    現在実装されている関数は以下の通り。
    関数名の末尾に"[Ez]"が付いているものについては、戻り値の型や一部処理の省略など簡素化された関数と、DLLオリジナルの関数の二つが実装されている。

    またdll関数を実行することでctypes.windll.user32へのアクセスを簡易化する。

    - AttachThreadInput
    - BringWindowToTop
    - FindWindowExW
    - EnumWindow[Ez]
    - GetWindowRect[Ez]
    - GetWindowTextLengthW
    - GetWindowTextW[Ez]
    - GetWindowThreadProcessId[Ez]
    - IsWindowEnabled
    - IsWindowVisible
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
        """スレッドの入力処理メカニズムを別のスレッドの入力処理メカニズムにアタッチまたはデタッチする。

        Args:
            idAttach (int): 別のスレッドにアタッチするスレッドの識別子。
            idAttachTo (int): idAttachがアタッチされるスレッドの識別子。
            fAttach (bool): Trueでアタッチ。Falseでデタッチ。

        Returns:
            bool: 成否。
        """
        return bool(User32.dll().AttachThreadInput(idAttach, idAttachTo, fAttach))

    @staticmethod
    def BringWindowToTop(hWnd: int) -> bool:
        """ウィンドウをZオーダーの先頭に移動する。

        Args:
            hWnd (int): ウィンドウハンドル。

        Returns:
            bool: 成否。
        """
        return bool(User32.dll().BringWindowToTop(hWnd))

    @staticmethod
    def EnumWindows(lpEnumFunc: "ctypes._FuncPointer", lParam: int) -> bool:
        """画面上の最上位ウィンドウをコールバック関数に列挙する。

        この関数を簡素化したEnumWindowsEzがある。

        Args:
            lpEnumFunc (ctypes._FuncPointer): コールバック関数へのポインター。
            lParam (int): コールバック関数に渡されるアプリケーション定義の値。

        Returns:
            bool: 成否。

        Note:
            lpEnumFuncは以下のような形式で定義する。

            pointer: ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
            callback: Callable[[int, int], bool]
            proc: pointer(callback)
        """
        return bool(User32.dll().EnumWindows(lpEnumFunc, lParam))

    @staticmethod
    def EnumWindowsEz() -> list[tuple[int, str]]:
        """画面上の最上位ウィンドウを列挙する。

        本来のEnumWindowsの簡素版。

        Returns:
            list[tuple[int, str]]: (プロセスID, ウィンドウネーム)のリスト。
        """
        result = []

        def callback(hWnd: int, lParam: int) -> bool:
            if User32.IsWindowVisible(hWnd):
                _, pid = User32.GetWindowThreadProcessIdEz(hWnd)
                title = User32.GetWindowTextWEz(hWnd)
                result.append((pid, title))
            return True

        proc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)(callback)
        User32.EnumWindows(proc, 0)
        return sorted(result, key=lambda x: x[1])

    @staticmethod
    def FindWindowExW(
        hWndParent: int | None = None,
        hWndChildAfter: int | None = None,
        lpszClass: str | None = None,
        lpszWindow: str | None = None,
    ) -> int:
        """クラス名とウィンドウ名が指定した文字列と一致するウィンドウのハンドルを取得する。

        Args:
            hWndParent (int | None, optional): 子ウィンドウを検索する親ウィンドウハンドル。
            hWndChildAfter (int | None, optional): 子ウィンドウハンドル。
            lpszClass (str | None, optional): クラス名またはクラスアトム。
            lpszWindow (str | None, optional): ウィンドウ名。

        Returns:
            int: ウィンドウハンドル。
        """
        return User32.dll().FindWindowExW(hWndParent, hWndChildAfter, lpszClass, lpszWindow)

    @staticmethod
    def GetWindowRect(hWnd: int, lpRect: wintypes.LPRECT) -> bool:
        """ウィンドウの外接する四角形のサイズを取得する。

        寸法は左上隅を基準とした画面座標。

        この関数を簡素化したGetWindowRectEzがある。

        Args:
            hWnd (int): ウィンドウハンドル。
            lpRect (wintypes.LPRECT): 寸法を受け取るポインタ。

        Returns:
            bool: 成否。
        """
        return bool(User32.dll().GetWindowRect(hWnd, lpRect))

    @staticmethod
    def GetWindowRectEz(hWnd: int) -> tuple[int, int, int, int]:
        """ウィンドウの外接する四角形のサイズを取得する。

        寸法は左上隅を基準とした画面座標。

        本来のGetWindowRectの簡素版。

        Args:
            hWnd (int): ウィンドウハンドル。

        Returns:
            tuple[int, int, int, int]: (左x座標, 左y座標, 右x座標, 右y座標)のタプル。
        """
        rect = wintypes.RECT()
        if not User32.GetWindowRect(hWnd, ctypes.pointer(rect)):  # type: ignore
            return -1, -1, -1, -1
        return (rect.left, rect.top, rect.right, rect.bottom)

    @staticmethod
    def GetWindowTextLengthW(hWnd: int) -> int:
        """ウィンドウのタイトルテキストの文字数を返す。

        Args:
            hWnd (int): ウィンドウハンドル。

        Returns:
            int: ウィンドウのタイトルテキストの文字数または0。
        """
        return User32.dll().GetWindowTextLengthW(hWnd)

    @staticmethod
    def GetWindowTextW(hWnd: int, lpString: ctypes.Array[wintypes.WCHAR], nMaxCount: int) -> int:
        """ウィンドウ(コントロール)のテキストをlpStringにコピーする。

        文字列がバッファーより長い場合、文字列は切り捨てられ、`null`文字で終了する。

        この関数を簡素化したGetWindowTextWEzがある。

        Args:
            hWnd (int): ウィンドウハンドル。
            lpString (ctypes.Array[wintypes.WCHAR]): テキストを受け取るバッファー。
            nMaxCount (int): バッファにコピーする最大文字数。

        Returns:
            int: コピーされた文字列の長さ、または0。
        """
        return User32.dll().GetWindowTextW(hWnd, lpString, nMaxCount)

    @staticmethod
    def GetWindowTextWEz(hWnd: int) -> str:
        """ウィンドウ(コントロール)のテキストを返す。

        DLL本来のGetWindowTextWの簡素版。

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
    def GetWindowThreadProcessId(hWnd: int, lpdwProcessId: wintypes.LPDWORD | None = None) -> int:
        """ウィンドウを作成したスレッドIDを返し、lpdwProcessIdにポインタを渡していればポインタにプロセスIDをコピーする。

        この関数を簡素化したGetWindowThreadProcessIdEzがある。

        Args:
            hWnd (int): ウィンドウハンドル。
            lpdwProcessId (wintypes.LPDWORD | None, optional): プロセスIDを受け取るポインタ。 Defaults to None.

        Returns:
            int: スレッドID。
        """
        return User32.dll().GetWindowThreadProcessId(hWnd, lpdwProcessId)

    @staticmethod
    def GetWindowThreadProcessIdEz(hWnd: int) -> tuple[int, int]:
        """ウィンドウのスレッドIDとプロセスIDを返す。

        DLL本来のGetWindowThreadProcessIdの簡素版。

        Args:
            hWnd (int): ウィンドウハンドル。

        Returns:
            tuple[int, int]: (スレッドID, プロセスID)のタプル。
        """
        proc = wintypes.DWORD()
        return User32.GetWindowThreadProcessId(hWnd, ctypes.pointer(proc)), proc.value  # type: ignore

    @staticmethod
    def IsWindowEnabled(hWnd: int) -> bool:
        """ウィンドウがマウスとキーボードの入力に対して有効になっているかどうかを返する。

        Args:
            hWnd (int): ウィンドウハンドル。

        Returns:
            bool: 有効かどうか。
        """
        return bool(User32.dll().IsWindowEnabled(hWnd))

    @staticmethod
    def IsWindowVisible(hWnd: int) -> bool:
        return bool(User32.dll().IsWindowVisible(hWnd))

    @staticmethod
    def MoveWindow(hWnd: int, X: int, Y: int, nWidth: int, nHeight: int, bRepaint: bool) -> bool:
        """ウィンドウを指定座標に動かす。

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
        return bool(User32.dll().MoveWindow(hWnd, X, Y, nWidth, nHeight, bRepaint))

    @staticmethod
    def SendMessageW(
        hWnd: int,
        Msg: int,
        wParam: int,
        lParam: int,
    ) -> int:
        """指定したメッセージをウィンドウに送信する。

        Args:
            hWnd (int): ウィンドウハンドル。
            Msg (int): 送信するメッセージ。
            wParam (int): 追加のメッセージ固有情報。
            lParam (int): 追加のメッセージ固有情報。

        Returns:
            int: ウィンドウからの応答。
        """
        return User32.dll().SendMessageW(hWnd, Msg, wParam, lParam)

    @staticmethod
    def SetActiveWindow(hWnd: int) -> int:
        """ウィンドウをアクティブ化する。

        Args:
            hWnd (int): ウィンドウハンドル。

        Returns:
            int: 以前アクティブだったウィンドウのハンドル。または0。
        """
        return User32.dll().SetActiveWindow(hWnd)

    @staticmethod
    def SetFocus(hWnd: int) -> int:
        """キーボードフォーカスをウィンドウに設定する。

        Args:
            hWnd (int): ウィンドウハンドル。

        Returns:
            int: 以前キーボードフォーカスを持っていたウィンドウのハンドル。または0。
        """
        return User32.dll().SetFocus(hWnd)

    @staticmethod
    def SetForegroundWindow(hWnd: int) -> bool:
        """ウィンドウを作成したスレッドをフォアグラウンドに移動し、ウィンドウをアクティブにする。

        Args:
            hWnd (int): ウィンドウハンドル。

        Returns:
            bool: 成否。
        """
        return bool(User32.dll().SetForegroundWindow(hWnd))

    @staticmethod
    def SetWindowPos(
        hWnd: int,
        hWndInsertAfter: int | None = None,
        X: int | None = None,
        Y: int | None = None,
        cx: int | None = None,
        cy: int | None = None,
        uFlags: int | None = None,
    ) -> bool:
        """子ウィンドウ、ポップアップウィンドウ、トップレベルウィンドウのサイズ、位置、Zの順序を変更する。

        Args:
            hWnd (int): ウィンドウハンドル。
            hWndInsertAfter (int | None, optional): Z順序で位置指定されたウィンドウの前にあるウィンドウへのハンドル。 ウィンドウハンドルまたは`constants.hWndInsertAfter`内の定数。 Defaults to None.
            X (int | None, optional): ウィンドウ左側の新しいX座標。 Defaults to None.
            Y (int | None, optional): ウィンドウ左側の新しいY座標。 Defaults to None.
            cx (int | None, optional): ウィンドウの新しい幅(ピクセル)。 Defaults to None.
            cy (int | None, optional): ウィンドウの新しい高さ(ピクセル)。 Defaults to None.
            uFlags (int | None, optional): ウィンドウサイズ設定とフラグ。`constants.uFlags`内の定数を`|`演算子で組み合わせて使用。 Defaults to None.

        Returns:
            bool: 成否。
        """
        return bool(User32.dll().SetWindowPos(hWnd, hWndInsertAfter, X, Y, cx, cy, uFlags))

    @staticmethod
    def ShowWindow(hWnd: int, nCmdShow: int) -> bool:
        """指定したウィンドウの表示状態に設定する。

        Args:
            hWnd (int): ウィンドウハンドル。
            nCmdShow (int): ウィンドウの表示方法。constants.nCmdShow内の定数を使用。

        Returns:
            bool: 以前のウィンドウの表示状態。
        """
        return bool(User32.dll().ShowWindow(hWnd, nCmdShow))

    @staticmethod
    def dll() -> ctypes.WinDLL:
        """ctypes.windll.user32。"""
        return ctypes.windll.user32
