import torch

def tokenize(text, max_word_length=25, max_tokens=300):
    """
    Tokenizes input text into words and encodes each word into a tensor representation.

    Args:
        text (str): Input text to be tokenized.
        max_word_length (int, optional): Maximum number of characters for each word tensor. Defaults to 25.
        max_tokens (int, optional): Maximum number of tokens in the output tensor. Defaults to 300.

    Returns:
        torch.Tensor: Tensor representation of tokenized text.
    """
    tokens = text.split()
    tokenized = torch.zeros(max_tokens, max_word_length)
    for idx, token in enumerate(tokens):
        if idx < max_tokens:
            t =  pad_tensor(to_unicode(token), max_word_length)
            tokenized[idx] = t
    return tokenized

def to_unicode(text, tensor=True):
    """
    Converts input text into Unicode code points.

    Args:
        text (str): Input text to be converted.

    Returns:
        torch.Tensor: Tensor of Unicode code points.
    """
    code_points = [ord(char) for char in text]
    if tensor:
        code_points = torch.tensor(code_points).float()
    return code_points

def pad_tensor(text, max_length=1000):
    """
    Pads input tensor with zeros or truncates it to match the maximum length.

    Args:
        text (torch.Tensor): Input tensor to be padded or truncated.
        max_length (int, optional): Maximum length for the output tensor. Defaults to 1000.

    Returns:
        torch.Tensor: Padded or truncated tensor.
    """
    if len(text) < max_length:
        pad = (0, max_length - len(text))
        text = torch.nn.functional.pad(text.clone(), pad)
    else:
        text = text[:max_length]
    return text
