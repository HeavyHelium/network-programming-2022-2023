class Status: 
    def __init__(self, label: str, msg: str) -> None: 
        self._label = label
        self._msg = msg

    def __str__(self) -> str: 
        return f"[{self._label}] {self._msg}"
    
    def __repr__(self) -> str: 
        return str((self._label, self._msg))