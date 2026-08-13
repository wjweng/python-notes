"""第一支程式：把文字顯示在畫面上。"""


def greeting(name: str = "Python") -> str:
    """組出打招呼的文字。"""
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(greeting())
    print("我的第一支程式")
