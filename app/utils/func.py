import inspect
import re


def format_doc(func):
    doc = inspect.getdoc(func)
    enhanced_doc = f"{doc or ''}"

    return remove_urls(enhanced_doc)


def remove_urls(text: str) -> str:
    # 更新的正则表达式，可以匹配包括路径在内的所有网址
    url_pattern = r"http[s]?://\S+"
    # 替换网址为空字符串
    return re.sub(url_pattern, "", text)


def format_parameters(sig: inspect.Signature) -> str:
    """格式化参数说明"""
    params = []
    for name, param in sig.parameters.items():
        default = (
            ""
            if param.default == inspect.Parameter.empty
            else f" (默认值: {param.default})"
        )
        params.append(f"- {name}{default}")
    return "\n".join(params)
